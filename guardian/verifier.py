from __future__ import annotations

import re
import unicodedata

from guardian.schemas import ControlFinding, VerifiedFinding


ABSENCE_MARKER = "[NO LOCALIZADO EN EL MATERIAL ANALIZADO]"


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", value).strip()


def verify_finding(finding: ControlFinding, source_text: str) -> VerifiedFinding:
    quote = finding.literal_quote.strip()
    absent = quote == ABSENCE_MARKER
    found = False if absent else normalize(quote) in normalize(source_text)
    status = finding.status
    support = finding.support_level
    note = "Cita localizada literalmente." if found else "No se aportó una cita verificable."

    if not found:
        quote = ABSENCE_MARKER
        support = "SIN EVIDENCIA LOCALIZADA"
        if status == "CUMPLE":
            status = "DESCONOCIDO"
            note = "La cita no aparece en la fuente; CUMPLE se rebajó automáticamente a DESCONOCIDO."

    if status == "CUMPLE" and support != "VALIDADA POR RESPONSABLE IDENTIFICADO":
        status = "DESCONOCIDO"
        note = "El control no tiene evidencia validada por un responsable identificado; CUMPLE se rebajó automáticamente a DESCONOCIDO."

    return VerifiedFinding(
        **finding.model_dump(exclude={"literal_quote", "support_level", "status"}),
        status=status,
        support_level=support,
        literal_quote=quote,
        quote_verified=found,
        verification_note=note,
    )
