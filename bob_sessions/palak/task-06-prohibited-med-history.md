# Write the prohibited medication rule check for TrialGuard.

Context files:
- @docs/architecture.md (section 4 step 5)
- @src/models.py
- @src/rules/check_visit_timing.py (follow this pattern)
- @src/rules/check_dose.py (follow this pattern)
- @tests/test_check_dose.py (mirror this test structure)
- @src/data/loader.py

Create two files following the exact pattern of check_dose.py:

### FILE 1: src/rules/check_prohibited_med.py

```python
def check_prohibited_med(visits_df: pd.DataFrame) -> list[Deviation]:
    """
    Detect visits where the protocol-prohibited Drug X was administered.

    Per TG-101, Drug X is prohibited for the duration of the trial.
    The visits_df Prohibited_Drug_X column is boolean (True = administered, False = not).

    Returns:
        List of Deviation objects with:
        - deviation_type = "Prohibited Medication"
        - deviation_reason = "Protocol-prohibited Drug X was recorded during visit {Visit_ID}."
    """
```

Rules:
- Skip rows where Visit_Status != "Completed"
- Handle NaN / None Prohibited_Drug_X gracefully (skip, don't crash — treat as not administered)
- Only flag when the value is truly True (be strict — False and None should NOT be flagged)
- Use Deviation.from_row()

Add helper: get_prohibited_med_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_site": {site_id: count}, "affected_patients": [unique patient IDs]}

### FILE 2: tests/test_check_prohibited_med.py

Mirror tests/test_check_dose.py exactly:

1. test_returns_list_of_deviation_objects
2. test_deviation_type_is_prohibited_medication
3. test_deviation_reason_mentions_drug_x
4. test_finds_all_ground_truth_prohibited_med_deviations — recall must be 100% against ground truth where Deviation_Type == "Prohibited Medication"
5. test_precision_on_prohibited_med — precision must be >= 95%
6. test_summary_helper_shapes
7. test_print_metrics — SAME structure as check_dose test_print_metrics, but for "Prohibited Medication":

```python
def test_print_metrics(capsys):
    from src.data.loader import load_visits
    from src.rules.check_prohibited_med import check_prohibited_med

    visits = load_visits()
    detected = check_prohibited_med(visits)

    gt_set = set(
        (r.Patient_ID, r.Visit_ID)
        for r in visits.itertuples()
        if r.Deviation_Type == "Prohibited Medication"
    )
    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0

    print(f"\n=== PROHIBITED MEDICATION RULE METRICS ===")
    print(f"Ground-truth Prohibited Medication deviations: {len(gt_set)}")
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

Write the prohibited medication rule check for TrialGuard.

Context files:
- @docs/architecture.md (section 4 step 5)
- @src/models.py
- @src/rules/check_visit_timing.py (follow this pattern)
- @src/rules/check_dose.py (follow this pattern)
- @tests/test_check_dose.py (mirror this test structure)
- @src/data/loader.py

Create two files following the exact pattern of check_dose.py:

### FILE 1: src/rules/check_prohibited_med.py

```python
def check_prohibited_med(visits_df: pd.DataFrame) -> list[Deviation]:
    """
    Detect visits where the protocol-prohibited Drug X was administered.

    Per TG-101, Drug X is prohibited for the duration of the trial.
    The visits_df Prohibited_Drug_X column is boolean (True = administered, False = not).

    Returns:
        List of Deviation objects with:
        - deviation_type = "Prohibited Medication"
        - deviation_reason = "Protocol-prohibited Drug X was recorded during visit {Visit_ID}."
    """
```

Rules:
- Skip rows where Visit_Status != "Completed"
- Handle NaN / None Prohibited_Drug_X gracefully (skip, don't crash — treat as not administered)
- Only flag when the value is truly True (be strict — False and None should NOT be flagged)
- Use Deviation.from_row()

Add helper: get_prohibited_med_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_site": {site_id: count}, "affected_patients": [unique patient IDs]}

### FILE 2: tests/test_check_prohibited_med.py

Mirror tests/test_check_dose.py exactly:

1. test_returns_list_of_deviation_objects
2. test_deviation_type_is_prohibited_medication
3. test_deviation_reason_mentions_drug_x
4. test_finds_all_ground_truth_prohibited_med_deviations — recall must be 100% against ground truth where Deviation_Type == "Prohibited Medication"
5. test_precision_on_prohibited_med — precision must be >= 95%
6. test_summary_helper_shapes
7. test_print_metrics — SAME structure as check_dose test_print_metrics, but for "Prohibited Medication":

```python
def test_print_metrics(capsys):
    from src.data.loader import load_visits
    from src.rules.check_prohibited_med import check_prohibited_med

    visits = load_visits()
    detected = check_prohibited_med(visits)

    gt_set = set(
        (r.Patient_ID, r.Visit_ID)
        for r in visits.itertuples()
        if r.Deviation_Type == "Prohibited Medication"
    )
    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0

    print(f"\n=== PROHIBITED MEDICATION RULE METRICS ===")
    print(f"Ground-truth Prohibited Medication deviations: {len(gt_set)}")
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

Let me read the context files first.

> 🔧 **read_file** — src/rules/check_dose.py

> 🔧 **read_file** — tests/test_check_dose.py

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: list_files

The project is under a subdirectory. Let me explore that.

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/tests

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/tests/test_check_dose.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_dose.py

### 🤖 Assistant

> 🔧 called: read_file, read_file

Now let me read the models and loader to understand `Deviation.from_row` and the data structure:

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/models.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/loader.py

### 🤖 Assistant

> 🔧 called: write_file

I have everything I need. Now I'll create both files:

> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_prohibited_med.py

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
Tests for src/rules/check_prohibited_med.py
"""

from __future__ import annotations

import pytest
import pandas as pd

from src.models import Deviation
from src.rules.check_prohibited_med import check_prohibited_med, get_prohibited_med_summary


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def visits_df():
    from src.data.loader import load_visits
    return load_visits()


@pytest.fixture(scope="module")
def detected(visits_df):
    return check_prohibited_med(visits_df)


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

def test_deviation_type_is_prohibited_medication(detected):
    """Every returned Deviation must carry deviation_type == 'Prohibited Medication'."""
    for dev in detected:
        assert dev.deviation_type == "Prohibited Medication", (
            f"Unexpected deviation_type '{dev.deviation_type}' for {dev.patient_id}/{dev.visit_id}"
        )


# ---------------------------------------------------------------------------
# 3. Reason string mentions Drug X
# ---------------------------------------------------------------------------

def test_deviation_reason_mentions_drug_x(detected):
    """The reason string must mention Drug X."""
    for dev in detected:
        assert "Drug X" in dev.deviation_reason, (
            f"Expected 'Drug X' in reason: {dev.deviation_reason!r}"
        )


# ---------------------------------------------------------------------------
# 4. Recall == 100 %: must detect every ground-truth Prohibited Medication row
# ---------------------------------------------------------------------------

def test_finds_all_ground_truth_prohibited_med_deviations(visits_df):
    """
    Ground truth: the dataset contains rows where Deviation_Type == "Prohibited Medication".
    Our rule engine must detect a superset of these (may detect additional edge cases,
    but must not miss any).
    """
    detected = check_prohibited_med(visits_df)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Prohibited Medication"
    }

    assert len(gt_set) > 0, "No ground-truth Prohibited Medication rows found — check CSV path"

    false_negatives = gt_set - det_set
    assert false_negatives == set(), (
        f"Rule engine missed {len(false_negatives)} ground-truth Prohibited Medication deviation(s):\n"
        + "\n".join(f"  Patient {p}, Visit {v}" for p, v in sorted(false_negatives))
    )


# ---------------------------------------------------------------------------
# 5. Precision >= 95 %
# ---------------------------------------------------------------------------

def test_precision_on_prohibited_med(visits_df):
    """At least 95% of detected Prohibited Medication deviations must match a ground-truth row."""
    detected = check_prohibited_med(visits_df)
    det_set = {(d.patient_id, d.visit_id) for d in detected}

    gt_set = {
        (r.Patient_ID, r.Visit_ID)
        for r in visits_df.itertuples()
        if str(getattr(r, "Deviation_Type", "")).strip() == "Prohibited Medication"
    }

    if not det_set:
        pytest.skip("No deviations detected; skipping precision check")

    true_positives = det_set & gt_set
    precision = len(true_positives) / len(det_set)

    print(f"\nProhibited Med Check precision: {precision:.2%} ({len(true_positives)}/{len(det_set)})")

    assert precision >= 0.95, (
        f"Precision {precision:.2%} is below the 95% threshold "
        f"({len(true_positives)} TPs, {len(det_set) - len(true_positives)} FPs)"
    )


# ---------------------------------------------------------------------------
# 6. Summary helper shape
# ---------------------------------------------------------------------------

def test_summary_helper_shapes(detected):
    """get_prohibited_med_summary must return the expected keys with correct counts."""
    summary = get_prohibited_med_summary(detected)

    assert "total" in summary
    assert "by_site" in summary
    assert "affected_patients" in summary

    assert isinstance(summary["total"], int)
    assert isinstance(summary["by_site"], dict)
    assert isinstance(summary["affected_patients"], list)

    # total must equal sum of by_site counts
    assert summary["total"] == sum(summary["by_site"].values()), (
        "summary['total'] does not match sum of by_site counts"
    )

    # affected_patients must be non-empty when deviations exist
    if detected:
        assert len(summary["affected_patients"]) > 0, (
            "Expected at least one affected patient"
        )


# ---------------------------------------------------------------------------
# Metrics print test — always passes, reports numbers in -v output
# ---------------------------------------------------------------------------

def test_print_metrics(capsys):
    from src.data.loader import load_visits
    from src.rules.check_prohibited_med import check_prohibited_med

    visits = load_visits()
    detected = check_prohibited_med(visits)

    gt_set = set(
        (r.Patient_ID, r.Visit_ID)
        for r in visits.itertuples()
        if r.Deviation_Type == "Prohibited Medication"
    )
    det_set = set((d.patient_id, d.visit_id) for d in detected)

    true_positives = gt_set & det_set
    false_positives = det_set - gt_set
    false_negatives = gt_set - det_set

    precision = len(true_positives) / len(det_set) if det_set else 0
    recall = len(true_positives) / len(gt_set) if gt_set else 0

    print(f"\n=== PROHIBITED MEDICATION RULE METRICS ===")
    print(f"Ground-truth Prohibited Medication deviations: {len(gt_set)}")
    print(f"Detected: {len(det_set)}")
    print(f"True positives: {len(true_positives)}")
    print(f"False positives: {len(false_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    assert True


### 🤖 Assistant

Both files are created. Here's a summary of what was written and why each decision was made:

---

### [`src/rules/check_prohibited_med.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_prohibited_med.py)

**`check_prohibited_med`** iterates with `itertuples` (matching [`check_dose.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_dose.py:31)) and applies three sequential guards:

1. **`Visit_Status != "Completed"` → skip** — same pattern as `check_dose`.
2. **NaN/None guard** — checks for `None` and `float` NaN explicitly. The loader's `_coerce_bool` maps unrecognised values to `None` and leaves missing cells as `None`, so both cases are covered without importing `math`.
3. **`drug_x_raw is not True` → skip** — uses identity (`is not True`) rather than a falsy check, so `False`, `None`, and any stray non-boolean objects are all skipped; only the Python singleton `True` passes. This satisfies "be strict" without risk of `1 == True` false-positives since the loader coerces to Python `bool`/`None`.

**`get_prohibited_med_summary`** returns `total`, `by_site` (matching the `check_dose` summary signature convention), and `affected_patients` as a sorted list of unique patient IDs per the spec.

---

### [`tests/test_check_prohibited_med.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_prohibited_med.py)

Mirrors [`test_check_dose.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_dose.py) exactly in structure — same `scope="module"` fixtures, same 7-test layout, same precision/recall assertions — substituting:
- `"Wrong Dose"` → `"Prohibited Medication"`
- `"Incorrect Dose"` → `"Prohibited Medication"` (the ground-truth `Deviation_Type` label used in the CSV)
- Summary key `unique_doses` → `affected_patients` (list, not set, matching the new helper's contract)
- The `test_print_metrics` body is verbatim from the spec.