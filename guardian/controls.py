CONTROL_DEFINITIONS = {
    "C1": {
        "name": "Responsable de negocio",
        "question": "¿Hay una persona con nombre y capacidad de decisión que responde del resultado, no solo del proyecto?",
    },
    "C2": {
        "name": "Problema, línea base y métrica",
        "question": "¿Existe un dolor medido hoy, con línea base, objetivo e horizonte?",
    },
    "C3": {
        "name": "Dato",
        "question": "¿Están demostrados la existencia, acceso, calidad y derecho contractual de uso, exportación o explotación del dato? Las autorizaciones del propietario o proveedor del dato se evalúan exclusivamente aquí.",
    },
    "C4": {
        "name": "Integración y supervisión",
        "question": "¿Se define cómo entra la IA en el proceso y qué sucede cuando la IA y la persona discrepan?",
    },
    "C5": {
        "name": "Privacidad, seguridad, derechos e impacto",
        "question": "¿Se han tratado privacidad, ciberseguridad, impacto sobre personas, derechos fundamentales y exposición regulatoria o reputacional? No duplique aquí la propiedad, exportación ni autorización contractual del dato, que pertenecen a C3.",
    },
    "C6": {
        "name": "Coste total, alternativa no IA y abandono",
        "question": "¿Se incluyen todos los costes, se descarta una alternativa simple y se fija cuándo abandonar?",
    },
}


CRITICALITY = {
    "IDEA": {"C1": "CRÍTICO", "C2": "CRÍTICO", "C3": "RELEVANTE", "C4": "NO APLICA", "C5": "RELEVANTE", "C6": "RELEVANTE"},
    "POC": {"C1": "CRÍTICO", "C2": "CRÍTICO", "C3": "CRÍTICO", "C4": "RELEVANTE", "C5": "CRÍTICO", "C6": "RELEVANTE"},
    "PILOTO": {"C1": "CRÍTICO", "C2": "CRÍTICO", "C3": "CRÍTICO", "C4": "CRÍTICO", "C5": "CRÍTICO", "C6": "CRÍTICO"},
    "ESCALADO": {"C1": "CRÍTICO", "C2": "CRÍTICO", "C3": "CRÍTICO", "C4": "CRÍTICO", "C5": "CRÍTICO", "C6": "CRÍTICO"},
}
