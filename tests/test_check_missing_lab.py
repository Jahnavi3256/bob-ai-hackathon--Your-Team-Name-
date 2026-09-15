"""
Tests for src/rules/check_missing_lab.py
"""

from __future__ import annotations

import pytest
import pandas as pd

from src.models import Deviation
from src.rules.check_missing_lab import check_missing_lab, get_missing_lab_summary


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def visits_df():
    from src.data.loader import load_visits
    return load_visits()


@pytest.fixture(scope="module")
def detected(visits_df):
    return check_missing_lab(visits_df)


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

def test_deviation_type_is_missing_lab(detected):
    """Every returned Deviation must carry deviation_type == 'Missing Lab'."""
    for dev in detected:
        assert dev.deviation_type == "Missing Lab", (
            f"Unexpected deviation_type '{dev.deviation_type}' for {dev.patient_id}/{dev.visit_id}"
        )


# ---------------------------------------------------------------------------
# 3. Reason string mentions lab name
# ---------------------------------------------------------------------------

def test_deviation_reason_mentions_lab_name(detected):
    """The reason string must mention 'CBC' or 'Chemistry Panel' (or both)."""
    for dev in detected:
        assert "CBC" in dev.deviation_reason or "Chemistry Panel" in dev.deviation_reason, (
            f"Expected 'CBC' or 'Chemistry Panel' in reason: {dev.deviation_reason!r}"
        )


# ---------------------------------------------------------------------------
# 4. Recall == 100 %: must detect every ground-truth Missing Laboratory row
# ---------------------------------------------------------------------------

def test_finds_all_ground_truth_missing_lab_deviations(visits_df):
    """
    Ground truth: the dataset contains rows where Deviation_Type == "Missing Laboratory".
    Our rule engine must detect a superset of these (may detect additional edge cases,
    but must not miss any).
    """
    detected = check_missing_lab(visits_df)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Missing Laboratory"
    }

    assert len(gt_set) > 0, "No ground-truth Missing Laboratory rows found — check CSV path"

    false_negatives = gt_set - det_set
    assert false_negatives == set(), (
        f"Rule engine missed {len(false_negatives)} ground-truth Missing Laboratory deviation(s):\n"
        + "\n".join(f"  Patient {p}, Visit {v}" for p, v in sorted(false_negatives))
    )


# ---------------------------------------------------------------------------
# 5. Precision >= 95 %
# ---------------------------------------------------------------------------

def test_precision_on_missing_lab(visits_df):
    """At least 95% of detected Missing Lab deviations must match a ground-truth row."""
    detected = check_missing_lab(visits_df)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Missing Laboratory"
    }

    if not det_set:
        pytest.skip("No deviations detected; skipping precision check")

    true_positives = det_set & gt_set
    precision = len(true_positives) / len(det_set)

    print(f"\nMissing Lab Check precision: {precision:.2%} ({len(true_positives)}/{len(det_set)})")

    assert precision >= 0.95, (
        f"Precision {precision:.2%} is below the 95% threshold "
        f"({len(true_positives)} TPs, {len(det_set) - len(true_positives)} FPs)"
    )


# ---------------------------------------------------------------------------
# 6. Summary helper shape
# ---------------------------------------------------------------------------

def test_summary_helper_shapes(detected):
    """get_missing_lab_summary must return the expected keys with correct counts."""
    summary = get_missing_lab_summary(detected)

    assert "total" in summary
    assert "by_lab" in summary
    assert "by_site" in summary

    assert isinstance(summary["total"], int)
    assert isinstance(summary["by_lab"], dict)
    assert isinstance(summary["by_site"], dict)

    # by_lab must contain exactly these three keys
    assert set(summary["by_lab"].keys()) == {"CBC", "Chemistry Panel", "Both"}, (
        f"Unexpected by_lab keys: {set(summary['by_lab'].keys())}"
    )

    # total must equal sum of by_lab counts
    assert summary["total"] == sum(summary["by_lab"].values()), (
        "summary['total'] does not match sum of by_lab counts"
    )

    # by_site counts must also sum to total
    assert summary["total"] == sum(summary["by_site"].values()), (
        "summary['total'] does not match sum of by_site counts"
    )

    # by_site must be non-empty when deviations exist
    if detected:
        assert len(summary["by_site"]) > 0, "Expected at least one site entry"


# ---------------------------------------------------------------------------
# Metrics print test — always passes, reports numbers in -v output
# ---------------------------------------------------------------------------

def test_print_metrics(capsys):
    from src.data.loader import load_visits
    from src.rules.check_missing_lab import check_missing_lab

    visits = load_visits()
    detected = check_missing_lab(visits)

    gt_set = set(
        (r.Patient_ID, r.Visit_ID)
        for r in visits.itertuples()
        if r.Deviation_Type == "Missing Laboratory"
    )
    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0

    print(f"\n=== MISSING LAB RULE METRICS ===")
    print(f"Ground-truth Missing Laboratory deviations: {len(gt_set)}")
    print(f"Detected: {len(det_set)}")
    print(f"True positives: {len(true_positives)}")
    print(f"False positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    assert True
