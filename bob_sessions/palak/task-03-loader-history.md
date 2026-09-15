# Write the foundation data models and CSV loader for TrialGuard.

Context files (read these first):
- @docs/architecture.md (sections 3 and 4 define the loader and Deviation schema)
- @src/data/trialguard_visit_records.csv (visit schema)
- @src/data/trialguard_patient_screening.csv (screening schema)
- @src/data/trialguard_protocol_rules.csv (protocol rules schema)

Create these three files:

### FILE 1: src/models.py

A single Deviation dataclass (use @dataclass from dataclasses):

Fields:
- trial_id: str
- site_id: str
- patient_id: str
- visit_id: str
- deviation_type: str  (one of: "Visit Timing", "Wrong Dose", "Prohibited Medication", "Missing Lab", "Documentation")
- deviation_reason: str  (human-readable explanation, e.g. "Visit occurred 10 days from scheduled day 14")
- severity: str | None = None  (populated later by the classifier: "Major", "Minor", "Administrative")
- severity_source: str | None = None  (either "rule" or "llm")
- raw_data: dict | None = None  (the original row dict for traceability)

Add a to_dict() method returning a flat dict suitable for DataFrame construction.
Add a from_row(row: dict, deviation_type: str, deviation_reason: str) classmethod that constructs a Deviation from a visit record row.

### FILE 2: src/data/loader.py

A module with these functions:

- load_visits(path: str = "src/data/trialguard_visit_records.csv") -> pd.DataFrame
- load_screening(path: str = "src/data/trialguard_patient_screening.csv") -> pd.DataFrame
- load_protocol_rules(path: str = "src/data/trialguard_protocol_rules.csv") -> pd.DataFrame
- load_all() -> dict  returning {"visits": df, "screening": df, "protocol": df}

Requirements:
- Parse date columns as pd.Timestamp: Scheduled_Date, Actual_Date in visits; Screening_Date, Enrollment_Date, Admission_Date, Discharge_Date in screening
- Parse Yes/No columns (Prohibited_Drug_X, CBC_Required, Chemistry_Panel_Required, Smoker, Diabetic) as booleans
- Handle missing/empty strings gracefully (screen-failure patients have empty Enrollment_Date)
- Print a one-line summary when load_all() completes: how many visits, patients, sites, and enrolled patients were loaded
- Add a helper function get_protocol_visit_schedule(protocol_df: pd.DataFrame) -> dict that returns {"V1": (0, 1), "V2": (14, 3), "V3": (28, 3), "V4": (56, 5)} parsed from the Visit rule rows

### FILE 3: tests/test_loader.py

Pytest tests:
- test_load_visits_row_count: expects exactly 628 rows
- test_load_screening_row_count: expects exactly 500 rows
- test_load_protocol_rules_row_count: expects exactly 13 rows
- test_load_all_returns_all_three_frames
- test_enrollment_date_is_datetime_or_nat  (some are empty for screen failures)
- test_prohibited_drug_x_is_boolean
- test_get_protocol_visit_schedule returns the correct 4-visit dict
- test_deviation_dataclass_to_dict_roundtrip: create a Deviation, call to_dict(), verify all fields present

Also create requirements.txt at the project root with:
pandas>=2.0
pytest>=7.0
python-dotenv>=1.0
streamlit>=1.28
ibm-watsonx-ai>=1.0

Do NOT run the tests. Do NOT create any other files. Do NOT modify existing files. Just create these 4 files and I will run the tests myself.

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

Write the foundation data models and CSV loader for TrialGuard.

Context files (read these first):
- @docs/architecture.md (sections 3 and 4 define the loader and Deviation schema)
- @src/data/trialguard_visit_records.csv (visit schema)
- @src/data/trialguard_patient_screening.csv (screening schema)
- @src/data/trialguard_protocol_rules.csv (protocol rules schema)

Create these three files:

### FILE 1: src/models.py

A single Deviation dataclass (use @dataclass from dataclasses):

Fields:
- trial_id: str
- site_id: str
- patient_id: str
- visit_id: str
- deviation_type: str  (one of: "Visit Timing", "Wrong Dose", "Prohibited Medication", "Missing Lab", "Documentation")
- deviation_reason: str  (human-readable explanation, e.g. "Visit occurred 10 days from scheduled day 14")
- severity: str | None = None  (populated later by the classifier: "Major", "Minor", "Administrative")
- severity_source: str | None = None  (either "rule" or "llm")
- raw_data: dict | None = None  (the original row dict for traceability)

