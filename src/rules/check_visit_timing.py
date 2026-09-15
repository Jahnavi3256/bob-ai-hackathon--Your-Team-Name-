"""
TrialGuard rule: Visit Timing Check.

Flags any visit where Actual_Day_From_Enrollment falls outside the
protocol-allowed window for that Visit_ID.
"""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from src.models import Deviation


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
    deviations: list[Deviation] = []

    for row in visits_df.itertuples(index=False):
        # Defensive: only evaluate completed visits
        if str(getattr(row, "Visit_Status", "")).strip() != "Completed":
            continue

        visit_id = str(row.Visit_ID).strip()

        # Skip visits not covered by the protocol schedule
        if visit_id not in visit_schedule:
            continue

        scheduled_day, window = visit_schedule[visit_id]

        try:
            actual_day = int(row.Actual_Day_From_Enrollment)
        except (ValueError, TypeError):
            continue

        days_off = abs(actual_day - scheduled_day)

        if days_off > window:
            reason = (
                f"Visit {visit_id} occurred on day {actual_day}, "
                f"{days_off} days from scheduled day {scheduled_day} "
                f"(allowed window \u00b1{window})"
            )
            deviations.append(
                Deviation.from_row(
                    row=row._asdict(),
                    deviation_type="Visit Timing",
                    deviation_reason=reason,
                )
            )

    return deviations


def get_visit_timing_summary(deviations: list[Deviation]) -> dict:
    """Return aggregate counts of Visit Timing deviations.

    Returns
    -------
    {
        "total": N,
        "by_site": {site_id: count, ...},
        "by_visit": {"V1": count, "V2": count, ...},
    }
    """
    by_site: dict[str, int] = defaultdict(int)
    by_visit: dict[str, int] = defaultdict(int)

    for dev in deviations:
        by_site[dev.site_id] += 1
        by_visit[dev.visit_id] += 1

    return {
        "total": len(deviations),
        "by_site": dict(by_site),
        "by_visit": dict(by_visit),
    }
