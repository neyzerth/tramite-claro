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
  url_documento: string | null
  url_audio: string | null
}

/** Lista todos los trámites con su estado de generación (Lectura Fácil + Audio TTS). */
export async function listarEstado(): Promise<TramiteAdminStatus[]> {
  const res = await fetch(`${BASE_URL}/admin/tramites`)
  if (!res.ok) {
    throw new Error(`Error al obtener el estado de los trámites (HTTP ${res.status})`)
  }
  return res.json() as Promise<TramiteAdminStatus[]>
}

/** Genera (o regenera) la versión de Lectura Fácil y Audio TTS para un trámite dado. */
export async function generarTramite(homoclave: string): Promise<GenerarResult> {
  const res = await fetch(`${BASE_URL}/admin/tramites/${encodeURIComponent(homoclave)}/generar`, {
    method: 'POST',
  })
  if (!res.ok) {
    let mensaje = `Error al generar el trámite ${homoclave} (HTTP ${res.status})`
    try {
      const body = (await res.json()) as { detail?: string }
      if (body.detail) mensaje = body.detail
    } catch {
      // ignorar si el body no es JSON
    }
    throw new Error(mensaje)
  }
  return res.json() as Promise<GenerarResult>
}
