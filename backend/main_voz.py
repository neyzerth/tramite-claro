"""
main_voz.py — CLI conversacional: modo texto o modo voz.

Uso:
  python main_voz.py          # modo texto (teclado → pantalla)
  python main_voz.py --voz    # modo accesibilidad (micrófono → altavoz)
"""
import argparse
import sys

from agent_service import AgenteRETyS
from stt_service import escuchar_consulta
from tts_service import hablar

# ─────────────────────────────────────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────────────────────────────────────

PALABRAS_SALIDA = {"salir", "adios", "adiós", "exit", "quit", "chao", "bye"}
BIENVENIDA = """
╔══════════════════════════════════════════════════════════╗
║          🏛️  TRÁMITE CLARO — Asistente Ciudadano         ║
║          Registro Estatal de Trámites de BC (RETyS)      ║
╚══════════════════════════════════════════════════════════╝
Puedo ayudarte con:  licencia de conducir · acta de nacimiento
                     pasaporte · credencial de elector · y más

Escribe "salir" para terminar.
"""
SEPARADOR = "─" * 60


# ─────────────────────────────────────────────────────────────────────────────
# Modos de operación
# ─────────────────────────────────────────────────────────────────────────────

def modo_texto(agente: AgenteRETyS) -> None:
    """Loop conversacional de texto: entrada por teclado, salida en terminal."""
    print(BIENVENIDA)
    print("Modo: TEXTO  (escribe tu pregunta)\n")

    while True:
        try:
            pregunta = input("¿En qué puedo ayudarte? > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 ¡Hasta luego!")
            break

        if not pregunta:
            continue

        if pregunta.lower() in PALABRAS_SALIDA:
            print("👋 ¡Hasta luego! Que tengas un buen día.")
            break

        print(f"\n{SEPARADOR}")
        print("⏳ Consultando...")
        try:
            respuesta = agente.consultar(pregunta, modo="texto")
        except Exception as exc:  # noqa: BLE001
            print(f"❌ Error al procesar tu consulta: {exc}")
            print("Por favor intenta de nuevo.")
            print(SEPARADOR)
            continue

        print(f"\n{respuesta}")
        print(f"\n{SEPARADOR}\n")


def modo_accesibilidad(agente: AgenteRETyS) -> None:
    """Loop conversacional por voz: micrófono → agente → altavoz."""
    print(BIENVENIDA)
    print("Modo: VOZ  (habla al micrófono cuando veas el ícono 🎤)\n")

    # Saludo inicial por voz
    try:
        hablar(
            "Hola. Soy Claro, tu asistente de trámites de Baja California. "
            "¿En qué puedo ayudarte hoy?"
        )
    except Exception:  # noqa: BLE001
        print("⚠️  No se pudo reproducir el audio de bienvenida (verifica TTS_URL y TTS_API_KEY).")

    while True:
        print("\n🎤 Habla ahora (8 segundos)...")
        try:
            pregunta = escuchar_consulta(duracion_seg=8)
        except RuntimeError as exc:
            print(f"❌ Error de micrófono: {exc}")
            break

        if not pregunta:
            print("⚠️  No te escuché. Por favor repite.")
            try:
                hablar("No te escuché bien. Por favor repite tu pregunta.")
            except Exception:  # noqa: BLE001
                pass
            continue

        print(f"🗣️  Entendí: \"{pregunta}\"")

        # Detectar palabra de salida en la transcripción
        if any(palabra in pregunta.lower() for palabra in PALABRAS_SALIDA):
            despedida = "¡Hasta luego! Que tengas un buen día."
            print(f"\n👋 {despedida}")
            try:
                hablar(despedida)
            except Exception:  # noqa: BLE001
                pass
            break

        print("⏳ Procesando tu consulta...")
        try:
            respuesta = agente.consultar(pregunta, modo="voz")
        except Exception as exc:  # noqa: BLE001
            print(f"❌ Error: {exc}")
            try:
                hablar("Lo siento. Hubo un error al procesar tu consulta. Por favor intenta de nuevo.")
            except Exception:  # noqa: BLE001
                pass
            continue

        print(f"\n{SEPARADOR}")
        print(f"📢 Respuesta:\n{respuesta}")
        print(SEPARADOR)

        try:
            hablar(respuesta)
        except Exception as exc:  # noqa: BLE001
            print(f"⚠️  No se pudo reproducir el audio: {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trámite Claro — Asistente de trámites RETyS BC"
    )
    parser.add_argument(
        "--voz",
        action="store_true",
        help="Activa el modo de accesibilidad por voz (micrófono + altavoz).",
    )
    args = parser.parse_args()

    print("Iniciando Trámite Claro...")
    agente = AgenteRETyS()

    if args.voz:
        modo_accesibilidad(agente)
    else:
        modo_texto(agente)


if __name__ == "__main__":
    main()