Add a to_dict() method returning a flat dict suitable for DataFrame construction.
Add a from_row(row: dict, deviation_type: str, deviation_reason: str) classmethod that constructs a Deviation from a visit record row.

### FILE 2: src/data/loader.py

A module with these functions:

- load_visits(path: str = "src/data/trialguard_visit_records.csv") -> pd.DataFrame
- load_screening(path: str = "src/data/trialguard_patient_screening.csv") -> pd.DataFrame
- load_protocol_rules(path: str = "src/data/trialguard_protocol_rules.csv") -> pd.DataFrame
- load_all() -> dict  returning {"visits": df, "screening": df, "protocol": df}

Requirements:
- Parse date columns as pd.Timestamp: Scheduled_Date, Actual_Date in visits; Screening_Date, Enrollment_Date, Admission_Date, Discharge_Date in screening
- Parse Yes/No columns (Prohibited_Drug_X, CBC_Required, Chemistry_Panel_Required, Smoker, Diabetic) as booleans
- Handle missing/empty strings gracefully (screen-failure patients have empty Enrollment_Date)
- Print a one-line summary when load_all() completes: how many visits, patients, sites, and enrolled patients were loaded
- Add a helper function get_protocol_visit_schedule(protocol_df: pd.DataFrame) -> dict that returns {"V1": (0, 1), "V2": (14, 3), "V3": (28, 3), "V4": (56, 5)} parsed from the Visit rule rows

### FILE 3: tests/test_loader.py

Pytest tests:
- test_load_visits_row_count: expects exactly 628 rows
- test_load_screening_row_count: expects exactly 500 rows
- test_load_protocol_rules_row_count: expects exactly 13 rows
- test_load_all_returns_all_three_frames
- test_enrollment_date_is_datetime_or_nat  (some are empty for screen failures)
- test_prohibited_drug_x_is_boolean
- test_get_protocol_visit_schedule returns the correct 4-visit dict
- test_deviation_dataclass_to_dict_roundtrip: create a Deviation, call to_dict(), verify all fields present

Also create requirements.txt at the project root with:
pandas>=2.0
pytest>=7.0
python-dotenv>=1.0
streamlit>=1.28
ibm-watsonx-ai>=1.0

Do NOT run the tests. Do NOT create any other files. Do NOT modify existing files. Just create these 4 files and I will run the tests myself.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file

Let me read the context files first.

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/docs/architecture.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/trialguard_visit_records.csv

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/trialguard_protocol_rules.csv

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/trialguard_patient_screening.csv

### 🤖 Assistant

> 🔧 called: update_todo_list

Now I have a clear picture of all schemas. Let me create the four files.

> 🔧 **update_todo_list** — 
[-] Create src/models.py — Deviation dataclass
[ ] Create src/data/loader.py — CSV loader functions
[ ] Create tests/test_loader.py — pytest tests
[ ] Create requirements.txt — project dependencies


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/src/models.py

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create src/models.py — Deviation dataclass
[-] Create src/data/loader.py — CSV loader functions
[ ] Create tests/test_loader.py — pytest tests
[ ] Create requirements.txt — project dependencies


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
TrialGuard CSV data loader.

