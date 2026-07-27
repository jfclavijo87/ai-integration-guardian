from guardian.schemas import ControlFinding
from guardian.verifier import ABSENCE_MARKER, verify_finding


def test_missing_quote_downgrades_compliance():
    finding = ControlFinding(
        control_id="C1",
        status="CUMPLE",
        support_level="DOCUMENTO APORTADO",
        literal_quote="Una cita inventada",
        locator="Página 1",
        rationale="",
        missing_evidence="Nombramiento",
        evidence_owner="Dirección",
        rights_impact=False,
    )
    verified = verify_finding(finding, "Este es el texto real.")
    assert verified.status == "DESCONOCIDO"
    assert verified.literal_quote == ABSENCE_MARKER
    assert not verified.quote_verified


def test_whitespace_normalization_accepts_literal_quote():
    finding = ControlFinding(
        control_id="C2",
        status="CUMPLE",
        support_level="VALIDADA POR RESPONSABLE IDENTIFICADO",
        literal_quote="La tasa actual es 4 %.",
        locator="Página 2",
        rationale="",
        missing_evidence="",
        evidence_owner="Operaciones",
        rights_impact=False,
    )
    verified = verify_finding(finding, "La tasa actual   es 4 %.\n")
    assert verified.quote_verified


def test_unvalidated_support_cannot_close_control():
    finding = ControlFinding(
        control_id="C4",
        status="CUMPLE",
        support_level="DOCUMENTO APORTADO",
        literal_quote="El técnico conserva la decisión final.",
        locator="Página 2",
        rationale="",
        missing_evidence="Validación del responsable",
        evidence_owner="Operaciones",
        rights_impact=False,
    )
    verified = verify_finding(finding, "El técnico conserva la decisión final.")
    assert verified.status == "DESCONOCIDO"
    assert verified.quote_verified
    assert "rebajó" in verified.verification_note
