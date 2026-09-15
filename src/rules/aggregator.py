"""
TrialGuard Deviation Aggregator.

Single entry point for the complete rule engine: loads data, runs all four
rule checks, and returns a unified list of Deviation objects (or a DataFrame).
"""

from __future__ import annotations

import pandas as pd

from src.models import Deviation
from src.data.loader import load_all, get_protocol_visit_schedule
from src.rules.check_visit_timing import check_visit_timing
from src.rules.check_dose import check_dose
from src.rules.check_prohibited_med import check_prohibited_med
from src.rules.check_missing_lab import check_missing_lab


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
    visit_schedule = get_protocol_visit_schedule(protocol_df)

    timing_devs = check_visit_timing(visits_df, visit_schedule)
    dose_devs = check_dose(visits_df)
    med_devs = check_prohibited_med(visits_df)
    lab_devs = check_missing_lab(visits_df)

    return timing_devs + dose_devs + med_devs + lab_devs


def deviations_to_dataframe(deviations: list[Deviation]) -> pd.DataFrame:
    """
    Convert a list of Deviation objects to a pandas DataFrame.

    Columns: trial_id, site_id, patient_id, visit_id, deviation_type,
             deviation_reason, severity, severity_source
    Excludes raw_data (too verbose for tabular display).
    """
    rows = [
        {
            "trial_id": d.trial_id,
            "site_id": d.site_id,
            "patient_id": d.patient_id,
            "visit_id": d.visit_id,
            "deviation_type": d.deviation_type,
            "deviation_reason": d.deviation_reason,
            "severity": d.severity,
            "severity_source": d.severity_source,
        }
        for d in deviations
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "trial_id",
            "site_id",
            "patient_id",
            "visit_id",
            "deviation_type",
            "deviation_reason",
            "severity",
            "severity_source",
        ],
    )


def run_engine() -> pd.DataFrame:
    """
    Convenience entrypoint: load data, run all rules, return deviations as DataFrame.
    Also prints a one-line summary: "Detected N deviations across M sites"
    """
    data = load_all()
    deviations = run_all_rules(data["visits"], data["protocol"])
    df = deviations_to_dataframe(deviations)
    n_sites = df["site_id"].nunique() if not df.empty else 0
    print(f"Detected {len(deviations)} deviations across {n_sites} sites")
    return df
