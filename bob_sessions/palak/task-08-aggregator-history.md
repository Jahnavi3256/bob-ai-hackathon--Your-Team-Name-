# Write the deviation aggregator — the single entry point for the complete rule engine.

Context files:
- @docs/architecture.md (section 4 step 7)
- @src/models.py
- @src/rules/check_visit_timing.py
- @src/rules/check_dose.py
- @src/rules/check_prohibited_med.py
- @src/rules/check_missing_lab.py
- @src/data/loader.py

Create two files:

### FILE 1: src/rules/aggregator.py

```python
from src.models import Deviation
from src.data.loader import load_all, get_protocol_visit_schedule
from src.rules.check_visit_timing import check_visit_timing
from src.rules.check_dose import check_dose
from src.rules.check_prohibited_med import check_prohibited_med
from src.rules.check_missing_lab import check_missing_lab
import pandas as pd

def run_all_rules(
    visits_df: pd.DataFrame,
    protocol_df: pd.DataFrame,
) -> list[Deviation]:
    """
    Run all four rule checks against the visit records and return a unified list of deviations.

    Args:
        visits_df: from load_visits()
        protocol_df: from load_protocol_rules()

    Returns:
        Combined list of Deviation objects from all four rule modules.
        Order preserved: visit timing, dose, prohibited med, missing lab.
    """

def deviations_to_dataframe(deviations: list[Deviation]) -> pd.DataFrame:
    """
    Convert a list of Deviation objects to a pandas DataFrame.
    Columns: trial_id, site_id, patient_id, visit_id, deviation_type, deviation_reason, severity, severity_source
    Excludes raw_data (too verbose for tabular display).
    """

def run_engine() -> pd.DataFrame:
    """
    Convenience entrypoint: load data, run all rules, return deviations as DataFrame.
    Also prints a one-line summary: "Detected N deviations across M sites"
    """
```

### FILE 2: tests/test_aggregator.py

Pytest tests:

1. test_run_all_rules_returns_list_of_deviations
2. test_run_all_rules_covers_all_four_types — the deviation_type set should contain exactly {"Visit Timing", "Wrong Dose", "Prohibited Medication", "Missing Lab"}
3. test_deviations_to_dataframe_has_expected_columns
4. test_run_engine_returns_dataframe

5. test_end_to_end_metrics — THE BIG ONE. Load data, run engine, compare against ground truth for ALL deviation types combined:

```python
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
```

Do NOT run tests. Do NOT modify other files. Just create these two.

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

Write the deviation aggregator — the single entry point for the complete rule engine.

Context files:
- @docs/architecture.md (section 4 step 7)
- @src/models.py
- @src/rules/check_visit_timing.py
- @src/rules/check_dose.py
- @src/rules/check_prohibited_med.py
- @src/rules/check_missing_lab.py
- @src/data/loader.py

Create two files:

### FILE 1: src/rules/aggregator.py

```python
from src.models import Deviation
from src.data.loader import load_all, get_protocol_visit_schedule
from src.rules.check_visit_timing import check_visit_timing
from src.rules.check_dose import check_dose
from src.rules.check_prohibited_med import check_prohibited_med
from src.rules.check_missing_lab import check_missing_lab
import pandas as pd

def run_all_rules(
    visits_df: pd.DataFrame,
    protocol_df: pd.DataFrame,
) -> list[Deviation]:
    """
    Run all four rule checks against the visit records and return a unified list of deviations.

    Args:
        visits_df: from load_visits()
        protocol_df: from load_protocol_rules()

    Returns:
        Combined list of Deviation objects from all four rule modules.
        Order preserved: visit timing, dose, prohibited med, missing lab.
    """

def deviations_to_dataframe(deviations: list[Deviation]) -> pd.DataFrame:
    """
    Convert a list of Deviation objects to a pandas DataFrame.
    Columns: trial_id, site_id, patient_id, visit_id, deviation_type, deviation_reason, severity, severity_source
    Excludes raw_data (too verbose for tabular display).
    """

def run_engine() -> pd.DataFrame:
    """
    Convenience entrypoint: load data, run all rules, return deviations as DataFrame.
    Also prints a one-line summary: "Detected N deviations across M sites"
    """
```

### FILE 2: tests/test_aggregator.py

Pytest tests:

1. test_run_all_rules_returns_list_of_deviations
2. test_run_all_rules_covers_all_four_types — the deviation_type set should contain exactly {"Visit Timing", "Wrong Dose", "Prohibited Medication", "Missing Lab"}
3. test_deviations_to_dataframe_has_expected_columns
4. test_run_engine_returns_dataframe

5. test_end_to_end_metrics — THE BIG ONE. Load data, run engine, compare against ground truth for ALL deviation types combined:

```python
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

> 🔧 called: list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/models.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/loader.py

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_dose.py

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_missing_lab.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/check_prohibited_med.py

### 🤖 Assistant

> 🔧 called: list_files, read_file

Now let me check the existing tests directory and architecture doc:

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/tests

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/docs/architecture.md

### 🤖 Assistant

> 🔧 called: read_file

Now let me peek at an existing test file to match conventions:

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/tests/test_check_dose.py

### 🤖 Assistant

> 🔧 called: write_file

I have everything I need. Now I'll create both files:

> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/aggregator.py

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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


### 🤖 Assistant

Both files are created. Here's a breakdown of every decision made:

---

### [`src/rules/aggregator.py`](bob-ai-hackathon--Your-Team-Name-/src/rules/aggregator.py)

**`run_all_rules(visits_df, protocol_df)`**  
Calls [`get_protocol_visit_schedule()`](bob-ai-hackathon--Your-Team-Name-/src/data/loader.py:152) internally — the visit schedule is derived from `protocol_df` exactly as [`check_visit_timing`](bob-ai-hackathon--Your-Team-Name-/src/rules/check_visit_timing.py:17) expects, so callers only need to pass the two DataFrames from `load_visits()` / `load_protocol_rules()`. Results are concatenated in the documented order (timing → dose → prohibited med → missing lab) via simple list addition.

**`deviations_to_dataframe(deviations)`**  
Manually projects the eight documented columns rather than calling `dev.to_dict()` (which includes `raw_data`). Column order is fixed by the explicit `columns=` argument to `pd.DataFrame()`, so it's stable regardless of insertion order.

**`run_engine()`**  
Calls `load_all()` (which already prints its own load summary), then prints the required `"Detected N deviations across M sites"` summary. Returns the DataFrame from `deviations_to_dataframe`.

---

### [`tests/test_aggregator.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_aggregator.py)

| Test | What it checks |
|---|---|
| `test_run_all_rules_returns_list_of_deviations` | `isinstance(dev, Deviation)` for every element |
| `test_run_all_rules_covers_all_four_types` | `set ==` exact match against `{"Visit Timing", "Wrong Dose", "Prohibited Medication", "Missing Lab"}` |
| `test_deviations_to_dataframe_has_expected_columns` | Column list equality, `raw_data` absence, row count parity |
| `test_run_engine_returns_dataframe` | Non-empty DataFrame + `capsys` check for the summary line |
| `test_end_to_end_metrics` | Verbatim as specified — ground-truth alignment on `(Patient_ID, Visit_ID)`, `recall >= 0.95` assertion |

`module`-scoped fixtures are used (matching the pattern in [`test_check_dose.py`](bob-ai-hackathon--Your-Team-Name-/tests/test_check_dose.py:18)) so the CSV files are loaded once per test session rather than once per test.