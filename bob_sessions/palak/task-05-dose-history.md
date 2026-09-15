# Write the dose check rule module for TrialGuard.

Context files:
- @docs/architecture.md (section 4 step 4 defines this rule)
- @src/models.py
- @src/rules/check_visit_timing.py (follow this exact pattern — same shape, same test structure)
- @tests/test_check_visit_timing.py (mirror this test style, including the metrics print block)
- @src/data/loader.py

Create two files following the exact pattern of the visit timing check:

### FILE 1: src/rules/check_dose.py

```python
def check_dose(visits_df: pd.DataFrame) -> list[Deviation]:
    """
    Detect visits where the administered dose differs from the protocol-specified dose.

    Per TG-101, the protocol dose is 100 mg (Protocol_Dose_mg column, uniform across all visits).
    Any row where Actual_Dose_mg != Protocol_Dose_mg is a deviation.

    Returns:
        List of Deviation objects with:
        - deviation_type = "Wrong Dose"
        - deviation_reason = e.g. "Administered dose was 150 mg; protocol-specified dose is 100 mg."
    """
```

Rules:
- Skip rows where Visit_Status != "Completed" (defensive)
- Handle NaN Actual_Dose_mg gracefully (skip, don't crash)
- Use Deviation.from_row() to construct
- Include actual dose AND protocol dose in the reason string

Add helper: get_dose_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_site": {site_id: count}, "unique_doses": [set of wrong doses observed]}

### FILE 2: tests/test_check_dose.py

Mirror tests/test_check_visit_timing.py exactly, but for dose:

1. test_returns_list_of_deviation_objects
2. test_deviation_type_is_wrong_dose
3. test_deviation_reason_contains_dose_value
4. test_finds_all_ground_truth_dose_deviations — recall must be 100% against ground truth where Deviation_Type == "Incorrect Dose"
5. test_precision_on_dose — precision must be >= 95%
6. test_summary_helper_shapes
7. test_print_metrics — SAME structure as visit timing's test_print_metrics, but for "Incorrect Dose":

```python
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
```

Do NOT run tests. Do NOT modify other files. Just create these two.

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

Write the dose check rule module for TrialGuard.

Context files:
- @docs/architecture.md (section 4 step 4 defines this rule)
- @src/models.py
- @src/rules/check_visit_timing.py (follow this exact pattern — same shape, same test structure)
- @tests/test_check_visit_timing.py (mirror this test style, including the metrics print block)
- @src/data/loader.py

Create two files following the exact pattern of the visit timing check:

### FILE 1: src/rules/check_dose.py

```python
def check_dose(visits_df: pd.DataFrame) -> list[Deviation]:
    """
    Detect visits where the administered dose differs from the protocol-specified dose.

    Per TG-101, the protocol dose is 100 mg (Protocol_Dose_mg column, uniform across all visits).
    Any row where Actual_Dose_mg != Protocol_Dose_mg is a deviation.

    Returns:
        List of Deviation objects with:
        - deviation_type = "Wrong Dose"
        - deviation_reason = e.g. "Administered dose was 150 mg; protocol-specified dose is 100 mg."
    """
```

Rules:
- Skip rows where Visit_Status != "Completed" (defensive)
- Handle NaN Actual_Dose_mg gracefully (skip, don't crash)
- Use Deviation.from_row() to construct
- Include actual dose AND protocol dose in the reason string

Add helper: get_dose_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_site": {site_id: count}, "unique_doses": [set of wrong doses observed]}

### FILE 2: tests/test_check_dose.py

Mirror tests/test_check_visit_timing.py exactly, but for dose:

1. test_returns_list_of_deviation_objects
2. test_deviation_type_is_wrong_dose
3. test_deviation_reason_contains_dose_value
4. test_finds_all_ground_truth_dose_deviations — recall must be 100% against ground truth where Deviation_Type == "Incorrect Dose"
5. test_precision_on_dose — precision must be >= 95%
6. test_summary_helper_shapes
7. test_print_metrics — SAME structure as visit timing's test_print_metrics, but for "Incorrect Dose":

```python
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
```

Do NOT run tests. Do NOT modify other files. Just create these two.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file

Let me read the reference files before writing anything.

> 🔧 **read_file** — src/rules/check_visit_timing.py

> 🔧 **read_file** — tests/test_check_visit_timing.py

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/tests

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src

### 🤖 Assistant

> 🔧 called: read_file, read_file

The project root is `bob-ai-hackathon--Your-Team-Name-/`. Let me read all the reference files.

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/tests/test_check_visit_timing.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py

### 🤖 Assistant

> 🔧 called: read_file, read_file

Now let me read the models and loader files:

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/models.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/loader.py

### 🤖 Assistant

> 🔧 called: execute_command

Now let me check the data to understand the dose columns:

> 🔧 **execute_command** — Get-Content "bob-ai-hackathon--Your-Team-Name-\src\data\trialguard_visit_records.csv" | Select-Object -First 3

### 🤖 Assistant

> 🔧 called: write_file

I have everything I need. Now I'll create both files:

> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_dose.py

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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


### 🤖 Assistant

Both files are created. Here's a summary of what was written and the key decisions made:

---

### [`src/rules/check_dose.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_dose.py)

Mirrors the exact shape of [`check_visit_timing.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py):

- **`check_dose(visits_df)`** — iterates with `itertuples`, guards on `Visit_Status == "Completed"`, skips rows where `Actual_Dose_mg` is `None` or `pd.isna()`, converts both dose columns to `float` (catches `ValueError`/`TypeError` on malformed values), flags any row where `actual_dose != protocol_dose`, and builds the reason string with both values using `:g` format (suppresses trailing `.0` for whole numbers, e.g. `"150 mg"` not `"150.0 mg"`).
- **`get_dose_summary(deviations)`** — returns `{"total": N, "by_site": {...}, "unique_doses": set(...)}`. The `unique_doses` set is populated from `raw_data["Actual_Dose_mg"]` stored on each `Deviation`.

---

### [`tests/test_check_dose.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_dose.py)

Exact structural mirror of [`test_check_visit_timing.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_visit_timing.py):

| # | Test | Notes |
|---|------|-------|
| 1 | `test_returns_list_of_deviation_objects` | checks list type + all `Deviation` instances |
| 2 | `test_deviation_type_is_wrong_dose` | asserts `"Wrong Dose"` label on every result |
| 3 | `test_deviation_reason_contains_dose_value` | verifies the actual dose value appears in the reason string |
| 4 | `test_finds_all_ground_truth_dose_deviations` | 100% recall against `Deviation_Type == "Incorrect Dose"` rows |
| 5 | `test_precision_on_dose` | precision ≥ 95% gate |
| 6 | `test_summary_helper_shapes` | checks all three keys, `total == sum(by_site)`, `unique_doses` non-empty |
| 7 | `test_print_metrics` | verbatim metrics block from the spec, `assert True` at end |