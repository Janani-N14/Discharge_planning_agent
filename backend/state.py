from typing import TypedDict, List

class TimelineEvent(TypedDict):
    step: str
    status: str
    note: str

class DischargeState(TypedDict):
    patient_summary: str
    diagnoses: List[str]
    medications: List[str]
    social_factors: str

    clinical_ready: bool
    risk_score: float
    missing_tasks: List[str]
    discharge_safe: bool
    explanation: str
    timeline: List[TimelineEvent]