Reads the three source CSVs into Pandas DataFrames and performs
lightweight type normalisation (date parsing, boolean coercion).
"""

from __future__ import annotations

import re
from typing import Dict

import pandas as pd


# ---------------------------------------------------------------------------
# Default file paths
# ---------------------------------------------------------------------------

_VISITS_PATH = "src/data/trialguard_visit_records.csv"
_SCREENING_PATH = "src/data/trialguard_patient_screening.csv"
_PROTOCOL_PATH = "src/data/trialguard_protocol_rules.csv"

# ---------------------------------------------------------------------------
# Boolean helpers
# ---------------------------------------------------------------------------

_YES_NO_MAP = {"yes": True, "no": False, "true": True, "false": False}


def _coerce_bool(series: pd.Series) -> pd.Series:
    """Convert a Yes/No (or True/False) text column to Python bool.

    Values that are not recognised (e.g. "Not Required") are left as *NaN*
    and the series dtype becomes object so callers must handle that if needed.
    Fully-missing (NaN) cells are also left as NaN.
    """
    return series.map(
        lambda v: _YES_NO_MAP.get(str(v).strip().lower(), None)
        if pd.notna(v)
        else None
    )


# ---------------------------------------------------------------------------
# Individual loaders
# ---------------------------------------------------------------------------


def load_visits(path: str = _VISITS_PATH) -> pd.DataFrame:
    """Load *trialguard_visit_records.csv* with typed columns.

    Date columns
    ------------
    ``Scheduled_Date``, ``Actual_Date`` → ``pd.Timestamp`` (``datetime64[ns]``)

    Boolean columns
    ---------------
    ``Prohibited_Drug_X``, ``CBC_Required``, ``Chemistry_Panel_Required``
    → ``bool`` where value is Yes/No; ``None`` where the field is "Not Required".
    """
    df = pd.read_csv(path, dtype=str)

    # Date columns
    for col in ("Scheduled_Date", "Actual_Date"):
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Boolean columns
    for col in ("Prohibited_Drug_X", "CBC_Required", "Chemistry_Panel_Required"):
        df[col] = _coerce_bool(df[col])

    return df


def load_screening(path: str = _SCREENING_PATH) -> pd.DataFrame:
    """Load *trialguard_patient_screening.csv* with typed columns.

    Date columns
    ------------
    ``Screening_Date``, ``Enrollment_Date``, ``Admission_Date``,
    ``Discharge_Date`` → ``pd.Timestamp``; screen-failure patients whose
    ``Enrollment_Date`` is empty become ``NaT``.

    Boolean columns
    ---------------
    ``Smoker``, ``Diabetic`` → ``bool`` (Yes/No).
    """
    df = pd.read_csv(path, dtype=str)

    # Replace empty strings with NaN so pd.to_datetime produces NaT correctly
    df.replace("", pd.NA, inplace=True)

    # Date columns
    for col in ("Screening_Date", "Enrollment_Date", "Admission_Date", "Discharge_Date"):
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Boolean columns
    for col in ("Smoker", "Diabetic"):
        df[col] = _coerce_bool(df[col])

    return df


def load_protocol_rules(path: str = _PROTOCOL_PATH) -> pd.DataFrame:
    """Load *trialguard_protocol_rules.csv* as a plain DataFrame."""
    return pd.read_csv(path, dtype=str)


# ---------------------------------------------------------------------------
# Composite loader
# ---------------------------------------------------------------------------


def load_all() -> Dict[str, pd.DataFrame]:
    """Load all three CSVs and return them in a single dict.

    Returns
    -------
    dict with keys ``"visits"``, ``"screening"``, and ``"protocol"``.

    Side-effect
    -----------
    Prints a one-line summary to stdout.
    """
    visits_df = load_visits()
    screening_df = load_screening()
    protocol_df = load_protocol_rules()

    n_visits = len(visits_df)
    n_patients = screening_df["Patient_ID"].nunique()
    n_sites = screening_df["Site_ID"].nunique()
    n_enrolled = screening_df["Enrollment_Date"].notna().sum()

    print(
        f"[TrialGuard] Loaded {n_visits} visits | "
        f"{n_patients} patients | "
        f"{n_sites} sites | "
        f"{n_enrolled} enrolled patients"
    )

    return {"visits": visits_df, "screening": screening_df, "protocol": protocol_df}


# ---------------------------------------------------------------------------
# Protocol visit-schedule helper
# ---------------------------------------------------------------------------

# Pattern: "Day <n> ±<w>" extracted from the Requirement column of Visit rows.
_WINDOW_RE = re.compile(r"Day\s+(\d+)\s*±\s*(\d+)", re.IGNORECASE)


def get_protocol_visit_schedule(protocol_df: pd.DataFrame) -> Dict[str, tuple]:
    """Parse Visit rows from *protocol_df* into a window dict.

    Returns
    -------
    ``{"V1": (scheduled_day, window), "V2": ..., "V3": ..., "V4": ...}``

    The values match the TG-101 specification::

        {"V1": (0, 1), "V2": (14, 3), "V3": (28, 3), "V4": (56, 5)}

    Only rows where ``Rule_Category == "Visit"`` are considered.
    Rows whose ``Requirement`` field does not match the expected pattern are
    silently skipped.
    """
    schedule: Dict[str, tuple] = {}
    visit_rows = protocol_df[protocol_df["Rule_Category"] == "Visit"]

    for _, row in visit_rows.iterrows():
        visit_id = str(row["Rule_Name"]).strip()
        requirement = str(row["Requirement"]).strip()
        match = _WINDOW_RE.search(requirement)
        if match:
            scheduled_day = int(match.group(1))
            window_days = int(match.group(2))
            schedule[visit_id] = (scheduled_day, window_days)

    return schedule


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create src/models.py — Deviation dataclass
[x] Create src/data/loader.py — CSV loader functions
[-] Create tests/test_loader.py — pytest tests
[ ] Create requirements.txt — project dependencies


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
Tests for src/data/loader.py and src/models.py.

Run with:
    pytest tests/test_loader.py -v
"""

