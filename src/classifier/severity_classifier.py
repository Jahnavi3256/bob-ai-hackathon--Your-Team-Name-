"""
TrialGuard — SeverityClassifier orchestrator.

Selects and manages a classifier backend, then exposes classify() and
classify_batch() for the rest of the application to consume.
"""

from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

from src.models import Deviation
from src.classifier.backends import (
    ClassificationResult,
    DeterministicBackend,
    GeminiBackend,
    WatsonxBackend,
)


class SeverityClassifier:
    """Orchestrates backend selection and deviation classification.

    Parameters
    ----------
    backend:
        "auto"          — try gemini → watsonx → deterministic (first that works)
        "gemini"        — use GeminiBackend; raises if GEMINI_API_KEY not set
        "watsonx"       — use WatsonxBackend; raises if any watsonx env var missing
        "deterministic" — always use DeterministicBackend (rule-based, no LLM)
    """

    def __init__(self, backend: str = "auto") -> None:
        self._backend_name: str
        self._backend: DeterministicBackend | GeminiBackend | WatsonxBackend

        if backend == "deterministic":
            self._backend = DeterministicBackend()
            self._backend_name = "deterministic"

        elif backend == "gemini":
            self._backend = GeminiBackend()
            self._backend_name = "gemini"

        elif backend == "watsonx":
            self._backend = WatsonxBackend()
            self._backend_name = "watsonx"

        elif backend == "auto":
            self._backend, self._backend_name = self._auto_select()

        else:
            raise ValueError(
                f"Unknown backend {backend!r}. "
                "Choose from: 'auto', 'gemini', 'watsonx', 'deterministic'."
            )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def classify(self, deviation: Deviation) -> ClassificationResult:
        """Classify a single deviation.

        On LLM failure the active backend falls back to deterministic
        internally (see GeminiBackend / WatsonxBackend).
        """
        return self._backend.classify(deviation)

    def classify_batch(self, deviations: list[Deviation]) -> list[Deviation]:
        """Classify a list of deviations in place.

        Mutates each Deviation:
          - deviation.severity       → "Major" | "Minor" | "Administrative"
          - deviation.severity_source → backend name used for that result

        Returns the same list for convenience.
        """
        for deviation in deviations:
            result = self._backend.classify(deviation)
            deviation.severity = result.severity
            deviation.severity_source = result.source
        return deviations

    def get_active_backend_name(self) -> str:
        """Return the name of the currently active backend."""
        return self._backend_name

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _auto_select() -> tuple[DeterministicBackend | GeminiBackend | WatsonxBackend, str]:
        """Try backends in priority order: gemini → watsonx → deterministic."""
        try:
            backend = GeminiBackend()
            return backend, "gemini"
        except (RuntimeError, ImportError):
            pass

        try:
            backend = WatsonxBackend()
            return backend, "watsonx"
        except (RuntimeError, ImportError):
            pass

        return DeterministicBackend(), "deterministic"
