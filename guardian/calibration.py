from __future__ import annotations

from collections import Counter

from guardian.decision_engine import decide
from guardian.question_verifier import verify_questions
from guardian.schemas import CalibrationRow, ConsolidatedEvaluation, EvaluationRun, VerifiedFinding
from guardian.verifier import verify_finding


def consolidate(runs: list[EvaluationRun], source_text: str, phase: str) -> ConsolidatedEvaluation:
    verified_runs = [[verify_finding(finding, source_text) for finding in run.controls] for run in runs]
    controls: list[VerifiedFinding] = []
    variability: list[str] = []
    calibration_rows: list[CalibrationRow] = []

    for control_id in ["C1", "C2", "C3", "C4", "C5", "C6"]:
        candidates = [next(c for c in run if c.control_id == control_id) for run in verified_runs]
        states = [c.status for c in candidates]
        state_counts = Counter(states)
        dominant_status, agreement_count = state_counts.most_common(1)[0]
        calibration_rows.append(CalibrationRow(
            control_id=control_id,
            run_statuses=states,
            dominant_status=dominant_status,
            agreement_count=agreement_count,
            total_runs=len(states),
            agreement_percentage=round(agreement_count * 100 / len(states)),
        ))
        selected = candidates[0].model_copy(deep=True)
        if len(set(states)) > 1:
            selected.status = "NO CONCLUYENTE"
            variability.append(f"{control_id}: las corridas discreparon ({', '.join(states)}).")
        else:
            selected.status = states[0]
        selected.quote_verified = all(c.quote_verified for c in candidates if c.literal_quote != "[NO LOCALIZADO EN EL MATERIAL ANALIZADO]")
        controls.append(selected)

    recommendation, blocking, conditions = decide(phase, controls)
    questions, question_notes = verify_questions(_most_frequent_questions(runs), source_text)
    return ConsolidatedEvaluation(
        controls=controls,
        recommendation=recommendation,
        blocking_controls=blocking,
        conditions_to_change=list(dict.fromkeys(x for x in conditions if x)),
        committee_questions=questions,
        question_validation_notes=question_notes,
        prediction=runs[0].prediction,
        run_count=len(runs),
        variability_notes=variability or (["Se realizó una sola corrida; todavía no se midió variabilidad."] if len(runs) == 1 else ["Las corridas coincidieron en los seis controles."]),
        calibration_rows=calibration_rows,
    )


def _most_frequent_questions(runs: list[EvaluationRun]) -> list[str]:
    questions = [q.strip() for run in runs for q in run.committee_questions if q.strip()]
    counts = Counter(q.casefold() for q in questions)
    return sorted(dict.fromkeys(questions), key=lambda q: counts[q.casefold()], reverse=True)
