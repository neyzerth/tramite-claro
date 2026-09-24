const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export interface TramiteAdminStatus {
  homoclave: string
  nombre: string
  tiene_md: boolean
  tiene_audio: boolean
  url_documento: string | null
  url_audio: string | null
}

export interface GenerarResult {
  homoclave: string
  nombre: string
  url_documento: string
  url_audio: string | null
}

/** Llama a GET /admin/tramites y devuelve el estado de generación de cada trámite. */
export async function listarEstado(): Promise<TramiteAdminStatus[]> {
  const res = await fetch(`${BASE_URL}/admin/tramites`)
  if (!res.ok) {
    throw new Error(`Error ${res.status}: ${res.statusText}`)
  }
  return res.json() as Promise<TramiteAdminStatus[]>
}

/** Llama a POST /admin/tramites/{homoclave}/generar para generar o regenerar el Markdown y audio. */
export async function generarTramite(homoclave: string): Promise<GenerarResult> {
  const res = await fetch(`${BASE_URL}/admin/tramites/${encodeURIComponent(homoclave)}/generar`, {
    method: 'POST',
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`Error ${res.status}: ${detail}`)
  }
  return res.json() as Promise<GenerarResult>
}