from __future__ import annotations

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
        assert isinstance(val, bool), (
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


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create src/models.py — Deviation dataclass
[x] Create src/data/loader.py — CSV loader functions
[x] Create tests/test_loader.py — pytest tests
[-] Create requirements.txt — project dependencies


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — pandas>=2.0
pytest>=7.0
python-dotenv>=1.0
streamlit>=1.28
ibm-watsonx-ai>=1.0


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create src/models.py — Deviation dataclass
[x] Create src/data/loader.py — CSV loader functions
[x] Create tests/test_loader.py — pytest tests
[x] Create requirements.txt — project dependencies


### 🤖 Assistant

All four files are created. Here's a summary of what was built and the key design decisions:

---

### Files created

#### [`src/models.py`](bob-ai-hackathon--Your-Team-Name-/src/models.py)
- `@dataclass Deviation` with all nine fields as specified.
- [`to_dict()`](bob-ai-hackathon--Your-Team-Name-/src/models.py:35) returns a flat dict with snake_case keys matching the field names — ready for `pd.DataFrame([d.to_dict() for d in deviations])`.
- [`from_row()`](bob-ai-hackathon--Your-Team-Name-/src/models.py:44) is a `@classmethod` that reads `Trial_ID`, `Site_ID`, `Patient_ID`, `Visit_ID` from the raw visit row dict and stores the full row in `raw_data` for traceability.

#### [`src/data/loader.py`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py)
- [`load_visits()`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py:53) — parses `Scheduled_Date`/`Actual_Date` as `datetime64`; coerces `Prohibited_Drug_X`, `CBC_Required`, `Chemistry_Panel_Required` to `True`/`False`/`None` (cells like `"Not Required"` become `None`, not a crash).
- [`load_screening()`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py:76) — replaces empty strings with `pd.NA` before date parsing so screen-failure `Enrollment_Date` cells become `NaT` correctly; coerces `Smoker`/`Diabetic` to bool.
- [`load_all()`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py:106) — prints a one-line summary counting visits, patients, sites, and enrolled patients (those with a non-NaT `Enrollment_Date`).
- [`get_protocol_visit_schedule()`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py:148) — regex-parses `"Day N ±W"` from the `Requirement` column of Visit rows, returning `{"V1": (0,1), "V2": (14,3), "V3": (28,3), "V4": (56,5)}`.

#### [`tests/test_loader.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_loader.py)
Eight pytest tests covering all specified assertions. The `sys.path.insert` at the top ensures the project root is on the Python path regardless of where pytest is invoked from.

#### [`requirements.txt`](bob-ai-hackathon--Your-Team-Name-/requirements.txt)
All five pinned minimum versions as specified.

---

### 👤 User

The test test_prohibited_drug_x_is_boolean fails because pandas stores booleans as numpy.bool_, not Python bool. isinstance(False, bool) returns False when that value came from a pandas column. Fix the assertion to accept both Python bool and numpy.bool_ (use `import numpy as np` and check `isinstance(val, (bool, np.bool_))`). Only change that one test, nothing else.

---

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/tests/test_loader.py

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/tests/test_loader.py

### 🤖 Assistant

> 🔧 called: apply_diff



> 🔧 **apply_diff** — bob-ai-hackathon--Your-Team-Name-/tests/test_loader.py

### 🤖 Assistant

Two targeted changes:

1. **[`import numpy as np`](bob-ai-hackathon--Your-Team-Name-/tests/test_loader.py:11)** added alongside the existing imports.
2. **[`isinstance(val, (bool, np.bool_))`](bob-ai-hackathon--Your-Team-Name-/tests/test_loader.py:99)** — the tuple form accepts both Python's native `bool` and NumPy's `numpy.bool_`, which is what pandas stores in object-dtype columns after a `.map()` call.

Nothing else was touched.