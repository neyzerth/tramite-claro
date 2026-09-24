"""
tts_service.py — Watson Text to Speech.

Convierte texto simplificado (modo voz) en audio MP3 usando Watson TTS
con voz neural en español latinoamericano, y lo reproduce con ffplay.
"""
import os
import re
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
# Limpieza de Markdown para TTS
# ─────────────────────────────────────────────────────────────────────────────

def limpiar_markdown_para_tts(texto: str) -> str:
    """
    Elimina toda la sintaxis Markdown del texto para que el TTS solo
    escuche puntuación natural (comas, puntos, acentos).

    Transformaciones aplicadas:
    - Encabezados (#, ##, ###...) → solo el texto del título.
    - Negrita/itálica (**texto**, *texto*, __texto__, _texto_) → texto plano.
    - Código inline (`código`) → el texto del código sin backticks.
    - Bloques de código (```...```) → eliminados.
    - Viñetas (-, *, •) al inicio de línea → la línea sin el símbolo.
    - Listas numeradas (1. 2. ...) → la línea sin el número.
    - Liens [texto](url) → solo el texto del enlace.
    - Emojis Unicode → eliminados.
    - Líneas horizontales (---) → eliminadas.
    - Líneas en blanco múltiples → una sola línea en blanco.
    """
    # Bloques de código con triple backtick
    texto = re.sub(r"```[\s\S]*?```", "", texto)

    # Encabezados Markdown (# Título)
    texto = re.sub(r"^#{1,6}\s+", "", texto, flags=re.MULTILINE)

    # Negrita + itálica combinada ***texto***
    texto = re.sub(r"\*{3}(.+?)\*{3}", r"\1", texto)
    # Negrita **texto** y __texto__
    texto = re.sub(r"\*{2}(.+?)\*{2}", r"\1", texto)
    texto = re.sub(r"_{2}(.+?)_{2}", r"\1", texto)
    # Itálica *texto* y _texto_ (sin tocar los guiones de lista ya limpios)
    texto = re.sub(r"\*(.+?)\*", r"\1", texto)
    texto = re.sub(r"_(.+?)_", r"\1", texto)

    # Código inline `texto`
    texto = re.sub(r"`(.+?)`", r"\1", texto)

    # Links [texto](url) → texto
    texto = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", texto)

    # Viñetas al inicio de línea (-, *, •)
    texto = re.sub(r"^[\s]*[-*•]\s+", "", texto, flags=re.MULTILINE)

    # Listas numeradas al inicio de línea (1. 2. ...)
    texto = re.sub(r"^[\s]*\d+\.\s+", "", texto, flags=re.MULTILINE)

    # Líneas horizontales (--- o ***)
    texto = re.sub(r"^[\s]*[-*_]{3,}[\s]*$", "", texto, flags=re.MULTILINE)

    # Emojis Unicode
    texto = re.sub(
        r"[\U00002600-\U000027BF"
        r"\U0001F300-\U0001F9FF"
        r"\U00002702-\U000027B0"
        r"\U0000FE00-\U0000FE0F"
        r"\U0001FA00-\U0001FA6F"
        r"\U0001FA70-\U0001FAFF"
        r"\u2640-\u2642\u2194-\u2199"
        r"\u23cf\u23e9\u231a\u3030\u303d"
        r"\u00a9\u00ae\u25aa-\u25fe]+",
        "",
        texto,
    )

    # Múltiples líneas en blanco → una sola
    texto = re.sub(r"\n{3,}", "\n\n", texto)

    return texto.strip()


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
    texto = limpiar_markdown_para_tts(texto)
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
