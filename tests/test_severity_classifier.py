"""
Tests for src/classifier/severity_classifier.py and its backends.
"""

from __future__ import annotations

import os

import pytest

from src.models import Deviation
from src.classifier.backends import DeterministicBackend, ClassificationResult
from src.classifier.severity_classifier import SeverityClassifier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_deviation(deviation_type: str, deviation_reason: str) -> Deviation:
    return Deviation(
        trial_id="TG-101",
        site_id="S01",
        patient_id="P001",
        visit_id="V2",
        deviation_type=deviation_type,
        deviation_reason=deviation_reason,
    )


# ---------------------------------------------------------------------------
# Test 1: DeterministicBackend is available and classifies Wrong Dose as Major
# ---------------------------------------------------------------------------


def test_deterministic_backend_available():
    backend = DeterministicBackend()
    dev = _make_deviation(
        "Wrong Dose",
        "Administered dose was 150 mg; protocol-specified dose is 100 mg.",
    )
    result = backend.classify(dev)
    assert isinstance(result, ClassificationResult)
    assert result.severity == "Major"
    assert result.source == "deterministic"
    assert result.confidence > 0


# ---------------------------------------------------------------------------
# Test 2: DeterministicBackend correctly classifies all deviation types
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "deviation_type, deviation_reason, expected_severity",
    [
        (
            "Wrong Dose",
            "Administered dose was 150 mg; protocol-specified dose is 100 mg.",
            "Major",
        ),
        (
            "Prohibited Medication",
            "Protocol-prohibited Drug X was recorded during visit V3.",
            "Major",
        ),
        (
            "Visit Timing",
            "Visit V2 occurred on day 24, 10 days from scheduled day 14 (allowed window ±3)",
            "Major",  # days_off=10 > 7 → Major
        ),
        (
            "Visit Timing",
            "Visit V3 occurred on day 32, 4 days from scheduled day 28 (allowed window ±3)",
            "Minor",  # days_off=4 ≤ 7 → Minor
        ),
        (
            "Missing Lab",
            "Required CBC was not recorded at V4.",
            "Minor",
        ),
        (
            "Documentation",
            "Source document missing coordinator initial on visit form.",
            "Administrative",
        ),
    ],
)
def test_deterministic_classifies_all_types(
    deviation_type: str, deviation_reason: str, expected_severity: str
):
    backend = DeterministicBackend()
    dev = _make_deviation(deviation_type, deviation_reason)
    result = backend.classify(dev)
    assert result.severity == expected_severity, (
        f"Expected {expected_severity!r} for type={deviation_type!r}, "
        f"got {result.severity!r}"
    )


# ---------------------------------------------------------------------------
# Test 3: SeverityClassifier auto-selects gemini when GEMINI_API_KEY is set
# ---------------------------------------------------------------------------


def test_classifier_auto_selects_gemini_when_key_present(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-test-key")

    # Patch GeminiBackend.__init__ so it doesn't actually call the real SDK
    original_init = None

    def _fake_gemini_init(self):  # noqa: ANN001
        import google.generativeai as genai  # type: ignore[import-untyped]
        # Skip real configure/model creation for the test
        self.model = None
        self._fallback = DeterministicBackend()

    import src.classifier.backends as backends_mod
    monkeypatch.setattr(backends_mod.GeminiBackend, "__init__", _fake_gemini_init)

    classifier = SeverityClassifier(backend="auto")
    assert classifier.get_active_backend_name() == "gemini"


# ---------------------------------------------------------------------------
# Test 4: SeverityClassifier falls back to deterministic when no LLM env vars
# ---------------------------------------------------------------------------


def test_classifier_falls_back_to_deterministic(monkeypatch):
    # Ensure none of the LLM env vars are set
    for var in ("GEMINI_API_KEY", "WATSONX_API_KEY", "WATSONX_PROJECT_ID", "WATSONX_URL"):
        monkeypatch.delenv(var, raising=False)

    classifier = SeverityClassifier(backend="auto")
    assert classifier.get_active_backend_name() == "deterministic"


# ---------------------------------------------------------------------------
# Test 5: classify_batch mutates severity field on every Deviation
# ---------------------------------------------------------------------------


def test_classify_batch_mutates_severity_field():
    classifier = SeverityClassifier(backend="deterministic")

    deviations = [
        _make_deviation("Wrong Dose", "Administered dose was 150 mg; protocol-specified dose is 100 mg."),
        _make_deviation("Missing Lab", "Required CBC was not recorded at V2."),
        _make_deviation(
            "Visit Timing",
            "Visit V2 occurred on day 24, 10 days from scheduled day 14 (allowed window ±3)",
        ),
    ]
    # Confirm severities are None before classification
    for d in deviations:
        assert d.severity is None

    classified = classifier.classify_batch(deviations)

    # Returns the same list
    assert classified is deviations

    # Every deviation now has a severity set
    for d in classified:
        assert d.severity in ("Major", "Minor", "Administrative"), (
            f"Unexpected severity {d.severity!r} for {d.deviation_type}"
        )
        assert d.severity_source is not None


# ---------------------------------------------------------------------------
# Test 6: end-to-end accuracy against ground truth in the CSV
# ---------------------------------------------------------------------------


def test_classify_batch_end_to_end(capsys):
    from src.data.loader import load_visits, load_protocol_rules
    from src.rules.aggregator import run_all_rules
    from src.classifier.severity_classifier import SeverityClassifier

    visits = load_visits()
    protocol = load_protocol_rules()
    deviations = run_all_rules(visits, protocol)

    classifier = SeverityClassifier(backend="deterministic")  # keep test hermetic
    classified = classifier.classify_batch(deviations)

    # Build ground truth lookup
    gt_lookup = {}
    for r in visits.itertuples():
        if r.Deviation_Severity and r.Deviation_Severity != "None":
            gt_lookup[(r.Patient_ID, r.Visit_ID)] = r.Deviation_Severity

    correct = 0
    total = 0
    mismatches = []
    for d in classified:
        key = (d.patient_id, d.visit_id)
        if key in gt_lookup:
            total += 1
            if d.severity == gt_lookup[key]:
                correct += 1
            else:
                mismatches.append((key, d.severity, gt_lookup[key]))

    accuracy = correct / total if total else 0
    print(f"\n=== SEVERITY CLASSIFIER ACCURACY (deterministic backend) ===")
    print(f"Backend active: {classifier.get_active_backend_name()}")
    print(f"Classified: {total} deviations")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.2%}")
    if mismatches:
        print(f"Mismatches: {mismatches[:5]}")
    assert accuracy >= 0.95, f"Accuracy {accuracy:.2%} below threshold"
