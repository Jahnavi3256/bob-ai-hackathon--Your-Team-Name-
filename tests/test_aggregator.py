"""
Tests for src/rules/aggregator.py
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.models import Deviation


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def visits_df():
    from src.data.loader import load_visits
    return load_visits()


@pytest.fixture(scope="module")
def protocol_df():
    from src.data.loader import load_protocol_rules
    return load_protocol_rules()


@pytest.fixture(scope="module")
def all_deviations(visits_df, protocol_df):
    from src.rules.aggregator import run_all_rules
    return run_all_rules(visits_df, protocol_df)


# ---------------------------------------------------------------------------
# 1. Return type
# ---------------------------------------------------------------------------

def test_run_all_rules_returns_list_of_deviations(all_deviations):
    """run_all_rules must return a list and every element must be a Deviation."""
    assert isinstance(all_deviations, list)
    assert len(all_deviations) > 0, "Expected at least one detected deviation"
    for dev in all_deviations:
        assert isinstance(dev, Deviation), f"Expected Deviation, got {type(dev)}"


# ---------------------------------------------------------------------------
# 2. All four deviation types are present
# ---------------------------------------------------------------------------

def test_run_all_rules_covers_all_four_types(all_deviations):
    """The deviation_type set must contain exactly the four expected rule types."""
    found_types = {d.deviation_type for d in all_deviations}
    expected = {"Visit Timing", "Wrong Dose", "Prohibited Medication", "Missing Lab"}
    assert found_types == expected, (
        f"Expected deviation types {expected}, got {found_types}"
    )


# ---------------------------------------------------------------------------
# 3. DataFrame columns
# ---------------------------------------------------------------------------

def test_deviations_to_dataframe_has_expected_columns(all_deviations):
    """deviations_to_dataframe must return a DataFrame with exactly the documented columns."""
    from src.rules.aggregator import deviations_to_dataframe

    df = deviations_to_dataframe(all_deviations)

    assert isinstance(df, pd.DataFrame)
    expected_columns = [
        "trial_id",
        "site_id",
        "patient_id",
        "visit_id",
        "deviation_type",
        "deviation_reason",
        "severity",
        "severity_source",
    ]
    assert list(df.columns) == expected_columns, (
        f"Column mismatch.\nExpected: {expected_columns}\nGot:      {list(df.columns)}"
    )
    # raw_data must NOT be present
    assert "raw_data" not in df.columns, "raw_data should be excluded from the tabular output"
    assert len(df) == len(all_deviations)


# ---------------------------------------------------------------------------
# 4. run_engine returns a DataFrame
# ---------------------------------------------------------------------------

def test_run_engine_returns_dataframe(capsys):
    """run_engine must return a non-empty DataFrame and print the summary line."""
    from src.rules.aggregator import run_engine

    df = run_engine()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0, "run_engine returned an empty DataFrame"

    captured = capsys.readouterr()
    assert "Detected" in captured.out and "deviations across" in captured.out, (
        f"Expected summary line in stdout, got: {captured.out!r}"
    )


# ---------------------------------------------------------------------------
# 5. End-to-end metrics
# ---------------------------------------------------------------------------

def test_end_to_end_metrics(capsys):
    from src.data.loader import load_visits, load_protocol_rules
    from src.rules.aggregator import run_all_rules

    visits = load_visits()
    protocol = load_protocol_rules()
    detected = run_all_rules(visits, protocol)

    # Ground truth: any row where Deviation_Type is not "None" and not NaN
    gt_rows = visits[visits["Deviation_Type"].notna() & (visits["Deviation_Type"] != "None")]
    gt_set = set((r.Patient_ID, r.Visit_ID) for r in gt_rows.itertuples())

    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print(f"\n" + "=" * 60)
    print(f"=== TRIALGUARD RULE ENGINE — END-TO-END METRICS ===")
    print("=" * 60)
    print(f"Ground-truth deviations (all types): {len(gt_set)}")
    print(f"Detected by rule engine: {len(det_set)}")
    print(f"True positives: {len(true_positives)}")
    print(f"False positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1: {f1:.2%}")
    print("=" * 60)
    # Note: Documentation deviations are not rule-detectable (handled by LLM classifier)
    # so recall of ~96% (25/26) is the expected ceiling for the rule engine alone
    assert recall >= 0.95, f"Recall {recall:.2%} below expected 95% threshold"
