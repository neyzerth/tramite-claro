"""
lectura_facil.py — Transformador de texto a norma UNE 153101:2018 EX.

Toma la respuesta técnica del agente y la reescribe aplicando Lectura Fácil,
con dos modos: "texto" (pantalla, con Markdown y emojis) y "voz" (TTS, sin
emojis, frases ≤20 palabras).
"""
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Credenciales y cliente watsonx.ai
# ─────────────────────────────────────────────────────────────────────────────

_credentials = Credentials(
    url=os.getenv("WATSONX_URL", ""),
    api_key=os.getenv("WATSONX_API_KEY", ""),
)
_project_id = os.getenv("WATSONX_PROJECT_ID", "")
_model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-4-h-small")

# ─────────────────────────────────────────────────────────────────────────────
# System prompts para Lectura Fácil
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_LECTURA_FACIL = """Eres un experto en Lectura Fácil según la norma UNE 153101:2018 EX.
Tu tarea es reescribir el texto que recibes aplicando estrictamente los 6 pasos de revisión:

PASO 1 — FRASES CORTAS (norma 6.1 Ortotipografía y 6.3 Frases):
- Escribe una sola idea por frase.
- Usa frases de máximo 15 palabras.
- Nunca uses punto y coma ni dos puntos seguidos de lista en la misma frase.
- Separa las ideas en frases distintas.

PASO 2 — VOCABULARIO SENCILLO (norma 6.2):
- Usa palabras que cualquier persona entienda.
- Cuando uses una sigla, explícala la primera vez. Ejemplo: INE (Instituto Nacional Electoral).
- No uses abreviaturas. Escribe las palabras completas.
- Cambia palabras difíciles por palabras simples.

PASO 3 — FORMAS VERBALES SIMPLES (norma 6.3):
- Usa el presente de indicativo siempre que puedas.
- No uses la voz pasiva. Ejemplo: "se deben presentar" → "tienes que presentar".
- No uses gerundios. Ejemplo: "siendo necesario" → "es necesario".
- No uses subjuntivo. Usa afirmaciones directas.

PASO 4 — TEXTO Y ESTILO (norma 6.4):
- Escribe en segunda persona: habla directamente al ciudadano con "tú" o "usted".
- Usa listas con viñetas (•) cuando haya 3 o más elementos seguidos.
- Pon primero la información más importante.
- Evita rodeos: ve directo al punto.

PASO 5 — PRESENTACIÓN VISUAL (norma 7.1):
- Usa emojis 📋 para listas de requisitos, 💰 para costos, ⏱ para tiempos, 📍 para lugar.
- Usa **negrita** para los términos más importantes.
- Deja una línea en blanco entre secciones.

PASO 6 — REVISIÓN FINAL:
- Asegúrate de que el texto sea amable y tranquilizador.
- Confirma que no hay información inventada: solo usa lo que estaba en el texto original.
- El texto final debe ser más corto que el original.

Responde ÚNICAMENTE con el texto transformado. No expliques lo que hiciste."""

SYSTEM_PROMPT_LECTURA_FACIL_VOZ = """Eres un experto en Lectura Fácil adaptada para síntesis de voz (norma UNE 153101:2018 EX).
Tu tarea es reescribir el texto para que suene natural cuando lo lea un asistente de voz.

Reglas estrictas:
1. Frases de máximo 20 palabras. Una sola idea por frase.
2. Sin emojis. Sin asteriscos. Sin Markdown. Solo texto plano.
3. Sin siglas sin explicar. Primera vez: "INE, es decir, el Instituto Nacional Electoral".
4. Verbos en presente de indicativo. Sin pasiva. Sin gerundios.
5. Usa "tienes que" en lugar de "se debe" o "hay que presentar".
6. Los costos en palabras: "295 pesos" (no "$295").
7. Los tiempos en días naturales con aclaración si son hábiles.
8. Para listas, di "Necesitas llevar estos documentos:" y luego cada elemento en una frase separada.
9. Termina con una frase de cierre amable.

Responde ÚNICAMENTE con el texto transformado. Sin explicaciones."""

# ─────────────────────────────────────────────────────────────────────────────
# Instancia del modelo (singleton por max_tokens para reutilizar la conexión)
# ─────────────────────────────────────────────────────────────────────────────

# El modelo se instancia sin params porque el SDK ignora max_new_tokens en .chat().
# Los parámetros se pasan directamente en cada llamada a chat().
_model = ModelInference(
    model_id=_model_id,
    credentials=_credentials,
    project_id=_project_id,
)


# ─────────────────────────────────────────────────────────────────────────────
# Función principal
# ─────────────────────────────────────────────────────────────────────────────

