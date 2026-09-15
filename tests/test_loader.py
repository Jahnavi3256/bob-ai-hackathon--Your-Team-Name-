"""
Tests for src/data/loader.py and src/models.py.

Run with:
    pytest tests/test_loader.py -v
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Make sure the project root is importable when pytest is run from the root.
# ---------------------------------------------------------------------------
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.loader import (
    load_all,
    load_protocol_rules,
    load_screening,
    load_visits,
    get_protocol_visit_schedule,
)
from src.models import Deviation


# ---------------------------------------------------------------------------
# Row-count tests
# ---------------------------------------------------------------------------


def test_load_visits_row_count():
    df = load_visits()
    assert len(df) == 628, f"Expected 628 visit rows, got {len(df)}"


def test_load_screening_row_count():
    df = load_screening()
    assert len(df) == 500, f"Expected 500 screening rows, got {len(df)}"


def test_load_protocol_rules_row_count():
    df = load_protocol_rules()
    assert len(df) == 13, f"Expected 13 protocol rule rows, got {len(df)}"


# ---------------------------------------------------------------------------
# load_all completeness test
# ---------------------------------------------------------------------------


def test_load_all_returns_all_three_frames():
    data = load_all()
    assert set(data.keys()) == {"visits", "screening", "protocol"}
    for key, df in data.items():
        assert isinstance(df, pd.DataFrame), f"'{key}' is not a DataFrame"
        assert len(df) > 0, f"'{key}' DataFrame is empty"


# ---------------------------------------------------------------------------
# Type-coercion tests
# ---------------------------------------------------------------------------


def test_enrollment_date_is_datetime_or_nat():
    """Enrollment_Date must be datetime64 (pd.Timestamp or NaT).

    Screen-failure patients have an empty Enrollment_Date, which must become
    NaT rather than an empty string.
    """
    df = load_screening()
    col = df["Enrollment_Date"]
    # The column dtype should be datetime64
    assert pd.api.types.is_datetime64_any_dtype(col), (
        f"Enrollment_Date dtype is {col.dtype}, expected datetime64"
    )
    # At least some NaT values must exist (screen failures)
    assert col.isna().any(), (
        "Expected at least one NaT in Enrollment_Date for screen-failure patients"
    )
    # All non-null values must be Timestamps
    non_null = col.dropna()
    assert len(non_null) > 0, "No non-null Enrollment_Date values found"
    assert all(isinstance(v, pd.Timestamp) for v in non_null), (
        "Some non-null Enrollment_Date values are not pd.Timestamp"
    )


def test_prohibited_drug_x_is_boolean():
    """Prohibited_Drug_X must contain only True, False, or None (Not Required rows)."""
    df = load_visits()
    col = df["Prohibited_Drug_X"]
    non_null_values = col.dropna().unique()
    for val in non_null_values:
        assert isinstance(val, (bool, np.bool_)), (
            f"Prohibited_Drug_X contains non-boolean value: {val!r}"
        )


# ---------------------------------------------------------------------------
# Protocol visit schedule helper test
# ---------------------------------------------------------------------------


def test_get_protocol_visit_schedule_returns_correct_dict():
    """get_protocol_visit_schedule must return the four TG-101 visit windows."""
    protocol_df = load_protocol_rules()
    schedule = get_protocol_visit_schedule(protocol_df)

    expected = {"V1": (0, 1), "V2": (14, 3), "V3": (28, 3), "V4": (56, 5)}
    assert schedule == expected, (
        f"Visit schedule mismatch.\nExpected: {expected}\nGot:      {schedule}"
    )


# ---------------------------------------------------------------------------
# Deviation dataclass round-trip test
# ---------------------------------------------------------------------------


def test_deviation_dataclass_to_dict_roundtrip():
    """Create a Deviation, call to_dict(), and verify all fields are present."""
    raw = {
        "Trial_ID": "TG-101",
        "Site_ID": "S01",
        "Patient_ID": "P042",
        "Visit_ID": "V2",
        "Actual_Dose_mg": "75",
    }
    dev = Deviation.from_row(
        row=raw,
        deviation_type="Wrong Dose",
        deviation_reason="Administered 75 mg; protocol requires 100 mg",
    )

    # Assign optional fields to verify they round-trip correctly
    dev.severity = "Major"
    dev.severity_source = "rule"

    d = dev.to_dict()

    expected_keys = {
        "trial_id",
        "site_id",
        "patient_id",
        "visit_id",
        "deviation_type",
        "deviation_reason",
        "severity",
        "severity_source",
        "raw_data",
    }
    assert expected_keys == set(d.keys()), (
        f"to_dict() keys mismatch.\nExpected: {sorted(expected_keys)}\nGot: {sorted(d.keys())}"
    )

    assert d["trial_id"] == "TG-101"
    assert d["site_id"] == "S01"
    assert d["patient_id"] == "P042"
    assert d["visit_id"] == "V2"
    assert d["deviation_type"] == "Wrong Dose"
    assert d["deviation_reason"] == "Administered 75 mg; protocol requires 100 mg"
    assert d["severity"] == "Major"
    assert d["severity_source"] == "rule"
    assert d["raw_data"] == raw
