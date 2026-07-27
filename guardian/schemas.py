from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Phase(str, Enum):
    IDEA = "IDEA"
    POC = "POC"
    PILOTO = "PILOTO"
    ESCALADO = "ESCALADO"


class ControlStatus(str, Enum):
    CUMPLE = "CUMPLE"
    NO_CUMPLE = "NO CUMPLE"
    DESCONOCIDO = "DESCONOCIDO"
    NO_APLICA = "NO APLICA"
    NO_CONCLUYENTE = "NO CONCLUYENTE"


class SupportLevel(str, Enum):
    AFIRMACION = "AFIRMACIÓN DEL SPONSOR"
    DOCUMENTO = "DOCUMENTO APORTADO"
    COHERENTE = "EVIDENCIA COHERENTE PENDIENTE DE VALIDACIÓN"
    VALIDADA = "VALIDADA POR RESPONSABLE IDENTIFICADO"
    AUSENTE = "SIN EVIDENCIA LOCALIZADA"


class ControlFinding(BaseModel):
    control_id: Literal["C1", "C2", "C3", "C4", "C5", "C6"]
    status: Literal["CUMPLE", "NO CUMPLE", "DESCONOCIDO", "NO APLICA"]
    support_level: Literal[
        "AFIRMACIÓN DEL SPONSOR",
        "DOCUMENTO APORTADO",
        "EVIDENCIA COHERENTE PENDIENTE DE VALIDACIÓN",
        "VALIDADA POR RESPONSABLE IDENTIFICADO",
        "SIN EVIDENCIA LOCALIZADA",
    ]
    literal_quote: str = Field(
        description="Un único fragmento continuo copiado carácter por carácter de la fuente, de máximo 350 caracteres, o [NO LOCALIZADO EN EL MATERIAL ANALIZADO]"
    )
    locator: str
    rationale: str
    missing_evidence: str
    evidence_owner: str
    rights_impact: bool = False


class FalsifiablePrediction(BaseModel):
    likely_failure_point: str
    observable_signal: str
    review_date_or_milestone: str
    condition_that_would_disprove_it: str


class EvaluationRun(BaseModel):
    controls: list[ControlFinding]
    committee_questions: list[str] = Field(min_length=6, max_length=10)
    prediction: FalsifiablePrediction


class VerifiedFinding(BaseModel):
    control_id: str
    status: str
    support_level: str
    literal_quote: str
    locator: str
    rationale: str
    missing_evidence: str
    evidence_owner: str
    rights_impact: bool
    quote_verified: bool
    verification_note: str


class CalibrationRow(BaseModel):
    control_id: str
    run_statuses: list[str]
    dominant_status: str
    agreement_count: int
    total_runs: int
    agreement_percentage: int


class ConsolidatedEvaluation(BaseModel):
    controls: list[VerifiedFinding]
    recommendation: str
    blocking_controls: list[str]
    conditions_to_change: list[str]
    committee_questions: list[str]
    question_validation_notes: list[str]
    prediction: FalsifiablePrediction
    run_count: int
    variability_notes: list[str]
    calibration_rows: list[CalibrationRow]
