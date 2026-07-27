# AI Integration Guardian

Prototipo académico para evaluar la evidencia disponible sobre una iniciativa de inteligencia artificial.

## Qué hace

1. Recibe un documento PDF, DOCX o TXT.
2. Solicita la fase, la decisión requerida y el responsable de negocio.
3. Evalúa los controles C1-C6 tres veces con Gemini.
4. Comprueba que las citas propuestas existan en el documento.
5. Declara `NO CONCLUYENTE` cuando las corridas discrepan.
6. Calcula la recomendación mediante reglas deterministas.

## Inicio rápido

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

La clave también puede escribirse temporalmente en la barra lateral de la aplicación. No se guarda en disco.

## Publicación en Streamlit Community Cloud

1. Conecte este repositorio desde Streamlit Community Cloud.
2. Seleccione `app.py` como archivo principal.
3. En la configuración avanzada, añada los secretos del servidor:

```toml
GEMINI_API_KEY = "su_clave"
GEMINI_MODEL = "gemini-3.5-flash-lite"
```

La clave queda integrada en el servidor. El profesor puede utilizar la aplicación sin introducir una clave propia.

## Seguridad

- No incluya documentos personales, confidenciales o sujetos a reserva en el prototipo académico.
- La clave de API nunca debe añadirse al repositorio.
- El informe es apoyo para una revisión humana, no una aprobación automática.

## Modelo

El modelo predeterminado es `gemini-3.5-flash-lite`. Puede cambiarse con `GEMINI_MODEL`.
