from __future__ import annotations

from datetime import datetime

from guardian.schemas import ConsolidatedEvaluation


def to_markdown(title: str, phase: str, requested_decision: str, result: ConsolidatedEvaluation, model: str) -> str:
    rows = []
    for c in result.controls:
        rows.append(f"| {c.control_id} | {c.status} | {c.support_level} | {c.literal_quote.replace('|', '/')} |")
    questions = "\n".join(f"{i}. {q}" for i, q in enumerate(result.committee_questions, start=1))
    conditions = "\n".join(f"- {x}" for x in result.conditions_to_change) or "- Ninguna condición adicional registrada."
    variability = "\n".join(f"- {x}" for x in result.variability_notes)
    question_validation = "\n".join(f"- {x}" for x in result.question_validation_notes)
    calibration_rows = "\n".join(
        f"| {row.control_id} | {' / '.join(row.run_statuses)} | {row.agreement_count}/{row.total_runs} | {row.agreement_percentage} % |"
        for row in result.calibration_rows
    )
    return f"""# AI Integration Guardian

**Iniciativa:** {title}  
**Fase:** {phase}  
**Decisión solicitada:** {requested_decision}  
**Recomendación:** {result.recommendation}

## Condiciones que cambiarían el resultado

{conditions}

## Preguntas para el comité

{questions}

## Verificación de preguntas

{question_validation}

## Matriz de evidencias

| Control | Estado | Sustento | Cita literal |
|---|---|---|---|
{chr(10).join(rows)}

## Variabilidad entre corridas

{variability}

| Control | Estados por corrida | Acuerdo dominante | Estabilidad |
|---|---|---:|---:|
{calibration_rows}

## Predicción falsable

- Punto de fallo: {result.prediction.likely_failure_point}
- Señal observable: {result.prediction.observable_signal}
- Revisión: {result.prediction.review_date_or_milestone}
- Quedaría refutada si: {result.prediction.condition_that_would_disprove_it}

## Trazabilidad

- Modelo: {model}
- Corridas: {result.run_count}
- Generado: {datetime.now().isoformat(timespec='minutes')}
- Decisión final: requiere revisión y asunción humana.
"""
