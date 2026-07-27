from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from guardian.calibration import consolidate
from guardian.demo import demo_run
from guardian.document_parser import DocumentError, extract_document
from guardian.evaluator import evaluate_with_gemini
from guardian.report import to_markdown


load_dotenv()
st.set_page_config(page_title="AI Integration Guardian", layout="wide")


def configured_value(name: str, default: str = "") -> str:
    """Read deployment secrets first and local environment variables second."""
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)

st.title("AI Integration Guardian")
st.caption("Evalúa la evidencia disponible. No aprueba inversiones ni sustituye al comité.")

SAMPLE_CASES = {
    "Caso 1: inspección visual completa": {
        "path": "test_cases/01_limpio_inspeccion_visual/caso.txt",
        "initiative": "Inspección visual de defectos",
        "phase": "PILOTO",
        "decision": "Autorizar un piloto de 24.800 EUR durante ocho semanas.",
        "owner": "Laura Gómez, directora de Operaciones",
    },
    "Caso 2: mantenimiento predictivo completo": {
        "path": "test_cases/02_limpio_mantenimiento_predictivo/caso.txt",
        "initiative": "Mantenimiento predictivo de prensas",
        "phase": "POC",
        "decision": "Autorizar una prueba de concepto con límite de 9.500 EUR.",
        "owner": "Miguel Torres, gerente de Mantenimiento",
    },
    "Caso 3: planificación de demanda completa": {
        "path": "test_cases/03_limpio_planificacion_demanda/caso.txt",
        "initiative": "Apoyo a la planificación de demanda",
        "phase": "IDEA",
        "decision": "Autorizar una fase de descubrimiento con límite de 4.000 EUR.",
        "owner": "Paula Ríos, directora Comercial",
    },
    "Caso 4: derecho de uso no acreditado": {
        "path": "test_cases/04_defecto_derecho_dato/caso.txt",
        "initiative": "Mantenimiento predictivo con datos del fabricante",
        "phase": "PILOTO",
        "decision": "Autorizar un piloto de 21.000 EUR.",
        "owner": "Daniel Ruiz, director de Planta",
    },
    "Caso 5: ausencia de línea base": {
        "path": "test_cases/05_defecto_sin_linea_base/caso.txt",
        "initiative": "Clasificación automática de defectos",
        "phase": "PILOTO",
        "decision": "Autorizar un piloto de 18.000 EUR.",
        "owner": "Silvia Martín, directora de Calidad",
    },
    "Caso 6: ausencia de responsable": {
        "path": "test_cases/06_defecto_sin_responsable/caso.txt",
        "initiative": "Optimización del consumo en hornos",
        "phase": "PILOTO",
        "decision": "Autorizar un piloto de 28.000 EUR.",
        "owner": "Equipo de Transformación Digital",
    },
    "P-05: riesgo sobre personas": {
        "path": "test_cases/07_riesgo_sobre_personas/caso.txt",
        "initiative": "Control biométrico de acceso y productividad",
        "phase": "PILOTO",
        "decision": "Autorizar un piloto de 32.000 EUR durante doce semanas.",
        "owner": "Ricardo Peña, director de Recursos Humanos",
    },
    "P-06: documento con instrucción maliciosa": {
        "path": "test_cases/08_prompt_injection/caso.txt",
        "initiative": "Mantenimiento predictivo con prueba de inyección",
        "phase": "PILOTO",
        "decision": "Autorizar un piloto de 21.000 EUR.",
        "owner": "Daniel Ruiz, director de Planta",
    },
    "P-07: Guardian evalúa su propia propuesta": {
        "path": "test_cases/09_guardian_sobre_guardian/propuesta_guardian.pdf",
        "initiative": "AI Integration Guardian",
        "phase": "ESCALADO",
        "decision": "Autorizar el paso del MVP académico a un piloto empresarial controlado.",
        "owner": "juan fernando clavijo, líder del proyecto",
    },
}

with st.sidebar:
    st.header("Configuración")
    mode = st.radio("Modo", ["Gemini", "Demostración sin API"], index=0)
    default_key = configured_value("GEMINI_API_KEY")
    api_key = st.text_input("Clave de Gemini", value=default_key, type="password", help="Se utiliza solo durante esta sesión.")
    model = st.text_input("Modelo", value=configured_value("GEMINI_MODEL", "gemini-3.5-flash-lite"))
    run_count = st.select_slider("Corridas de calibración", options=[1, 3, 5], value=3)
    st.warning("Utilice únicamente documentos sintéticos o anonimizados.")

