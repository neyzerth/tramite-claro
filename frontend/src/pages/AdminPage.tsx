import { Fragment, useState, useEffect, useCallback } from 'react'
import { marked } from 'marked'
import Container from 'react-bootstrap/Container'
import Table from 'react-bootstrap/Table'
import Button from 'react-bootstrap/Button'
import Badge from 'react-bootstrap/Badge'
import Spinner from 'react-bootstrap/Spinner'
import Alert from 'react-bootstrap/Alert'
import Modal from 'react-bootstrap/Modal'
import { listarEstado, generarTramite } from '../api/adminApi'
import type { TramiteAdminStatus } from '../api/adminApi'
const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

interface RowState {
  data: TramiteAdminStatus
  generando: boolean
  error: string | null
}

interface PreviewState {
  nombre: string
  mdContent: string | null
  cargando: boolean
}

function AdminPage() {
  const [filas, setFilas] = useState<RowState[]>([])
  const [cargando, setCargando] = useState(true)
  const [errorCarga, setErrorCarga] = useState<string | null>(null)
  const [generandoTodos, setGenerandoTodos] = useState(false)
  const [progresoTodos, setProgresoTodos] = useState<string | null>(null)
  const [preview, setPreview] = useState<PreviewState | null>(null)

  const cargarEstado = useCallback(async () => {
    setCargando(true)
    setErrorCarga(null)
    try {
      const lista = await listarEstado()
      setFilas(lista.map((item) => ({ data: item, generando: false, error: null })))
    } catch (err) {
      setErrorCarga(err instanceof Error ? err.message : 'Error desconocido al cargar los trámites.')
    } finally {
      setCargando(false)
    }
  }, [])

  useEffect(() => {
    void cargarEstado()
  }, [cargarEstado])

  const handleGenerar = async (homoclave: string) => {
    setFilas((prev) =>
      prev.map((f) => (f.data.homoclave === homoclave ? { ...f, generando: true, error: null } : f)),
    )
    try {
      const resultado = await generarTramite(homoclave)
      setFilas((prev) =>
        prev.map((f) =>
          f.data.homoclave === homoclave
            ? {
                ...f,
                generando: false,
                error: null,
                data: {
                  ...f.data,
                  tiene_md: resultado.url_documento !== null,
                  tiene_audio: resultado.url_audio !== null,
                  url_documento: resultado.url_documento,
                  url_audio: resultado.url_audio,
                },
              }
            : f,
        ),
      )
    } catch (err) {
      const mensaje = err instanceof Error ? err.message : 'Error desconocido durante la generación.'
      setFilas((prev) =>
        prev.map((f) => (f.data.homoclave === homoclave ? { ...f, generando: false, error: mensaje } : f)),
      )
    }
  }

  const handleVerPreview = async (fila: RowState) => {
    setPreview({ nombre: fila.data.nombre, mdContent: null, cargando: true })
    try {
      const res = await fetch(`${BASE_URL}/${fila.data.url_documento!}`)
      const text = res.ok ? await res.text() : null
      setPreview({ nombre: fila.data.nombre, mdContent: text, cargando: false })
    } catch {
      setPreview({ nombre: fila.data.nombre, mdContent: null, cargando: false })
    }
  }

  const handleGenerarTodos = async () => {
    setGenerandoTodos(true)
    const total = filas.length
    for (let i = 0; i < total; i++) {
      const fila = filas[i]
      setProgresoTodos(`Generando ${i + 1} de ${total}: ${fila.data.nombre}…`)
      await handleGenerar(fila.data.homoclave)
    }
    setProgresoTodos(null)
    setGenerandoTodos(false)
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f4f6fb' }}>
      {/* Cabecera del panel */}
      <div
        style={{
          background: 'linear-gradient(135deg, #003a8c 0%, #0055cc 100%)',
          color: '#fff',
          padding: '1.5rem 0',
          marginBottom: '2rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
        }}
      >
        <Container className="d-flex justify-content-between align-items-center flex-wrap gap-3">
          <div>
            <h4 className="mb-0 fw-bold">🛠 Panel de Administración</h4>
            <small style={{ opacity: 0.8 }}>RETyS Accesible — Gestión de Lectura Fácil y Audio TTS</small>
          </div>
          <Button
            variant="warning"
            disabled={generandoTodos || cargando || filas.length === 0}
            onClick={() => { void handleGenerarTodos() }}
            className="fw-semibold"
          >
            {generandoTodos ? (
              <>
                <Spinner size="sm" className="me-2" />
                {progresoTodos ?? 'Generando…'}
              </>
            ) : (
              '⚡ Generar todos'
            )}
          </Button>
        </Container>
      </div>

      <Container>
        {/* Estado de carga inicial */}
        {cargando && (
          <div className="text-center py-5">
            <Spinner animation="border" variant="primary" />
            <p className="mt-3 text-muted">Cargando estado de los trámites…</p>
          </div>
        )}

        {/* Error de carga */}
        {!cargando && errorCarga && (
          <Alert variant="danger">
            <Alert.Heading>No se pudo conectar con el backend</Alert.Heading>
            <p className="mb-2">{errorCarga}</p>
            <Button variant="outline-danger" size="sm" onClick={() => { void cargarEstado() }}>
              🔄 Reintentar
            </Button>
          </Alert>
        )}

        {/* Tabla de trámites */}
        {!cargando && !errorCarga && (
          <>
            <p className="text-muted mb-3" style={{ fontSize: '0.88rem' }}>
              {filas.length} trámite{filas.length !== 1 ? 's' : ''} en el catálogo.
              Genera la versión accesible de cada uno antes de la demo.
            </p>
            <div style={{ background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
              <Table hover responsive className="mb-0" style={{ fontSize: '0.88rem' }}>
                <thead style={{ background: '#f0f4fa' }}>
                  <tr>
                    <th style={{ width: '35%' }}>Trámite</th>
                    <th style={{ width: '15%' }}>Homoclave</th>
                    <th style={{ width: '15%', textAlign: 'center' }}>Lectura Fácil</th>
                    <th style={{ width: '15%', textAlign: 'center' }}>Audio TTS</th>
                    <th style={{ width: '20%', textAlign: 'center' }}>Acción</th>
                  </tr>
                </thead>
                <tbody>
                  {filas.map((fila) => (
                    <Fragment key={fila.data.homoclave}>
                      <tr>
                        <td className="fw-semibold align-middle">{fila.data.nombre}</td>
                        <td className="align-middle">
                          <code style={{ fontSize: '0.78rem', background: '#f0f4fa', padding: '2px 6px', borderRadius: 4 }}>
                            {fila.data.homoclave}
                          </code>
                        </td>
                        <td className="text-center align-middle">
                          {fila.data.tiene_md ? (
                            <div className="d-flex align-items-center justify-content-center gap-1">
                              <Badge bg="success">✅ Generado</Badge>
                              <Button
                                size="sm"
                                variant="outline-success"
                                style={{ padding: '1px 6px', fontSize: '0.75rem' }}
                                onClick={() => { void handleVerPreview(fila) }}
                              >
                                👁 Ver
                              </Button>
                            </div>
                          ) : (
                            <Badge bg="secondary">⏳ Pendiente</Badge>
                          )}
                        </td>
                        <td className="text-center align-middle">
                          {fila.data.tiene_audio ? (
                            <Badge bg="success">✅ Generado</Badge>
                          ) : (
                            <Badge bg="secondary">⏳ Pendiente</Badge>
                          )}
                        </td>
                        <td className="text-center align-middle">
                          <Button
                            size="sm"
                            variant={fila.data.tiene_md ? 'outline-secondary' : 'primary'}
                            disabled={fila.generando || generandoTodos}
                            onClick={() => { void handleGenerar(fila.data.homoclave) }}
                          >
                            {fila.generando ? (
                              <>
                                <Spinner size="sm" className="me-1" />
                                Generando…
                              </>
                            ) : fila.data.tiene_md ? (
                              '🔄 Actualizar'
                            ) : (
                              'Generar'
                            )}
                          </Button>
                        </td>
                      </tr>
                      {fila.error && (
                        <tr>
                          <td colSpan={5} style={{ padding: '0.25rem 1rem 0.75rem' }}>
                            <Alert variant="danger" className="mb-0 py-2" style={{ fontSize: '0.82rem' }}>
                              ❌ {fila.error}
                            </Alert>
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  ))}
                </tbody>
              </Table>
            </div>
          </>
        )}
      </Container>

      {/* Modal de previsualización de Lectura Fácil */}
      <Modal
        show={preview !== null}
        onHide={() => { setPreview(null) }}
        size="lg"
        scrollable
      >
        <Modal.Header closeButton style={{ background: '#f0f4fa' }}>
          <Modal.Title style={{ fontSize: '1rem' }}>
            📄 Lectura Fácil — {preview?.nombre}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {preview?.cargando && (
            <div className="text-center py-4">
              <Spinner animation="border" variant="success" />
              <p className="mt-2 text-muted">Cargando documento…</p>
            </div>
          )}
          {!preview?.cargando && preview?.mdContent && (
            <div
              className="lectura-facil-content p-3 rounded"
              style={{
                background: '#f8fff8',
                border: '2px solid #28a745',
                lineHeight: 1.8,
                fontSize: '1rem',
              }}
              dangerouslySetInnerHTML={{ __html: marked(preview.mdContent) as string }}
            />
          )}
          {!preview?.cargando && !preview?.mdContent && (
            <Alert variant="warning" className="mb-0">
              No se pudo cargar el documento. Verifica que el backend esté activo.
            </Alert>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => { setPreview(null) }}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

export default AdminPage