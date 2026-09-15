# Write the visit timing rule check module for TrialGuard.

Context files (read these first):
- @docs/architecture.md (section 4 step 3 defines this rule's logic)
- @src/models.py (the Deviation dataclass you must return instances of)
- @src/data/loader.py (use load_visits and get_protocol_visit_schedule)
- @src/data/trialguard_visit_records.csv (has ground-truth Deviation_Severity column for validation)

Create two files:

### FILE 1: src/rules/check_visit_timing.py

A module with:

```python
from src.models import Deviation
import pandas as pd

def check_visit_timing(
    visits_df: pd.DataFrame,
    visit_schedule: dict[str, tuple[int, int]],
) -> list[Deviation]:
    """
    Detect visits that fall outside their protocol-allowed window.

    Args:
        visits_df: output of load_visits() — one row per (patient, visit)
        visit_schedule: output of get_protocol_visit_schedule() — {"V1": (0, 1), ...}
                        where the tuple is (scheduled_day, window_days_plus_minus)

    Returns:
        List of Deviation objects, one per visit outside window.
        deviation_type = "Visit Timing"
        deviation_reason = human-readable, e.g.
            "Visit V2 occurred on day 24, 10 days from scheduled day 14 (allowed window ±3)"
    """
```

Rules:
- For each visit row, look up the (scheduled_day, window) tuple from visit_schedule[Visit_ID]
- Compute days_off = abs(Actual_Day_From_Enrollment - scheduled_day)
- If days_off > window, emit a Deviation
- Skip rows where Visit_Status != "Completed" (though in our dataset all 628 are completed, be defensive)
- Use Deviation.from_row() to construct — passes raw row into raw_data for traceability
- Include the days_off value in the deviation_reason string

Add a helper: get_visit_timing_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_site": {site_id: count, ...}, "by_visit": {"V1": count, "V2": count, ...}}

### FILE 2: tests/test_check_visit_timing.py

Pytest tests. This is where we prove the rule engine works using ground-truth validation:

```python
def test_finds_all_ground_truth_visit_timing_deviations():
    """
    Ground truth: the dataset contains rows where Deviation_Type == "Visit Timing".
    Our rule engine must detect a superset of these (may detect additional edge cases,
    but must not miss any).
    """
```

Required tests:
1. test_returns_list_of_deviation_objects — result is list, every element is a Deviation instance
2. test_deviation_type_is_visit_timing — every returned Deviation has deviation_type == "Visit Timing"
3. test_deviation_reason_contains_days_off — reason string mentions the days_off value
4. test_finds_all_ground_truth_visit_timing_deviations — for every visit row where the CSV's Deviation_Type == "Visit Timing", our engine must produce a Deviation with matching (Patient_ID, Visit_ID). Assert recall == 100%.
5. test_precision_on_visit_timing — of all deviations we return, at least 95% should match a ground-truth Visit Timing row. Print the actual precision.
6. test_summary_helper_shapes — get_visit_timing_summary returns the expected keys and counts

At the end of the test file, add this print block INSIDE a test called test_print_metrics that always passes but reports the numbers, so we see them in pytest -v output:

```python
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
```

Do NOT run the tests. Do NOT create any other files. Do NOT modify existing files. Just create these two.

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

Write the visit timing rule check module for TrialGuard.

Context files (read these first):
- @docs/architecture.md (section 4 step 3 defines this rule's logic)
- @src/models.py (the Deviation dataclass you must return instances of)
- @src/data/loader.py (use load_visits and get_protocol_visit_schedule)
- @src/data/trialguard_visit_records.csv (has ground-truth Deviation_Severity column for validation)

Create two files:

### FILE 1: src/rules/check_visit_timing.py

A module with:

```python
from src.models import Deviation
import pandas as pd

def check_visit_timing(
    visits_df: pd.DataFrame,
    visit_schedule: dict[str, tuple[int, int]],
) -> list[Deviation]:
    """
    Detect visits that fall outside their protocol-allowed window.

    Args:
        visits_df: output of load_visits() — one row per (patient, visit)
        visit_schedule: output of get_protocol_visit_schedule() — {"V1": (0, 1), ...}
                        where the tuple is (scheduled_day, window_days_plus_minus)

    Returns:
        List of Deviation objects, one per visit outside window.
        deviation_type = "Visit Timing"
        deviation_reason = human-readable, e.g.
            "Visit V2 occurred on day 24, 10 days from scheduled day 14 (allowed window ±3)"
    """
```

Rules:
- For each visit row, look up the (scheduled_day, window) tuple from visit_schedule[Visit_ID]
- Compute days_off = abs(Actual_Day_From_Enrollment - scheduled_day)
- If days_off > window, emit a Deviation
- Skip rows where Visit_Status != "Completed" (though in our dataset all 628 are completed, be defensive)
- Use Deviation.from_row() to construct — passes raw row into raw_data for traceability
- Include the days_off value in the deviation_reason string

Add a helper: get_visit_timing_summary(deviations: list[Deviation]) -> dict
Returns {"total": N, "by_site": {site_id: count, ...}, "by_visit": {"V1": count, "V2": count, ...}}

### FILE 2: tests/test_check_visit_timing.py

Pytest tests. This is where we prove the rule engine works using ground-truth validation:

```python
def test_finds_all_ground_truth_visit_timing_deviations():
    """
    Ground truth: the dataset contains rows where Deviation_Type == "Visit Timing".
    Our rule engine must detect a superset of these (may detect additional edge cases,
    but must not miss any).
    """
```

Required tests:
1. test_returns_list_of_deviation_objects — result is list, every element is a Deviation instance
2. test_deviation_type_is_visit_timing — every returned Deviation has deviation_type == "Visit Timing"
3. test_deviation_reason_contains_days_off — reason string mentions the days_off value
4. test_finds_all_ground_truth_visit_timing_deviations — for every visit row where the CSV's Deviation_Type == "Visit Timing", our engine must produce a Deviation with matching (Patient_ID, Visit_ID). Assert recall == 100%.
5. test_precision_on_visit_timing — of all deviations we return, at least 95% should match a ground-truth Visit Timing row. Print the actual precision.
6. test_summary_helper_shapes — get_visit_timing_summary returns the expected keys and counts

At the end of the test file, add this print block INSIDE a test called test_print_metrics that always passes but reports the numbers, so we see them in pytest -v output:

```python
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
```

Do NOT run the tests. Do NOT create any other files. Do NOT modify existing files. Just create these two.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file

Let me read the context files first before writing anything.

> 🔧 **read_file** — docs/architecture.md

> 🔧 **read_file** — src/models.py

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-

### 🤖 Assistant

> 🔧 called: read_file, read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/models.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/docs/architecture.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/loader.py

### 🤖 Assistant

> 🔧 called: read_file, list_files, list_files

Now let me read the CSV to understand its columns and a few sample rows:

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/tests

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src/rules

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/trialguard_visit_records.csv

### 🤖 Assistant

> 🔧 called: execute_command

Now I have everything I need. Let me check a few rows with actual deviations to understand the data shape, then I'll write both files:

> 🔧 **execute_command** — Select-String -Path "bob-ai-hackathon--Your-Team-Name-\src\data\trialguard_visit_records.csv" -Pattern "Visit Timing" | Select-Object -First 8 | ForEach-Object { $_.Line }

### 🤖 Assistant

> 🔧 called: update_todo_list

I have all I need. The columns are clear: `Actual_Day_From_Enrollment` is already an integer in the CSV, `Visit_ID` maps to `visit_schedule` keys, and `Scheduled_Day` / `Visit_Window_Days` are also present in the row (but the function parameter is the authoritative source). Now I'll write both files:

> 🔧 **update_todo_list** — 
[-] Write src/rules/check_visit_timing.py
[ ] Write tests/test_check_visit_timing.py


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Write src/rules/check_visit_timing.py
[-] Write tests/test_check_visit_timing.py


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Write src/rules/check_visit_timing.py
[x] Write tests/test_check_visit_timing.py


### 🤖 Assistant

Both files are created. Here's a summary of every design decision made:

---

### [`src/rules/check_visit_timing.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py)

**`check_visit_timing`**
- Iterates with [`itertuples`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py:44) (faster than `iterrows`, preserves named attribute access).
- Skips rows where `Visit_Status != "Completed"` defensively, and skips `Visit_ID` values not present in `visit_schedule` (future-proof against extra visit types).
- Wraps `int(row.Actual_Day_From_Enrollment)` in a try/except to silently skip malformed cells — the only realistic bad-data case.
- Calls [`Deviation.from_row(row._asdict(), ...)`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py:57) — `_asdict()` on a namedtuple produces the `dict` that `from_row` expects, and stores it in `raw_data` for full traceability.
- The `±` symbol in the `deviation_reason` is written as its Unicode escape `\u00b1` to avoid any encoding issues on Windows.

**`get_visit_timing_summary`**
- Uses `collections.defaultdict` to accumulate counts, then converts to plain `dict` for the returned value — no surprises for callers.

---

### [`tests/test_check_visit_timing.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_visit_timing.py)

All fixtures are `scope="module"` so the CSV is loaded once for the whole test session.

| Test | What it proves |
|---|---|
| `test_returns_list_of_deviation_objects` | Return type contract — `list[Deviation]` |
| `test_deviation_type_is_visit_timing` | Every element carries the correct `deviation_type` label |
| `test_deviation_reason_contains_days_off` | Recomputes `days_off` from `raw_data` and asserts it appears in the reason string |
| `test_finds_all_ground_truth_visit_timing_deviations` | **100% recall** — no ground-truth row may be missed |
| `test_precision_on_visit_timing` | **≥ 95% precision** — false-positive budget is tight |
| `test_summary_helper_shapes` | Checks all three keys, cross-validates `total == Σ(by_site) == Σ(by_visit)` |
| `test_print_metrics` | Exact block from the spec — always passes, prints full TP/FP/FN/P/R table |