source_mode = st.radio("1. Documento que se evaluará", ["Caso de prueba incluido", "Subir otro documento"], horizontal=True)
sample_meta = None
uploaded = None
if source_mode == "Caso de prueba incluido":
    selected_sample = st.selectbox("Seleccione el caso", list(SAMPLE_CASES))
    sample_meta = SAMPLE_CASES[selected_sample]
    document_path = Path(sample_meta["path"])
    document_name = document_path.name
    document_bytes = document_path.read_bytes()
    st.caption("El caso es sintético y puede utilizarse sin riesgo de exponer información empresarial.")
else:
    uploaded = st.file_uploader("Suba el documento de la iniciativa", type=["pdf", "docx", "txt"])
    document_name = uploaded.name if uploaded else ""
    document_bytes = uploaded.getvalue() if uploaded else b""

col1, col2 = st.columns(2)
with col1:
    initiative_name = st.text_input("Nombre de la iniciativa", value=sample_meta["initiative"] if sample_meta else "", placeholder="Ej.: Inspección visual de defectos")
    phase_options = ["IDEA", "POC", "PILOTO", "ESCALADO"]
    phase = st.selectbox("2. Fase declarada", phase_options, index=phase_options.index(sample_meta["phase"]) if sample_meta else 0)
with col2:
    requested_decision = st.text_area("3. Decisión solicitada y coste", value=sample_meta["decision"] if sample_meta else "", placeholder="Ej.: Autorizar piloto de 25.000 EUR durante 8 semanas")
    business_owner = st.text_input("4. Responsable de negocio y unidad", value=sample_meta["owner"] if sample_meta else "", placeholder="Ej.: Laura Gómez, directora de Operaciones")

ready = all([document_bytes, initiative_name.strip(), requested_decision.strip(), business_owner.strip()])
if st.button("Evaluar iniciativa", type="primary", disabled=not ready):
    try:
        source_text = extract_document(document_name, document_bytes)
        if mode == "Gemini" and not api_key:
            st.error("Falta la clave de Gemini. Escríbala en la barra lateral o seleccione el modo demostración.")
            st.stop()

        runs = []
        progress = st.progress(0, text="Preparando la evaluación...")
        for index in range(run_count):
            if mode == "Gemini":
                run = evaluate_with_gemini(api_key, model, source_text, phase, requested_decision, business_owner)
            else:
                run = demo_run(source_text, business_owner)
            runs.append(run)
            progress.progress((index + 1) / run_count, text=f"Corrida {index + 1} de {run_count} completada")

        result = consolidate(runs, source_text, phase)
        st.session_state["guardian_result"] = result
        st.session_state["guardian_report"] = to_markdown(initiative_name, phase, requested_decision, result, model if mode == "Gemini" else "MODO DEMOSTRACIÓN")
        progress.empty()
    except DocumentError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"No fue posible completar la evaluación: {exc}")

if result := st.session_state.get("guardian_result"):
    st.divider()
    st.subheader("Recomendación")
    st.info(result.recommendation)

    st.subheader("Controles")
    st.dataframe([
        {
            "Control": c.control_id,
            "Estado": c.status,
            "Sustento": c.support_level,
            "Cita verificada": "Sí" if c.quote_verified else "No",
            "Cita": c.literal_quote,
            "Qué falta": c.missing_evidence,
        }
        for c in result.controls
    ], width="stretch", hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Preguntas para el comité")
        for index, question in enumerate(result.committee_questions, start=1):
            st.write(f"{index}. {question}")
    with right:
        st.subheader("Variabilidad")
        for note in result.variability_notes:
            st.write(f"- {note}")
        st.dataframe([
            {
                "Control": row.control_id,
                "Estados": " / ".join(row.run_statuses),
                "Acuerdo": f"{row.agreement_count}/{row.total_runs}",
                "Estabilidad": f"{row.agreement_percentage} %",
            }
            for row in result.calibration_rows
        ], width="stretch", hide_index=True)
        st.subheader("Predicción falsable")
        st.write(result.prediction.model_dump())
        with st.expander("Verificación de preguntas"):
            for note in result.question_validation_notes:
                st.write(f"- {note}")

    report = st.session_state["guardian_report"]
    st.download_button("Descargar informe", report, file_name="informe_guardian.md", mime="text/markdown")
