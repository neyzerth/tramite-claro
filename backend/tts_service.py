"""
tts_service.py — Watson Text to Speech.

Convierte texto simplificado (modo voz) en audio MP3 usando Watson TTS
con voz neural en español latinoamericano, y lo reproduce con ffplay.
"""
import os
import subprocess
import tempfile
from dotenv import load_dotenv
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Configuración del cliente Watson TTS
# ─────────────────────────────────────────────────────────────────────────────

_TTS_VOZ = "es-LA_SofiaV3Voice"   # Voz neural, español latinoamericano
_MAX_CHARS_POR_SEGMENTO = 4800    # Watson TTS tiene límite de ~5000 caracteres


def _get_tts_client() -> TextToSpeechV1:
    """Crea y devuelve una instancia autenticada de Watson TTS."""
    authenticator = IAMAuthenticator(os.getenv("TTS_API_KEY", ""))
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(os.getenv("TTS_URL", ""))
    return client


# ─────────────────────────────────────────────────────────────────────────────
# Síntesis de voz
# ─────────────────────────────────────────────────────────────────────────────

def texto_a_audio(texto: str) -> bytes:
    """
    Sintetiza texto a audio MP3 usando Watson TTS.

    Args:
        texto: Texto a sintetizar (máx. ~4800 caracteres por llamada).

    Returns:
        Bytes del audio en formato MP3.

    Raises:
        RuntimeError: Si el servicio Watson TTS no está disponible.
    """
    try:
        client = _get_tts_client()
        respuesta = client.synthesize(
            text=texto,
            voice=_TTS_VOZ,
            accept="audio/mp3",
        ).get_result()
        return respuesta.content
    except Exception as exc:
        raise RuntimeError(
            f"Error al conectar con Watson TTS: {exc}. "
            "Verifica TTS_API_KEY y TTS_URL en tu archivo .env."
        ) from exc


# ─────────────────────────────────────────────────────────────────────────────
# Reproducción de audio
# ─────────────────────────────────────────────────────────────────────────────

def reproducir_audio(audio_bytes: bytes) -> None:
    """
    Reproduce bytes de audio MP3 usando ffplay.

    Guarda el audio en un archivo temporal, lo reproduce y luego lo elimina.

    Args:
        audio_bytes: Bytes del audio MP3.

    Raises:
        RuntimeError: Si ffplay no está instalado en el sistema.
    """
    with tempfile.NamedTemporaryFile(
        suffix=".mp3", delete=False, prefix="tramite_audio_"
    ) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        resultado = subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", tmp_path],
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "ffplay no está instalado. Instala ffmpeg con: sudo apt install ffmpeg"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Error al reproducir el audio: {exc}") from exc
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ─────────────────────────────────────────────────────────────────────────────
# Segmentación de texto largo
# ─────────────────────────────────────────────────────────────────────────────

def segmentar_texto(texto: str, max_chars: int = _MAX_CHARS_POR_SEGMENTO) -> list[str]:
    """
    Divide el texto en segmentos de a lo mucho max_chars caracteres,
    cortando en oraciones completas (punto + espacio).

    Args:
        texto:     Texto a segmentar.
        max_chars: Número máximo de caracteres por segmento.

    Returns:
        Lista de segmentos de texto.
    """
    if len(texto) <= max_chars:
        return [texto]

    segmentos = []
    inicio = 0
    while inicio < len(texto):
        fin = inicio + max_chars
        if fin >= len(texto):
            segmentos.append(texto[inicio:].strip())
            break

        # Buscar el último punto antes del límite para no cortar a la mitad
        corte = texto.rfind(". ", inicio, fin)
        if corte == -1:
            corte = fin   # No hay punto, cortar en el límite duro
        else:
            corte += 2    # Incluir ". " en el segmento anterior

        segmento = texto[inicio:corte].strip()
        if segmento:
            segmentos.append(segmento)
        inicio = corte

    return segmentos


# ─────────────────────────────────────────────────────────────────────────────
# Función combinada
# ─────────────────────────────────────────────────────────────────────────────

def hablar(texto: str) -> None:
    """
    Sintetiza y reproduce el texto completo, segmentando si es necesario.

    Args:
        texto: Texto a hablar.
    """
    segmentos = segmentar_texto(texto)
    for segmento in segmentos:
        audio = texto_a_audio(segmento)
        reproducir_audio(audio)


# ─────────────────────────────────────────────────────────────────────────────
# Prueba rápida (ejecutar directamente: python tts_service.py)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    texto_prueba = (
        "Hola. Soy Claro, tu asistente de trámites de Baja California. "
        "Puedo ayudarte a saber qué necesitas para hacer tus trámites. "
        "¿En qué puedo ayudarte hoy?"
    )
    print(f"Sintetizando: '{texto_prueba}'")
    hablar(texto_prueba)
    print("✅ Audio reproducido correctamente.")
