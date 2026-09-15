"""
TrialGuard — Severity classifier backends.

Three pluggable backends with a common interface:

    backend.classify(deviation: Deviation) -> ClassificationResult

Backends
--------
DeterministicBackend  — rule-based, always available, derived from TG-101 rules.
GeminiBackend         — Google Gemini API; requires GEMINI_API_KEY env var.
WatsonxBackend        — IBM watsonx.ai Granite; requires WATSONX_API_KEY,
                        WATSONX_PROJECT_ID, and WATSONX_URL env vars.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from src.models import Deviation


# ---------------------------------------------------------------------------
# Shared result type
# ---------------------------------------------------------------------------


@dataclass
class ClassificationResult:
    """Result of a single deviation classification."""

    severity: str        # "Major" | "Minor" | "Administrative"
    rationale: str       # One sentence citing the applicable ICH E6 principle
    confidence: float    # 0.0–1.0
    source: str          # "gemini" | "watsonx" | "watsonx-stub" | "deterministic"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_days_off(reason: str) -> int | None:
    """Extract the numeric days-off value from a Visit Timing deviation reason.

    Handles the pattern produced by check_visit_timing.py:
        "Visit V2 occurred on day 24, 10 days from scheduled day 14 (allowed window ±3)"
                                       ^^
    Returns None if the pattern is not found.
    """
    match = re.search(r",\s*(\d+)\s+days?\s+from\s+scheduled", reason)
    if match:
        return int(match.group(1))
    return None


def _parse_json_from_text(text: str) -> dict:
    """Extract the first JSON object from an LLM response string.

    Raises ValueError if no valid JSON object is found.
    """
    # Try the whole text first (model may return clean JSON)
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Fall back to the first {...} block
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"No valid JSON object found in LLM response: {text!r}")


# ---------------------------------------------------------------------------
# Deterministic backend
# ---------------------------------------------------------------------------


class DeterministicBackend:
    """Rule-based classifier derived from TG-101 protocol rules.

    Classification rules (from trialguard_protocol_rules.csv):
      - Wrong Dose            → Major
      - Prohibited Medication → Major
      - Visit Timing          → Major if days_off > 7, else Minor
      - Missing Lab           → Minor
      - Documentation         → Administrative

    Always available; used as fallback when LLM backends are unavailable.
    """

    _RULES: dict[str, str] = {
        "Wrong Dose": "Major",
        "Prohibited Medication": "Major",
        "Missing Lab": "Minor",
        "Documentation": "Administrative",
    }

    _RATIONALES: dict[str, str] = {
        "Wrong Dose": (
            "Incorrect dosing directly affects subject safety and primary endpoint "
            "validity per ICH E6(R2) 5.18.3."
        ),
        "Prohibited Medication": (
            "Concomitant use of a prohibited medication may confound efficacy "
            "endpoints per ICH E6(R2) 4.5."
        ),
        "Visit Timing Major": (
            "Assessment window exceedance beyond 7 days risks missing endpoint "
            "observations per ICH E6(R2) 8.3."
        ),
        "Visit Timing Minor": (
            "Visit outside window but within 7 days; assessments still valid "
            "per ICH E6(R2) 8.3."
        ),
        "Missing Lab": (
            "Required safety lab omitted; clinically relevant but does not "
            "invalidate efficacy endpoint per ICH E6(R2) 5.18.3."
        ),
        "Documentation": (
            "No clinical or data integrity impact per ICH E6(R2) 4.9."
        ),
    }

    def classify(self, deviation: Deviation) -> ClassificationResult:
        """Classify a deviation using deterministic TG-101 rules."""
        dev_type = deviation.deviation_type

        if dev_type == "Visit Timing":
            days_off = _parse_days_off(deviation.deviation_reason)
            if days_off is not None and days_off > 7:
                severity = "Major"
                rationale = self._RATIONALES["Visit Timing Major"]
                confidence = 0.95
            else:
                severity = "Minor"
                rationale = self._RATIONALES["Visit Timing Minor"]
                confidence = 0.90
        elif dev_type in self._RULES:
            severity = self._RULES[dev_type]
            rationale = self._RATIONALES[dev_type]
            confidence = 0.95
        else:
            # Unknown type — default to Minor with low confidence
            severity = "Minor"
            rationale = (
                "Deviation type not explicitly mapped; defaulting to Minor "
                "pending review per ICH E6(R2) 5.1."
            )
            confidence = 0.50

        return ClassificationResult(
            severity=severity,
            rationale=rationale,
            confidence=confidence,
            source="deterministic",
        )


# ---------------------------------------------------------------------------
# Gemini backend
# ---------------------------------------------------------------------------


class GeminiBackend:
    """Google Gemini API classifier.

    Activates when the GEMINI_API_KEY environment variable is set.
    Falls back to DeterministicBackend on any parse or API error.
    """

    def __init__(self) -> None:
        import os

        import google.generativeai as genai  # type: ignore[import-untyped]

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.model = genai.GenerativeModel(model_name)
        self._fallback = DeterministicBackend()

    def classify(self, deviation: Deviation) -> ClassificationResult:
        """Classify using Gemini; falls back to deterministic on failure."""
        from src.classifier.prompts import ICH_E6_SYSTEM_PROMPT, build_user_prompt

        system_and_user = (
            ICH_E6_SYSTEM_PROMPT
            + "\n\n"
            + build_user_prompt(deviation.deviation_type, deviation.deviation_reason)
        )

        try:
            response = self.model.generate_content(system_and_user)
            parsed = _parse_json_from_text(response.text)

            severity = str(parsed.get("severity", "")).strip()
            if severity not in ("Major", "Minor", "Administrative"):
                raise ValueError(f"Unexpected severity value: {severity!r}")

            return ClassificationResult(
                severity=severity,
                rationale=str(parsed.get("rationale", "")),
                confidence=float(parsed.get("confidence", 0.80)),
                source="gemini",
            )
        except Exception as exc:  # noqa: BLE001
            import sys
            print(f"GEMINI FAILURE: {type(exc).__name__}: {exc}", file=sys.stderr)
            result = self._fallback.classify(deviation)
            result.source = "deterministic"
            return result


# ---------------------------------------------------------------------------
# watsonx backend
# ---------------------------------------------------------------------------


class WatsonxBackend:
    """IBM watsonx.ai Granite classifier — documented target integration.

    Activates when WATSONX_API_KEY, WATSONX_PROJECT_ID, and WATSONX_URL are
    all set.  Raises RuntimeError with a clear message if any var is missing.

    The real Granite call is stubbed with a TODO; the placeholder returns the
    DeterministicBackend result tagged as source="watsonx-stub".
    """

    def __init__(self) -> None:
        import os

        required = ["WATSONX_API_KEY", "WATSONX_PROJECT_ID", "WATSONX_URL"]
        missing = [v for v in required if not os.getenv(v)]
        if missing:
            raise RuntimeError(
                f"watsonx.ai unavailable — missing env vars: {missing}. "
                f"Populate them in .env to activate this backend."
            )

        # TODO: initialise the ibm-watsonx-ai SDK client when credentials are live.
        # Example (not yet active):
        #   from ibm_watsonx_ai import Credentials, APIClient
        #   from ibm_watsonx_ai.foundation_models import ModelInference
        #   credentials = Credentials(url=os.getenv("WATSONX_URL"),
        #                             api_key=os.getenv("WATSONX_API_KEY"))
        #   self.client = APIClient(credentials)
        #   self.model = ModelInference(
        #       model_id="ibm/granite-13b-instruct-v2",
        #       project_id=os.getenv("WATSONX_PROJECT_ID"),
        #       api_client=self.client,
        #   )
        self._fallback = DeterministicBackend()

    def classify(self, deviation: Deviation) -> ClassificationResult:
        """Classify using watsonx Granite.

        TODO: replace stub with a real Granite inference call once credentials
        are available.  The prompt to use is already built by
        ``src.classifier.prompts.build_user_prompt``.
        """
        # TODO: real Granite call — replace the lines below with:
        #   from src.classifier.prompts import ICH_E6_SYSTEM_PROMPT, build_user_prompt
        #   prompt = build_user_prompt(deviation.deviation_type, deviation.deviation_reason)
        #   response = self.model.generate(prompt=prompt, ...)
        #   parsed = _parse_json_from_text(response["results"][0]["generated_text"])
        #   return ClassificationResult(severity=..., source="watsonx")

        result = self._fallback.classify(deviation)
        result.source = "watsonx-stub"
        return result
