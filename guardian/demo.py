from guardian.schemas import ControlFinding, EvaluationRun, FalsifiablePrediction


def demo_run(source_text: str, business_owner: str) -> EvaluationRun:
    present_owner = bool(business_owner.strip())
    controls = []
    for control_id in ["C1", "C2", "C3", "C4", "C5", "C6"]:
        if control_id == "C1" and present_owner:
            status = "DESCONOCIDO"
            rationale = "Se informó un responsable, pero el modo demostración no puede validar su capacidad de decisión."
            missing = "Confirmación firmada de la responsabilidad sobre el resultado de negocio."
        else:
            status = "DESCONOCIDO"
            rationale = "El modo demostración no interpreta semánticamente el documento."
            missing = f"Evidencia verificable para cerrar {control_id}."
        controls.append(ControlFinding(
            control_id=control_id,
            status=status,
            support_level="SIN EVIDENCIA LOCALIZADA",
            literal_quote="[NO LOCALIZADO EN EL MATERIAL ANALIZADO]",
            locator="No localizado",
            rationale=rationale,
            missing_evidence=missing,
            evidence_owner="Sponsor de la iniciativa",
            rights_impact=False,
        ))
    return EvaluationRun(
        controls=controls,
        committee_questions=[
            "¿Quién responde personalmente por el resultado de negocio?",
            "¿Cuál es la línea base medida hoy?",
            "¿Qué documento acredita el derecho de uso de los datos?",
            "¿Qué ocurre cuando la IA y el operario discrepan?",
            "¿Qué riesgo sobre derechos requiere revisión especializada?",
            "¿Qué condición obliga a detener el proyecto?",
        ],
        prediction=FalsifiablePrediction(
            likely_failure_point="Ausencia de evidencia validada.",
            observable_signal="Los controles críticos continúan sin documento y responsable validador.",
            review_date_or_milestone="Antes del siguiente comité.",
            condition_that_would_disprove_it="Se aporta y valida la evidencia solicitada.",
        ),
    )

