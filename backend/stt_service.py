"""
stt_service.py — Watson Speech to Text.

Graba audio desde el micrófono y lo transcribe usando Watson STT
con el modelo en español mexicano (es-MX, banda ancha 16kHz).
"""
import os
from dotenv import load_dotenv
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests as _requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Configuración del cliente Watson STT
# ─────────────────────────────────────────────────────────────────────────────

_STT_MODEL = "es-MX_BroadbandModel"   # Español mexicano, banda ancha (es-LA_BroadbandModel retirado)
_AUDIO_RATE = 16000
_AUDIO_CHANNELS = 1
_AUDIO_FORMAT_PA = None   # Se inicializa con pyaudio en tiempo de ejecución
_AUDIO_CHUNK = 1024


def _get_stt_client() -> SpeechToTextV1:
    """Crea y devuelve una instancia autenticada de Watson STT con retry automático."""
    authenticator = IAMAuthenticator(os.getenv("STT_API_KEY", ""))
    client = SpeechToTextV1(authenticator=authenticator)
    client.set_service_url(os.getenv("STT_URL", ""))

    # Configurar retry para tolerar fallos transitorios de red en el pool HTTPS
    session = _requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    client.set_http_client(session)

    return client


# ─────────────────────────────────────────────────────────────────────────────
# Grabación de audio
# ─────────────────────────────────────────────────────────────────────────────

def grabar_audio(duracion_seg: int = 8) -> bytes:
    """
    Graba audio desde el micrófono del sistema.

    Args:
        duracion_seg: Duración de la grabación en segundos.

    Returns:
        Bytes del audio grabado en formato PCM 16-bit, mono, 16kHz.

    Raises:
        RuntimeError: Si no se puede acceder al micrófono.
    """
    try:
        import pyaudio  # importación tardía para no fallar si no está instalado
    except ImportError as exc:
        raise RuntimeError(
            "PyAudio no está instalado. Instálalo con: pip install pyaudio"
        ) from exc

    pa = pyaudio.PyAudio()
    pa_format = pyaudio.paInt16

    print("🎤 Escuchando... (habla ahora)")

    try:
        stream = pa.open(
            format=pa_format,
            channels=_AUDIO_CHANNELS,
            rate=_AUDIO_RATE,
            input=True,
            frames_per_buffer=_AUDIO_CHUNK,
        )

        frames = []
        total_chunks = int(_AUDIO_RATE / _AUDIO_CHUNK * duracion_seg)
        for _ in range(total_chunks):
            frames.append(stream.read(_AUDIO_CHUNK, exception_on_overflow=False))

        stream.stop_stream()
        stream.close()
    except OSError as exc:
        pa.terminate()
        raise RuntimeError(
            f"No se pudo acceder al micrófono: {exc}. "
            "Verifica que el micrófono esté conectado y configurado."
        ) from exc
    finally:
        pa.terminate()

    print("✅ Grabación terminada.")
    return b"".join(frames)


# ─────────────────────────────────────────────────────────────────────────────
# Transcripción
# ─────────────────────────────────────────────────────────────────────────────

def transcribir_audio(audio_bytes: bytes) -> str:
    """
    Envía audio a Watson STT y devuelve la transcripción.

    Args:
        audio_bytes: Audio en formato PCM 16-bit, mono, 16kHz.

    Returns:
        Texto transcrito, o cadena vacía si no se detectó habla.

    Raises:
        RuntimeError: Si el servicio Watson STT no está disponible.
    """
    if not audio_bytes:
        return ""

    try:
        client = _get_stt_client()
        resultado = client.recognize(
            audio=audio_bytes,
            content_type=f"audio/l16;rate={_AUDIO_RATE}",
            model=_STT_MODEL,
            smart_formatting=True,
        ).get_result()
    except Exception as exc:
        raise RuntimeError(
            f"Error al conectar con Watson STT: {exc}. "
            "Verifica STT_API_KEY y STT_URL en tu archivo .env."
        ) from exc

    resultados = resultado.get("results", [])
    if not resultados:
        return ""

    # Tomar el transcript con mayor confianza del primer resultado
    alternativas = resultados[0].get("alternatives", [])
    if not alternativas:
        return ""

    return alternativas[0].get("transcript", "").strip()


# ─────────────────────────────────────────────────────────────────────────────
# Función combinada
# ─────────────────────────────────────────────────────────────────────────────

def escuchar_consulta(duracion_seg: int = 8) -> str:
    """
    Graba audio del micrófono y lo transcribe en un solo paso.

    Args:
        duracion_seg: Duración de la grabación en segundos.

    Returns:
        Texto transcrito, o cadena vacía si no se detectó habla.
    """
    audio = grabar_audio(duracion_seg)
    transcripcion = transcribir_audio(audio)

    if not transcripcion:
        print("⚠️  No se detectó habla. Por favor, intenta de nuevo.")

    return transcripcion


# ─────────────────────────────────────────────────────────────────────────────
# Prueba rápida (ejecutar directamente: python stt_service.py)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Prueba de Watson STT — di algo en los próximos 8 segundos")
    texto = escuchar_consulta(duracion_seg=8)
    print(f"\nTranscripción: '{texto}'")
