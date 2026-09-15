"""
TrialGuard data models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Deviation:
    """Represents a single detected protocol deviation."""

    trial_id: str
    site_id: str
    patient_id: str
    visit_id: str
    deviation_type: str  # "Visit Timing" | "Wrong Dose" | "Prohibited Medication" | "Missing Lab" | "Documentation"
    deviation_reason: str  # Human-readable explanation
    severity: Optional[str] = None          # "Major" | "Minor" | "Administrative" — populated by classifier
    severity_source: Optional[str] = None  # "rule" | "llm"
    raw_data: Optional[dict] = field(default=None, repr=False)  # Original row dict for traceability

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a flat dict suitable for DataFrame construction."""
        return {
            "trial_id": self.trial_id,
            "site_id": self.site_id,
            "patient_id": self.patient_id,
            "visit_id": self.visit_id,
            "deviation_type": self.deviation_type,
            "deviation_reason": self.deviation_reason,
            "severity": self.severity,
            "severity_source": self.severity_source,
            "raw_data": self.raw_data,
        }

    @classmethod
    def from_row(
        cls,
        row: dict,
        deviation_type: str,
        deviation_reason: str,
    ) -> "Deviation":
        """Construct a Deviation from a visit record row dict.

        Expects the row to contain at least the keys:
        Trial_ID, Site_ID, Patient_ID, Visit_ID.
        """
        return cls(
            trial_id=row.get("Trial_ID", ""),
            site_id=row.get("Site_ID", ""),
            patient_id=row.get("Patient_ID", ""),
            visit_id=row.get("Visit_ID", ""),
            deviation_type=deviation_type,
            deviation_reason=deviation_reason,
            raw_data=dict(row),
        )