def transformar_a_lectura_facil(texto: str, modo: str = "texto") -> str:
    """
    Transforma un texto técnico-administrativo a Lectura Fácil.

    Args:
        texto: Texto de entrada (respuesta del agente).
        modo:  "texto" — optimizado para pantalla (Markdown, emojis).
               "voz"   — optimizado para TTS (texto plano, frases cortas).

    Returns:
        Texto transformado según la norma UNE 153101:2018 EX.
    """
    if modo == "voz":
        system_prompt = SYSTEM_PROMPT_LECTURA_FACIL_VOZ
        max_tokens = 512
    else:
        system_prompt = SYSTEM_PROMPT_LECTURA_FACIL
        max_tokens = 600

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Transforma este texto a Lectura Fácil:\n\n{texto}",
        },
    ]

    response = _model.chat(
        messages=messages,
        params={"max_tokens": max_tokens, "temperature": 0.1},
    )
    return response["choices"][0]["message"]["content"].strip()


def aplicar_6_pasos_revision(texto: str) -> dict:
    """
    Aplica los 6 pasos de revisión de Lectura Fácil y devuelve un dict con
    el texto transformado y una nota de cada paso.

    Args:
        texto: Texto de entrada.

    Returns:
        {
            "texto_transformado": str,
            "pasos": {
                "paso_1_frases": str,
                "paso_2_vocabulario": str,
                "paso_3_verbos": str,
                "paso_4_estilo": str,
                "paso_5_presentacion": str,
                "paso_6_revision_final": str,
            }
        }
    """
    prompt_diagnostico = (
        "Analiza el siguiente texto e indica brevemente (1 línea por paso) "
        "qué cambios aplicarías en cada uno de los 6 pasos de Lectura Fácil "
        "según la norma UNE 153101:2018 EX:\n\n"
        "Paso 1 - Frases cortas:\n"
        "Paso 2 - Vocabulario sencillo:\n"
        "Paso 3 - Formas verbales simples:\n"
        "Paso 4 - Texto y estilo:\n"
        "Paso 5 - Presentación visual:\n"
        "Paso 6 - Revisión final:\n\n"
        f"Texto:\n{texto}"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_LECTURA_FACIL},
        {"role": "user", "content": prompt_diagnostico},
    ]
    notas_raw = _model.chat(
        messages=messages,
        params={"max_tokens": 400, "temperature": 0.1},
    )["choices"][0]["message"]["content"]

    texto_transformado = transformar_a_lectura_facil(texto, modo="texto")

    pasos = {}
    for i, nombre in enumerate(
        [
            "paso_1_frases",
            "paso_2_vocabulario",
            "paso_3_verbos",
            "paso_4_estilo",
            "paso_5_presentacion",
            "paso_6_revision_final",
        ],
        start=1,
    ):
        lineas = [
            l.strip()
            for l in notas_raw.splitlines()
            if l.strip().startswith(f"Paso {i}")
        ]
        pasos[nombre] = lineas[0] if lineas else "—"

    return {
        "texto_transformado": texto_transformado,
        "pasos": pasos,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pruebas rápidas (ejecutar directamente: python lectura_facil.py)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ejemplos = [
        (
            "Para llevar a cabo el procedimiento de obtención de la licencia de conducir "
            "tipo B, el ciudadano deberá presentarse en la Dirección de Vialidad con la "
            "documentación requerida, misma que consta de: identificación oficial vigente, "
            "comprobante de domicilio no mayor a tres meses, CURP y el comprobante de pago "
            "de derechos por la cantidad de $295.00 pesos, debiendo además aprobar el "
            "examen psicofísico que se realizará en las instalaciones de la dependencia.",
            "texto",
        ),
        (
            "El pasaporte es el documento de viaje internacional expedido por la SRE. "
            "Para su expedición se requiere acta de nacimiento, identificación oficial, "
            "comprobante de domicilio, CURP y pago previo de derechos por $1,540 pesos.",
            "voz",
        ),
        (
            "La constancia de no antecedentes penales es emitida por la Fiscalía General "
            "del Estado, siendo necesaria la presentación de identificación oficial e INE, "
            "así como el pago correspondiente de derechos por la suma de $203.00 pesos, "
            "procediéndose a la entrega del documento el mismo día de la solicitud.",
            "texto",
        ),
    ]

    for texto_entrada, modo in ejemplos:
        print(f"\n{'─'*60}")
        print(f"MODO: {modo}")
        print(f"ORIGINAL:\n{texto_entrada}")
        print(f"\nTRANSFORMADO:")
        print(transformar_a_lectura_facil(texto_entrada, modo))
