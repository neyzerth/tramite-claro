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
