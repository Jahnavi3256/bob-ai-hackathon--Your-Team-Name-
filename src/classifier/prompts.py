"""
TrialGuard — ICH E6(R2) classification prompt templates.

These prompts are sent to LLM backends (Gemini, watsonx) to classify
protocol deviations as Major, Minor, or Administrative.
"""

from __future__ import annotations

ICH_E6_SYSTEM_PROMPT = """You are a Good Clinical Practice (GCP) auditor classifying protocol deviations for clinical trial TG-101 per ICH E6(R2) standards.

Classify each deviation as exactly one of:
- Major: Deviation affects subject safety, subject rights, well-being, data integrity, or trial credibility. Requires FDA reporting and formal CAPA.
- Minor: Procedural deviation not affecting critical variables. Documented but does not require immediate action.
- Administrative: Clerical or documentation deviation without clinical or data integrity impact.

Return your answer as strict JSON: {"severity": "Major|Minor|Administrative", "rationale": "one sentence citing the ICH E6 principle", "confidence": 0.0-1.0}"""

FEW_SHOT_EXAMPLES = [
    {
        "deviation_type": "Wrong Dose",
        "deviation_reason": "Administered dose was 150 mg; protocol-specified dose is 100 mg.",
        "expected": {
            "severity": "Major",
            "rationale": "Incorrect dosing directly affects subject safety and primary endpoint validity per ICH E6(R2) 5.18.3.",
            "confidence": 0.98,
        },
    },
    {
        "deviation_type": "Prohibited Medication",
        "deviation_reason": "Protocol-prohibited Drug X was recorded during visit V3.",
        "expected": {
            "severity": "Major",
            "rationale": "Concomitant use of a prohibited medication may confound efficacy endpoints per ICH E6(R2) 4.5.",
            "confidence": 0.97,
        },
    },
    {
        "deviation_type": "Visit Timing",
        "deviation_reason": "Visit V2 occurred on day 24, 10 days from scheduled day 14 (allowed window plus or minus 3).",
        "expected": {
            "severity": "Major",
            "rationale": "Assessment window exceedance beyond 7 days risks missing endpoint observations per ICH E6(R2) 8.3.",
            "confidence": 0.92,
        },
    },
    {
        "deviation_type": "Visit Timing",
        "deviation_reason": "Visit V3 occurred on day 32, 4 days from scheduled day 28 (allowed window plus or minus 3).",
        "expected": {
            "severity": "Minor",
            "rationale": "Visit outside window but within 7 days; assessments still valid.",
            "confidence": 0.88,
        },
    },
    {
        "deviation_type": "Missing Lab",
        "deviation_reason": "Required CBC was not recorded at V4.",
        "expected": {
            "severity": "Minor",
            "rationale": "Required safety lab omitted; clinically relevant but does not invalidate efficacy endpoint.",
            "confidence": 0.90,
        },
    },
    {
        "deviation_type": "Documentation",
        "deviation_reason": "Source document missing coordinator initial on visit form.",
        "expected": {
            "severity": "Administrative",
            "rationale": "No clinical or data integrity impact per ICH E6(R2) 4.9.",
            "confidence": 0.95,
        },
    },
]


def build_user_prompt(deviation_type: str, deviation_reason: str) -> str:
    """Assembles the few-shot user prompt for a single deviation.

    Includes all FEW_SHOT_EXAMPLES as in-context demonstrations followed
    by the target deviation for classification.
    """
    lines: list[str] = []

    lines.append("Below are example classifications:\n")
    for ex in FEW_SHOT_EXAMPLES:
        lines.append(f"Deviation Type: {ex['deviation_type']}")
        lines.append(f"Reason: {ex['deviation_reason']}")
        lines.append(f"Classification: {ex['expected']}\n")

    lines.append("Now classify this deviation:")
    lines.append(f"Deviation Type: {deviation_type}")
    lines.append(f"Reason: {deviation_reason}")
    lines.append("Classification (strict JSON only):")

    return "\n".join(lines)
