"""
Tests for src/rules/check_visit_timing.py
"""

from __future__ import annotations

import pytest
import pandas as pd

from src.models import Deviation
from src.rules.check_visit_timing import check_visit_timing, get_visit_timing_summary


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def visit_schedule():
    from src.data.loader import load_protocol_rules, get_protocol_visit_schedule
    return get_protocol_visit_schedule(load_protocol_rules())


@pytest.fixture(scope="module")
def visits_df():
    from src.data.loader import load_visits
    return load_visits()


@pytest.fixture(scope="module")
def detected(visits_df, visit_schedule):
    return check_visit_timing(visits_df, visit_schedule)


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

def test_deviation_type_is_visit_timing(detected):
    """Every returned Deviation must carry deviation_type == 'Visit Timing'."""
    for dev in detected:
        assert dev.deviation_type == "Visit Timing", (
            f"Unexpected deviation_type '{dev.deviation_type}' for {dev.patient_id}/{dev.visit_id}"
        )


# ---------------------------------------------------------------------------
# 3. Reason string contains days_off
# ---------------------------------------------------------------------------

def test_deviation_reason_contains_days_off(visits_df, visit_schedule):
    """The reason string must mention the numeric days_off value."""
    detected = check_visit_timing(visits_df, visit_schedule)
    for dev in detected:
        # Extract the raw actual_day and scheduled_day from raw_data
        raw = dev.raw_data or {}
        visit_id = dev.visit_id
        if visit_id not in visit_schedule:
            continue
        scheduled_day, window = visit_schedule[visit_id]
        actual_day = int(raw.get("Actual_Day_From_Enrollment", scheduled_day))
        days_off = abs(actual_day - scheduled_day)
        assert str(days_off) in dev.deviation_reason, (
            f"Expected '{days_off}' in reason: {dev.deviation_reason!r}"
        )


# ---------------------------------------------------------------------------
# 4. Recall == 100 %: must detect every ground-truth Visit Timing row
# ---------------------------------------------------------------------------

def test_finds_all_ground_truth_visit_timing_deviations(visits_df, visit_schedule):
    """
    Ground truth: the dataset contains rows where Deviation_Type == "Visit Timing".
    Our rule engine must detect a superset of these (may detect additional edge cases,
    but must not miss any).
    """
    detected = check_visit_timing(visits_df, visit_schedule)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Visit Timing"
    }

    assert len(gt_set) > 0, "No ground-truth Visit Timing rows found — check CSV path"

    false_negatives = gt_set - det_set
    assert false_negatives == set(), (
        f"Rule engine missed {len(false_negatives)} ground-truth Visit Timing deviation(s):\n"
        + "\n".join(f"  Patient {p}, Visit {v}" for p, v in sorted(false_negatives))
    )


# ---------------------------------------------------------------------------
# 5. Precision >= 95 %
# ---------------------------------------------------------------------------

def test_precision_on_visit_timing(visits_df, visit_schedule):
    """At least 95% of detected Visit Timing deviations must match a ground-truth row."""
    detected = check_visit_timing(visits_df, visit_schedule)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Visit Timing"
    }

    if not det_set:
        pytest.skip("No deviations detected; skipping precision check")

    true_positives = det_set & gt_set
    precision = len(true_positives) / len(det_set)

    print(f"\nVisit Timing precision: {precision:.2%} ({len(true_positives)}/{len(det_set)})")

    assert precision >= 0.95, (
        f"Precision {precision:.2%} is below the 95% threshold "
        f"({len(true_positives)} TPs, {len(det_set) - len(true_positives)} FPs)"
    )


# ---------------------------------------------------------------------------
# 6. Summary helper shape
# ---------------------------------------------------------------------------

def test_summary_helper_shapes(detected):
    """get_visit_timing_summary must return the expected keys with correct counts."""
    summary = get_visit_timing_summary(detected)

    assert "total" in summary
    assert "by_site" in summary
    assert "by_visit" in summary

    assert isinstance(summary["total"], int)
    assert isinstance(summary["by_site"], dict)
    assert isinstance(summary["by_visit"], dict)

    # total must equal sum of by_site counts
    assert summary["total"] == sum(summary["by_site"].values()), (
        "summary['total'] does not match sum of by_site counts"
    )

    # total must equal sum of by_visit counts
    assert summary["total"] == sum(summary["by_visit"].values()), (
        "summary['total'] does not match sum of by_visit counts"
    )

    # every key in by_visit should look like a visit ID
    for visit_id in summary["by_visit"]:
        assert visit_id.startswith("V"), f"Unexpected visit key: {visit_id!r}"


# ---------------------------------------------------------------------------
# Metrics print test — always passes, reports numbers in -v output
# ---------------------------------------------------------------------------

def test_print_metrics(capsys):
    from src.data.loader import load_visits, load_protocol_rules, get_protocol_visit_schedule
    from src.rules.check_visit_timing import check_visit_timing

    visits = load_visits()
    schedule = get_protocol_visit_schedule(load_protocol_rules())
    detected = check_visit_timing(visits, schedule)

    gt_set = set(
        (r.Patient_ID, r.Visit_ID)
        for r in visits.itertuples()
        if r.Deviation_Type == "Visit Timing"
    )
    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0

    print(f"\n=== VISIT TIMING RULE METRICS ===")
    print(f"Ground-truth Visit Timing deviations: {len(gt_set)}")
    print(f"Detected: {len(det_set)}")
    print(f"True positives: {len(true_positives)}")
    print(f"False positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    assert True  # metrics print regardless
