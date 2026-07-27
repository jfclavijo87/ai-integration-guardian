from guardian.decision_engine import decide
from guardian.schemas import VerifiedFinding


def finding(control_id: str, status: str, rights_impact: bool = False) -> VerifiedFinding:
    return VerifiedFinding(
        control_id=control_id,
        status=status,
        support_level="SIN EVIDENCIA LOCALIZADA",
        literal_quote="[NO LOCALIZADO EN EL MATERIAL ANALIZADO]",
        locator="",
        rationale="",
        missing_evidence=f"Falta {control_id}",
        evidence_owner="Sponsor",
        rights_impact=rights_impact,
        quote_verified=False,
        verification_note="",
    )


def complete(statuses: dict[str, str]) -> list[VerifiedFinding]:
    return [finding(cid, statuses.get(cid, "CUMPLE")) for cid in ["C1", "C2", "C3", "C4", "C5", "C6"]]


def test_unknown_critical_is_not_decidable():
    recommendation, blocking, _ = decide("PILOTO", complete({"C3": "DESCONOCIDO"}))
    assert recommendation == "NO DECIDIBLE - FALTA EVIDENCIA"
    assert blocking == ["C3"]


def test_c2_failure_stops_project():
    recommendation, blocking, _ = decide("PILOTO", complete({"C2": "NO CUMPLE"}))
    assert recommendation == "NO CONTINUAR"
    assert blocking == ["C2"]


def test_rights_impact_requires_specialist():
    controls = complete({})
    controls[4] = finding("C5", "NO CUMPLE", rights_impact=True)
    recommendation, _, _ = decide("PILOTO", controls)
    assert recommendation == "REVISIÓN ESPECIALIZADA"


def test_blocking_control_never_reports_no_condition():
    controls = complete({"C4": "DESCONOCIDO"})
    controls[3].missing_evidence = "Ninguna"
    recommendation, _, conditions = decide("PILOTO", controls)
    assert recommendation == "NO DECIDIBLE - FALTA EVIDENCIA"
    assert conditions == ["Aportar evidencia verificable y validada para cerrar C4."]


def test_absence_marker_never_becomes_a_condition():
    controls = complete({"C4": "DESCONOCIDO"})
    controls[3].missing_evidence = "[NO LOCALIZADO EN EL MATERIAL ANALIZADO]"
    _, _, conditions = decide("PILOTO", controls)
    assert conditions == ["Aportar evidencia verificable y validada para cerrar C4."]


def test_punctuated_none_never_becomes_a_condition():
    controls = complete({"C4": "DESCONOCIDO"})
    controls[3].missing_evidence = "Ninguna."
    _, _, conditions = decide("PILOTO", controls)
    assert conditions == ["Aportar evidencia verificable y validada para cerrar C4."]
