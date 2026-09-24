"""
agent_service.py — Agente orquestador con loop ReAct + tool calling.

Recibe la pregunta del ciudadano, decide si invocar la skill RETyS BC,
obtiene la información y genera una respuesta que luego pasa al
transformador de Lectura Fácil.
"""
import json
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from skill_retys import TOOL_DEFINITION, ejecutar_skill
from lectura_facil import transformar_a_lectura_facil

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Credenciales y configuración
# ─────────────────────────────────────────────────────────────────────────────

_credentials = Credentials(
    url=os.getenv("WATSONX_URL", ""),
    api_key=os.getenv("WATSONX_API_KEY", ""),
)
_project_id = os.getenv("WATSONX_PROJECT_ID", "")
_model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-4-h-small")

# ─────────────────────────────────────────────────────────────────────────────
# System prompt del agente
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_AGENTE = """Eres Claro, un asistente de trámites gubernamentales del estado de Baja California, México.
Tu misión es ayudar a los ciudadanos a entender cómo realizar trámites del Registro Estatal de Trámites y Servicios (RETyS BC).

REGLAS IMPORTANTES:
1. Siempre consulta la herramienta 'consultar_tramite_retys' antes de responder sobre cualquier trámite.
   No respondas de memoria sobre requisitos, costos ni tiempos de trámites.
2. Si el ciudadano pregunta sobre un trámite, usa la herramienta con tipo_busqueda "parcial".
3. Si la herramienta no encuentra el trámite, informa amablemente y lista los trámites disponibles.
4. Responde en primera persona y con tono amable, como si hablaras directamente con el ciudadano.
5. Tu respuesta será procesada después para simplificarla a Lectura Fácil, así que
   incluye TODA la información relevante de la ficha del trámite en tu respuesta.
6. Si la pregunta no es sobre un trámite (saludo, pregunta general), responde de forma breve y amable
   sin usar la herramienta.

Idioma: español de México."""

# ─────────────────────────────────────────────────────────────────────────────
# Clase principal del agente
# ─────────────────────────────────────────────────────────────────────────────

class AgenteRETyS:
    """
    Agente orquestador para consultas de trámites RETyS BC.

    Usa un loop ReAct (Razonar → Actuar → Observar) con tool calling.
    """

    def __init__(self) -> None:
        self._model = ModelInference(
            model_id=_model_id,
            credentials=_credentials,
            project_id=_project_id,
        )
        self._params = {"max_tokens": 800, "temperature": 0.3}
        self._tools = [TOOL_DEFINITION]

    # ─────────────────────────────────────────────────────────────────────────
    # Loop ReAct
    # ─────────────────────────────────────────────────────────────────────────

    def _loop_react(self, historial: list[dict], max_iter: int = 5) -> str:
        """
        Ejecuta el loop ReAct hasta obtener una respuesta final del modelo.

        Args:
            historial:  Lista de mensajes en formato OpenAI.
            max_iter:   Número máximo de iteraciones para evitar bucles infinitos.

        Returns:
            Texto de la respuesta final del agente.
        """
        for _ in range(max_iter):
            response = self._model.chat(
                messages=historial,
                tools=self._tools,
                tool_choice="auto",
                params=self._params,
            )
            mensaje = response["choices"][0]["message"]

            # Si el modelo quiere usar una tool
            if mensaje.get("tool_calls"):
                historial.append({"role": "assistant", **mensaje})

                for tool_call in mensaje["tool_calls"]:
                    fn_name = tool_call["function"]["name"]
                    fn_args_raw = tool_call["function"].get("arguments", "{}")

                    # Parsear argumentos (pueden venir como string JSON)
                    if isinstance(fn_args_raw, str):
                        try:
                            fn_args = json.loads(fn_args_raw)
                        except json.JSONDecodeError:
                            fn_args = {}
                    else:
                        fn_args = fn_args_raw

                    # Ejecutar la skill correspondiente
                    if fn_name == "consultar_tramite_retys":
                        resultado = ejecutar_skill(fn_args)
                    else:
                        resultado = json.dumps(
                            {"error": f"Herramienta '{fn_name}' no reconocida."},
                            ensure_ascii=False,
                        )

                    # Agregar resultado al historial como mensaje tool
                    historial.append(
                        {
                            "role": "tool",
                            "content": resultado,
                            "tool_call_id": tool_call["id"],
                        }
                    )
                # Continuar el loop para que el modelo genere la respuesta final
                continue

            # Si es una respuesta de texto, salir del loop
            contenido = mensaje.get("content", "")
            if contenido:
                return contenido.strip()

        # Si se agotaron las iteraciones sin respuesta de texto
        return (
            "Lo siento, no pude procesar tu consulta en este momento. "
            "Por favor intenta de nuevo."
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Método público
    # ─────────────────────────────────────────────────────────────────────────

    def consultar(self, pregunta: str, modo: str = "texto") -> str:
        """
        Procesa la consulta del ciudadano y devuelve la respuesta en Lectura Fácil.

        Args:
            pregunta: Texto de la pregunta del ciudadano.
            modo:     "texto" (pantalla) o "voz" (TTS).

        Returns:
            Respuesta simplificada en Lectura Fácil.
        """
        historial = [
            {"role": "system", "content": SYSTEM_PROMPT_AGENTE},
            {"role": "user", "content": pregunta},
        ]

        respuesta_agente = self._loop_react(historial)
        respuesta_final = transformar_a_lectura_facil(respuesta_agente, modo=modo)
        return respuesta_final


# ─────────────────────────────────────────────────────────────────────────────
# Pruebas rápidas (ejecutar directamente: python agent_service.py)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agente = AgenteRETyS()

    consultas = [
        ("¿Qué necesito para sacar mi licencia de conducir?", "texto"),
        ("¿Cuánto cuesta el pasaporte y cuánto tarda?", "texto"),
        ("Necesito hacer una constancia de no antecedentes penales", "voz"),
    ]

    for pregunta, modo in consultas:
        print(f"\n{'═'*60}")
        print(f"PREGUNTA ({modo}): {pregunta}")
        print(f"{'─'*60}")
        respuesta = agente.consultar(pregunta, modo=modo)
        print(respuesta)
