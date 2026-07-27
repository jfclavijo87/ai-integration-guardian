from guardian.question_verifier import verify_questions


def test_rejects_number_unit_pair_not_found_in_source():
    source = "El presupuesto incluye 2.000 euros de tiempo interno y la línea acumuló 312 horas de parada."
    questions = [
        "¿Cómo se verificarán las 2.000 horas asignadas al personal?",
        "¿Quién validó el presupuesto de 2.000 euros?",
    ]
    accepted, notes = verify_questions(questions, source)
    assert questions[0] not in accepted
    assert questions[1] in accepted
    assert len(accepted) >= 6
    assert "descartada" in notes[0]


def test_accepts_percentage_with_spacing_difference():
    accepted, notes = verify_questions(
        ["¿Cómo se medirá el objetivo del 70%?"],
        "El objetivo es detectar al menos el 70 % de los eventos.",
    )
    assert "¿Cómo se medirá el objetivo del 70%?" in accepted
    assert notes == ["No se detectaron cifras o unidades no sustentadas en las preguntas."]

