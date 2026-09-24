const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export { BASE_URL }

export interface AccesibleResponse {
  homoclave: string
  generado: boolean
  url_documento: string | null
  url_audio: string | null
}

/** Consulta si hay una versión de Lectura Fácil pre-generada para el trámite. */
export async function consultarAccesible(homoclave: string): Promise<AccesibleResponse> {
  try {
    const res = await fetch(`${BASE_URL}/tramites/${encodeURIComponent(homoclave)}/accesible`)
    if (!res.ok) {
      return { homoclave, generado: false, url_documento: null, url_audio: null }
    }
    return res.json() as Promise<AccesibleResponse>
  } catch {
    return { homoclave, generado: false, url_documento: null, url_audio: null }
  }
}

/**
 * Llama a POST /accesibilidad/tts/sintetizar y devuelve un Blob MP3 listo
 * para reproducir con `new Audio(URL.createObjectURL(blob))`.
 * Si el backend no está disponible devuelve null para que el caller
 * caiga en Web Speech API como fallback.
 */
export async function sintetizarTTS(texto: string): Promise<Blob | null> {
  try {
    const res = await fetch(`${BASE_URL}/accesibilidad/tts/sintetizar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto }),
    })
    if (!res.ok) return null
    const { audio_base64 } = (await res.json()) as { audio_base64: string; longitud_bytes: number }
    const binary = atob(audio_base64)
    const bytes = new Uint8Array(binary.length)
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i)
    return new Blob([bytes], { type: 'audio/mpeg' })
  } catch {
    return null
  }
}
