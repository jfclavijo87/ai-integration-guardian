from __future__ import annotations

from guardian.controls import CRITICALITY
from guardian.schemas import VerifiedFinding


def decide(phase: str, controls: list[VerifiedFinding]) -> tuple[str, list[str], list[str]]:
    by_id = {control.control_id: control for control in controls}
    c5 = by_id.get("C5")
    if c5 and c5.status == "NO CUMPLE" and c5.rights_impact:
        return "REVISIÓN ESPECIALIZADA", ["C5"], [_condition_for(c5)]

    critical_ids = [control_id for control_id, level in CRITICALITY[phase].items() if level == "CRÍTICO"]
    failing = [control_id for control_id in critical_ids if by_id[control_id].status == "NO CUMPLE"]
    unknown = [control_id for control_id in critical_ids if by_id[control_id].status in {"DESCONOCIDO", "NO CONCLUYENTE"}]

    if failing:
        recommendation = "NO CONTINUAR" if "C2" in failing else "REFORMULAR"
        return recommendation, failing, [_condition_for(by_id[x]) for x in failing]
    if unknown:
        return "NO DECIDIBLE - FALTA EVIDENCIA", unknown, [_condition_for(by_id[x]) for x in unknown]

    next_step = {
        "IDEA": "AVANZAR A DESCUBRIMIENTO",
        "POC": "AVANZAR A POC",
        "PILOTO": "AVANZAR A PILOTO CONDICIONADO",
        "ESCALADO": "AVANZAR A ESCALADO",
    }[phase]
    conditions = [c.missing_evidence for c in controls if c.status != "CUMPLE" and c.missing_evidence]
    return next_step, [], conditions


def _condition_for(control: VerifiedFinding) -> str:
    missing = control.missing_evidence.strip()
    invalid_conditions = {
        "ninguna",
        "ninguno",
        "no aplica",
        "n/a",
        "[no localizado en el material analizado]",
    }
    normalized_missing = missing.casefold().strip(" .;:")
    if not missing or normalized_missing in invalid_conditions:
        return f"Aportar evidencia verificable y validada para cerrar {control.control_id}."
    return missing
