"""
TrialGuard rule: Missing Lab Check.

Flags any completed visit where a required lab (CBC or Chemistry Panel)
was not recorded as completed.
"""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from src.models import Deviation


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
    deviations: list[Deviation] = []

    for row in visits_df.itertuples(index=False):
        # Only evaluate completed visits
        if str(getattr(row, "Visit_Status", "")).strip() != "Completed":
            continue

        visit_id = getattr(row, "Visit_ID", "")

        # --- CBC ---
        cbc_required = getattr(row, "CBC_Required", None)
        cbc_completed_raw = getattr(row, "CBC_Completed", None)
        # Treat NaN/None as not "Yes"
        cbc_completed = (
            str(cbc_completed_raw).strip()
            if cbc_completed_raw is not None and not (isinstance(cbc_completed_raw, float) and pd.isna(cbc_completed_raw))
            else ""
        )
        cbc_missing = (cbc_required is True) and (cbc_completed != "Yes")

        # --- Chemistry Panel ---
        chem_required = getattr(row, "Chemistry_Panel_Required", None)
        chem_completed_raw = getattr(row, "Chemistry_Panel_Completed", None)
        chem_completed = (
            str(chem_completed_raw).strip()
            if chem_completed_raw is not None and not (isinstance(chem_completed_raw, float) and pd.isna(chem_completed_raw))
            else ""
        )
        chem_missing = (chem_required is True) and (chem_completed != "Yes")

        if not cbc_missing and not chem_missing:
            continue

        # Build a single combined reason when both are missing
        if cbc_missing and chem_missing:
            reason = f"Required CBC and Chemistry Panel were not recorded at {visit_id}."
        elif cbc_missing:
            reason = f"Required CBC was not recorded at {visit_id}."
        else:
            reason = f"Required Chemistry Panel was not recorded at {visit_id}."

        deviations.append(
            Deviation.from_row(
                row=row._asdict(),
                deviation_type="Missing Lab",
                deviation_reason=reason,
            )
        )

    return deviations


def get_missing_lab_summary(deviations: list[Deviation]) -> dict:
    """Return aggregate counts of Missing Lab deviations.

    Returns
    -------
    {
        "total": N,
        "by_lab": {"CBC": count, "Chemistry Panel": count, "Both": count},
        "by_site": {site_id: count, ...},
    }
    """
    by_lab: dict[str, int] = {"CBC": 0, "Chemistry Panel": 0, "Both": 0}
    by_site: dict[str, int] = defaultdict(int)

    for dev in deviations:
        reason = dev.deviation_reason
        if "CBC and Chemistry Panel" in reason:
            by_lab["Both"] += 1
        elif "CBC" in reason:
            by_lab["CBC"] += 1
        elif "Chemistry Panel" in reason:
            by_lab["Chemistry Panel"] += 1

        by_site[dev.site_id] += 1

    return {
        "total": len(deviations),
        "by_lab": by_lab,
        "by_site": dict(by_site),
    }
