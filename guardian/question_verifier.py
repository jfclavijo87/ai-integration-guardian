from __future__ import annotations

import re
import unicodedata


NUMERIC_FACT = re.compile(
    r"\b(\d[\d.,]*)\s*(%|eur|euros?|horas?|d[ií]as?|semanas?|meses?|a[nñ]os?)\b",
    re.IGNORECASE,
)


SAFE_FALLBACK_QUESTIONS = [
    "¿Qué documento acredita que la persona identificada asume la responsabilidad por el resultado de negocio?",
    "¿Qué evidencia permitirá al comité confirmar la línea base, el objetivo y el horizonte de la iniciativa?",
    "¿Qué documento acredita la existencia, calidad, acceso y derecho contractual de uso de los datos?",
    "¿Qué procedimiento se aplicará cuando la recomendación de la IA y el criterio humano discrepen?",
    "¿Qué responsable validó los controles de privacidad, seguridad e impacto sobre personas?",
    "¿Qué condición objetiva obligará a detener la iniciativa antes de consumir más recursos?",
]


def verify_questions(questions: list[str], source_text: str) -> tuple[list[str], list[str]]:
    source_facts = _facts(source_text)
    accepted: list[str] = []
    notes: list[str] = []

    for question in questions:
        question_facts = _facts(question)
        unsupported = question_facts - source_facts
        if unsupported:
            notes.append(
                f"Pregunta descartada por introducir una cifra o unidad no sustentada: {question}"
            )
            continue
        if question not in accepted:
            accepted.append(question)

    for fallback in SAFE_FALLBACK_QUESTIONS:
        if len(accepted) >= 6:
            break
        if fallback not in accepted:
            accepted.append(fallback)

    return accepted[:10], notes or ["No se detectaron cifras o unidades no sustentadas en las preguntas."]


def _facts(text: str) -> set[tuple[str, str]]:
    return {(_number(number), _unit(unit)) for number, unit in NUMERIC_FACT.findall(_plain(text))}


def _plain(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def _number(value: str) -> str:
    return value.replace(".", "").replace(",", ".")


def _unit(value: str) -> str:
    value = value.casefold().replace("í", "i").replace("ñ", "n")
    if value in {"eur", "euro", "euros"}:
        return "eur"
    if value in {"hora", "horas"}:
        return "hora"
    if value in {"dia", "dias"}:
        return "dia"
    if value in {"semana", "semanas"}:
        return "semana"
    if value in {"mes", "meses"}:
        return "mes"
    if value in {"ano", "anos"}:
        return "ano"
    return value

