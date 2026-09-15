"""
TrialGuard rule: Dose Check.

Flags any completed visit where the administered dose differs from the
protocol-specified dose (Protocol_Dose_mg column, uniform across all visits).
"""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from src.models import Deviation


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
    deviations: list[Deviation] = []

    for row in visits_df.itertuples(index=False):
        # Defensive: only evaluate completed visits
        if str(getattr(row, "Visit_Status", "")).strip() != "Completed":
            continue

        # Skip rows where Actual_Dose_mg is NaN / missing
        actual_dose_raw = getattr(row, "Actual_Dose_mg", None)
        if actual_dose_raw is None or pd.isna(actual_dose_raw):
            continue

        try:
            actual_dose = float(actual_dose_raw)
            protocol_dose = float(row.Protocol_Dose_mg)
        except (ValueError, TypeError):
            continue

        if actual_dose != protocol_dose:
            reason = (
                f"Administered dose was {actual_dose:g} mg; "
                f"protocol-specified dose is {protocol_dose:g} mg."
            )
            deviations.append(
                Deviation.from_row(
                    row=row._asdict(),
                    deviation_type="Wrong Dose",
                    deviation_reason=reason,
                )
            )

    return deviations


def get_dose_summary(deviations: list[Deviation]) -> dict:
    """Return aggregate counts of Wrong Dose deviations.

    Returns
    -------
    {
        "total": N,
        "by_site": {site_id: count, ...},
        "unique_doses": [set of wrong actual doses observed],
    }
    """
    by_site: dict[str, int] = defaultdict(int)
    unique_doses: set[float] = set()

    for dev in deviations:
        by_site[dev.site_id] += 1
        raw = dev.raw_data or {}
        try:
            unique_doses.add(float(raw.get("Actual_Dose_mg", float("nan"))))
        except (ValueError, TypeError):
            pass

    return {
        "total": len(deviations),
        "by_site": dict(by_site),
        "unique_doses": unique_doses,
    }
