"""
TrialGuard rule: Prohibited Medication Check.

Flags any completed visit where protocol-prohibited Drug X was administered.
"""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from src.models import Deviation


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
    deviations: list[Deviation] = []

    for row in visits_df.itertuples(index=False):
        # Only evaluate completed visits
        if str(getattr(row, "Visit_Status", "")).strip() != "Completed":
            continue

        # Retrieve the Prohibited_Drug_X flag; skip if missing/NaN
        drug_x_raw = getattr(row, "Prohibited_Drug_X", None)
        if drug_x_raw is None or (isinstance(drug_x_raw, float) and pd.isna(drug_x_raw)):
            continue

        # Only flag when the value is strictly True
        if drug_x_raw is not True:
            continue

        visit_id = getattr(row, "Visit_ID", "")
        reason = f"Protocol-prohibited Drug X was recorded during visit {visit_id}."
        deviations.append(
            Deviation.from_row(
                row=row._asdict(),
                deviation_type="Prohibited Medication",
                deviation_reason=reason,
            )
        )

    return deviations


def get_prohibited_med_summary(deviations: list[Deviation]) -> dict:
    """Return aggregate counts of Prohibited Medication deviations.

    Returns
    -------
    {
        "total": N,
        "by_site": {site_id: count, ...},
        "affected_patients": [unique patient IDs],
    }
    """
    by_site: dict[str, int] = defaultdict(int)
    affected_patients: set[str] = set()

    for dev in deviations:
        by_site[dev.site_id] += 1
        affected_patients.add(dev.patient_id)

    return {
        "total": len(deviations),
        "by_site": dict(by_site),
        "affected_patients": sorted(affected_patients),
    }
