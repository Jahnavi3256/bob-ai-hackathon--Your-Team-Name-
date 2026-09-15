"""
Tests for src/rules/check_dose.py
"""

from __future__ import annotations

import pytest
import pandas as pd

from src.models import Deviation
from src.rules.check_dose import check_dose, get_dose_summary


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def visits_df():
    from src.data.loader import load_visits
    return load_visits()


@pytest.fixture(scope="module")
def detected(visits_df):
    return check_dose(visits_df)


# ---------------------------------------------------------------------------
# 1. Return type
# ---------------------------------------------------------------------------

def test_returns_list_of_deviation_objects(detected):
    """Result must be a list and every element must be a Deviation instance."""
    assert isinstance(detected, list)
    assert len(detected) > 0, "Expected at least one detected deviation"
    for dev in detected:
        assert isinstance(dev, Deviation), f"Expected Deviation, got {type(dev)}"


# ---------------------------------------------------------------------------
# 2. Deviation type label
# ---------------------------------------------------------------------------

def test_deviation_type_is_wrong_dose(detected):
    """Every returned Deviation must carry deviation_type == 'Wrong Dose'."""
    for dev in detected:
        assert dev.deviation_type == "Wrong Dose", (
            f"Unexpected deviation_type '{dev.deviation_type}' for {dev.patient_id}/{dev.visit_id}"
        )


# ---------------------------------------------------------------------------
# 3. Reason string contains dose value
# ---------------------------------------------------------------------------

def test_deviation_reason_contains_dose_value(visits_df):
    """The reason string must mention the actual administered dose."""
    detected = check_dose(visits_df)
    for dev in detected:
        raw = dev.raw_data or {}
        try:
            actual_dose = float(raw.get("Actual_Dose_mg", ""))
        except (ValueError, TypeError):
            continue
        assert str(int(actual_dose)) in dev.deviation_reason or f"{actual_dose:g}" in dev.deviation_reason, (
            f"Expected dose value '{actual_dose:g}' in reason: {dev.deviation_reason!r}"
        )


# ---------------------------------------------------------------------------
# 4. Recall == 100 %: must detect every ground-truth Incorrect Dose row
# ---------------------------------------------------------------------------

def test_finds_all_ground_truth_dose_deviations(visits_df):
    """
    Ground truth: the dataset contains rows where Deviation_Type == "Incorrect Dose".
    Our rule engine must detect a superset of these (may detect additional edge cases,
    but must not miss any).
    """
    detected = check_dose(visits_df)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Incorrect Dose"
    }

    assert len(gt_set) > 0, "No ground-truth Incorrect Dose rows found — check CSV path"

    false_negatives = gt_set - det_set
    assert false_negatives == set(), (
        f"Rule engine missed {len(false_negatives)} ground-truth Incorrect Dose deviation(s):\n"
        + "\n".join(f"  Patient {p}, Visit {v}" for p, v in sorted(false_negatives))
    )


# ---------------------------------------------------------------------------
# 5. Precision >= 95 %
# ---------------------------------------------------------------------------

def test_precision_on_dose(visits_df):
    """At least 95% of detected Wrong Dose deviations must match a ground-truth row."""
    detected = check_dose(visits_df)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Incorrect Dose"
    }

    if not det_set:
        pytest.skip("No deviations detected; skipping precision check")

    true_positives = det_set & gt_set
    precision = len(true_positives) / len(det_set)

    print(f"\nDose Check precision: {precision:.2%} ({len(true_positives)}/{len(det_set)})")

    assert precision >= 0.95, (
        f"Precision {precision:.2%} is below the 95% threshold "
        f"({len(true_positives)} TPs, {len(det_set) - len(true_positives)} FPs)"
    )


# ---------------------------------------------------------------------------
# 6. Summary helper shape
# ---------------------------------------------------------------------------

def test_summary_helper_shapes(detected):
    """get_dose_summary must return the expected keys with correct counts."""
    summary = get_dose_summary(detected)

    assert "total" in summary
    assert "by_site" in summary
    assert "unique_doses" in summary

    assert isinstance(summary["total"], int)
    assert isinstance(summary["by_site"], dict)
    assert isinstance(summary["unique_doses"], set)

    # total must equal sum of by_site counts
    assert summary["total"] == sum(summary["by_site"].values()), (
        "summary['total'] does not match sum of by_site counts"
    )

    # unique_doses must be non-empty when deviations exist
    if detected:
        assert len(summary["unique_doses"]) > 0, (
            "Expected at least one unique wrong dose value"
        )


# ---------------------------------------------------------------------------
# Metrics print test — always passes, reports numbers in -v output
# ---------------------------------------------------------------------------

def test_print_metrics(capsys):
    from src.data.loader import load_visits
    from src.rules.check_dose import check_dose

    visits = load_visits()
    detected = check_dose(visits)

    gt_set = set(
        (r.Patient_ID, r.Visit_ID)
        for r in visits.itertuples()
        if r.Deviation_Type == "Incorrect Dose"
    )
    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0

    print(f"\n=== DOSE CHECK RULE METRICS ===")
    print(f"Ground-truth Incorrect Dose deviations: {len(gt_set)}")
    print(f"Detected: {len(det_set)}")
    print(f"True positives: {len(true_positives)}")
    print(f"False positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    assert True
