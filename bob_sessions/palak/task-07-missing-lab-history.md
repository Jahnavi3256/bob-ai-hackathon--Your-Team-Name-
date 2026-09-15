# Write the missing lab rule check for TrialGuard — the fourth and final rule.

Context files:
- @docs/architecture.md (section 4 step 6)
- @src/models.py
- @src/rules/check_prohibited_med.py (follow this pattern)
- @tests/test_check_prohibited_med.py (mirror this test structure)
- @src/data/loader.py

Create two files:

### FILE 1: src/rules/check_missing_lab.py

```python
def check_missing_lab(visits_df: pd.DataFrame) -> list[Deviation]:
    """
    Detect visits where a required lab was not completed.

    Per TG-101, CBC and Chemistry Panel are required at V2 and V4 only (not V1 or V3).
    The visit records have:
    - CBC_Required: True | False | None
    - CBC_Completed: "Yes" | "No" | "Not Required"
    - Chemistry_Panel_Required: True | False | None
    - Chemistry_Panel_Completed: "Yes" | "No" | "Not Required"

    A missing-lab deviation occurs when:
    - CBC_Required is True AND CBC_Completed != "Yes"
    OR
    - Chemistry_Panel_Required is True AND Chemistry_Panel_Completed != "Yes"

    Returns:
        List of Deviation objects with:
        - deviation_type = "Missing Lab"
        - deviation_reason = e.g. "Required CBC was not recorded at V2." or
                            "Required Chemistry Panel was not recorded at V4." or
                            "Required CBC and Chemistry Panel were not recorded at V2." (if both missing)
    """
```

Rules:
- Skip rows where Visit_Status != "Completed"
- Handle NaN / None in required/completed columns gracefully
- If BOTH labs are missing at the same visit, emit ONE Deviation (not two) with a combined reason
- Use Deviation.from_row()

Add helper: get_missing_lab_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_lab": {"CBC": count, "Chemistry Panel": count, "Both": count}, "by_site": {site_id: count}}

### FILE 2: tests/test_check_missing_lab.py

Mirror tests/test_check_prohibited_med.py:

1. test_returns_list_of_deviation_objects
2. test_deviation_type_is_missing_lab
3. test_deviation_reason_mentions_lab_name
4. test_finds_all_ground_truth_missing_lab_deviations — recall must be 100% against ground truth where Deviation_Type == "Missing Laboratory"
5. test_precision_on_missing_lab — precision must be >= 95%
6. test_summary_helper_shapes
7. test_print_metrics — SAME structure, but for "Missing Laboratory":

```python
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
```

Do NOT run tests. Do NOT modify other files. Just create these two.

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

Write the missing lab rule check for TrialGuard — the fourth and final rule.

Context files:
- @docs/architecture.md (section 4 step 6)
- @src/models.py
- @src/rules/check_prohibited_med.py (follow this pattern)
- @tests/test_check_prohibited_med.py (mirror this test structure)
- @src/data/loader.py

Create two files:

### FILE 1: src/rules/check_missing_lab.py

```python
def check_missing_lab(visits_df: pd.DataFrame) -> list[Deviation]:
    """
    Detect visits where a required lab was not completed.

    Per TG-101, CBC and Chemistry Panel are required at V2 and V4 only (not V1 or V3).
    The visit records have:
    - CBC_Required: True | False | None
    - CBC_Completed: "Yes" | "No" | "Not Required"
    - Chemistry_Panel_Required: True | False | None
    - Chemistry_Panel_Completed: "Yes" | "No" | "Not Required"

    A missing-lab deviation occurs when:
    - CBC_Required is True AND CBC_Completed != "Yes"
    OR
    - Chemistry_Panel_Required is True AND Chemistry_Panel_Completed != "Yes"

    Returns:
        List of Deviation objects with:
        - deviation_type = "Missing Lab"
        - deviation_reason = e.g. "Required CBC was not recorded at V2." or
                            "Required Chemistry Panel was not recorded at V4." or
                            "Required CBC and Chemistry Panel were not recorded at V2." (if both missing)
    """
```

Rules:
- Skip rows where Visit_Status != "Completed"
- Handle NaN / None in required/completed columns gracefully
- If BOTH labs are missing at the same visit, emit ONE Deviation (not two) with a combined reason
- Use Deviation.from_row()

Add helper: get_missing_lab_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_lab": {"CBC": count, "Chemistry Panel": count, "Both": count}, "by_site": {site_id: count}}

### FILE 2: tests/test_check_missing_lab.py

Mirror tests/test_check_prohibited_med.py:

1. test_returns_list_of_deviation_objects
2. test_deviation_type_is_missing_lab
3. test_deviation_reason_mentions_lab_name
4. test_finds_all_ground_truth_missing_lab_deviations — recall must be 100% against ground truth where Deviation_Type == "Missing Laboratory"
5. test_precision_on_missing_lab — precision must be >= 95%
6. test_summary_helper_shapes
7. test_print_metrics — SAME structure, but for "Missing Laboratory":

```python
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
```

Do NOT run tests. Do NOT modify other files. Just create these two.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file

Let me read the context files before writing anything.

> 🔧 **read_file** — docs/architecture.md

> 🔧 **read_file** — src/models.py

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: read_file, read_file

The project root is inside a subdirectory. Let me read all the reference files:

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/models.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_prohibited_med.py

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/tests/test_check_prohibited_med.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/loader.py

### 🤖 Assistant

> 🔧 called: write_file

I have everything I need. Now I'll create both files:

> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_missing_lab.py

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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


### 🤖 Assistant

Both files are created. Here's a summary of every decision made:

---

### [`src/rules/check_missing_lab.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_missing_lab.py)

**`check_missing_lab`** follows the exact same loop structure as [`check_prohibited_med`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_prohibited_med.py):

- `Visit_Status != "Completed"` rows are skipped first.
- `CBC_Required` and `Chemistry_Panel_Required` are already coerced to `True | False | None` by [`loader._coerce_bool()`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py:38) — so the `is True` guard handles `None`/`False`/`NaN` gracefully without extra branching.
- `CBC_Completed` / `Chemistry_Panel_Completed` are raw strings (the loader does **not** coerce them) — they're safely stringified with a NaN guard before comparing to `"Yes"`.
- Both-missing case emits **one** `Deviation` with the combined reason; single-lab missing emits the appropriate single-lab reason. `Deviation.from_row()` is used throughout as required.

**`get_missing_lab_summary`** classifies each deviation's reason string into `"CBC"`, `"Chemistry Panel"`, or `"Both"` buckets and counts by site — checking `"CBC and Chemistry Panel"` before the individual names to avoid double-counting the combined case.

---

### [`tests/test_check_missing_lab.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_missing_lab.py)

Mirrors [`test_check_prohibited_med.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_prohibited_med.py) precisely:

| # | Test | Notes |
|---|------|-------|
| 1 | `test_returns_list_of_deviation_objects` | Type + non-empty check |
| 2 | `test_deviation_type_is_missing_lab` | Label `"Missing Lab"` on every result |
| 3 | `test_deviation_reason_mentions_lab_name` | `"CBC"` or `"Chemistry Panel"` in reason |
| 4 | `test_finds_all_ground_truth_missing_lab_deviations` | 100% recall vs `Deviation_Type == "Missing Laboratory"` |
| 5 | `test_precision_on_missing_lab` | Precision ≥ 95% |
| 6 | `test_summary_helper_shapes` | Checks all three keys; validates `total == sum(by_lab) == sum(by_site)` |
| 7 | `test_print_metrics` | Exact structure from the spec, always passes |