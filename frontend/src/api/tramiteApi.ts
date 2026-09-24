const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export { BASE_URL }

export interface AccesibleResponse {
  homoclave: string
  generado: boolean
  url_documento: string | null
  url_audio: string | null
}

/**
 * Elimina toda la sintaxis Markdown y deja solo texto plano con puntuación
 * natural (espacios, comas, puntos, acentos) para que TTS y Web Speech
 * pronuncien correctamente sin leer "asterisco", "almohadilla", etc.
 *
 * Orden de transformaciones:
 *  1. Bloques de código  → vacío (no aportan información oral)
 *  2. Imágenes           → texto alternativo
 *  3. Enlaces            → solo el texto visible
 *  4. Negrita / cursiva  → texto sin marcadores
 *  5. Encabezados        → texto + punto para que TTS haga pausa
 *  6. Líneas horizontales → vacío
 *  7. Listas (-, *, +, números) → texto precedido de coma para listar con pausa
 *  8. Blockquotes        → texto sin ">"
 *  9. Backtick inline    → texto sin backtick
 * 10. Espacios múltiples y saltos de línea → espacio simple
 */
export function stripMarkdown(md: string): string {
  return md
    // 1. Bloques de código ```...```
    .replace(/```[\s\S]*?```/g, '')
    // 2. Imágenes ![alt](url) → alt
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    // 3. Enlaces [texto](url) → texto
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    // 4. Negrita+cursiva ***texto*** o ___texto___
    .replace(/\*{3}([^*]+)\*{3}/g, '$1')
    .replace(/_{3}([^_]+)_{3}/g, '$1')
    // 4b. Negrita **texto** o __texto__
    .replace(/\*{2}([^*]+)\*{2}/g, '$1')
    .replace(/_{2}([^_]+)_{2}/g, '$1')
    // 4c. Cursiva *texto* o _texto_
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/_([^_]+)_/g, '$1')
    // 5. Encabezados # ## ### → texto + punto
    .replace(/^#{1,6}\s+(.+)$/gm, '$1.')
    // 6. Líneas horizontales --- *** ___
    .replace(/^[-*_]{3,}\s*$/gm, '')
    // 7. Listas con viñeta: - item / * item / + item → ", item"
    .replace(/^[\s]*[-*+]\s+(.+)$/gm, ', $1')
    // 7b. Listas numeradas: 1. item → ", item"
    .replace(/^[\s]*\d+\.\s+(.+)$/gm, ', $1')
    // 8. Blockquotes > texto → texto
    .replace(/^>\s*/gm, '')
    // 9. Backtick inline `código` → código
    .replace(/`([^`]+)`/g, '$1')
    // 10. Limpiar comas iniciales sueltas al inicio del texto
    .replace(/^[,\s]+/, '')
    // 10b. Múltiples espacios / saltos de línea → espacio simple
    .replace(/\s{2,}/g, ' ')
    .trim()
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
