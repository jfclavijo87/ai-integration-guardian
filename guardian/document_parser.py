from __future__ import annotations

from io import BytesIO

from docx import Document
from pypdf import PdfReader


class DocumentError(ValueError):
    pass


def extract_document(filename: str, data: bytes) -> str:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if suffix == "pdf":
        return _extract_pdf(data)
    if suffix == "docx":
        return _extract_docx(data)
    if suffix == "txt":
        return data.decode("utf-8", errors="replace")
    raise DocumentError("Formato no admitido. Utilice PDF, DOCX o TXT.")


def _extract_pdf(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        pages.append(f"[PÁGINA {index}]\n{page.extract_text() or ''}")
    text = "\n\n".join(pages).strip()
    if not text:
        raise DocumentError("El PDF no contiene texto extraíble. Para este MVP utilice un PDF con texto seleccionable.")
    return text


def _extract_docx(data: bytes) -> str:
    document = Document(BytesIO(data))
    paragraphs = [f"[PÁRRAFO {index}]\n{p.text}" for index, p in enumerate(document.paragraphs, start=1) if p.text.strip()]
    return "\n\n".join(paragraphs)

