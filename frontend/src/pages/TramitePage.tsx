import { useState, useRef, useEffect } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Table from 'react-bootstrap/Table'
import Badge from 'react-bootstrap/Badge'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import Alert from 'react-bootstrap/Alert'
import { Link, useParams } from 'react-router-dom'
import tramites from '../data/tramites'
import { consultarAccesible, BASE_URL } from '../api/tramiteApi'
import type { AccesibleResponse } from '../api/tramiteApi'

// ─────────────────────────────────────────────────────────────────────────────
// Markdown → HTML helper (no external deps)
// ─────────────────────────────────────────────────────────────────────────────

function markdownToHtml(md: string): string {
  const lines = md.split('\n')
  const output: string[] = []
  let inList = false

  for (const raw of lines) {
    const line = raw.trimEnd()

    if (/^## (.+)/.test(line)) {
      if (inList) { output.push('</ul>'); inList = false }
      output.push(`<h5>${line.replace(/^## /, '')}</h5>`)
    } else if (/^# (.+)/.test(line)) {
      if (inList) { output.push('</ul>'); inList = false }
      output.push(`<h4>${line.replace(/^# /, '')}</h4>`)
    } else if (/^[-*] (.+)/.test(line)) {
      if (!inList) { output.push('<ul>'); inList = true }
      const itemText = line.replace(/^[-*] /, '').replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      output.push(`<li>${itemText}</li>`)
    } else if (line.trim() === '') {
      if (inList) { output.push('</ul>'); inList = false }
      output.push('<br />')
    } else {
      if (inList) { output.push('</ul>'); inList = false }
      const para = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      output.push(`<p>${para}</p>`)
    }
  }

  if (inList) output.push('</ul>')
  return output.join('\n')
}

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────

function TramitePage() {
  const { id } = useParams<{ id: string }>()
  const tramite = tramites.find((t) => t.id === Number(id))

  // Lectura Fácil state
  const [modoLF, setModoLF] = useState(false)
  const [cargandoLF, setCargandoLF] = useState(false)
  const [accesibleData, setAccesibleData] = useState<AccesibleResponse | null>(null)
  const [mdContent, setMdContent] = useState<string | null>(null)
  const [reproduciendo, setReproduciendo] = useState(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      audioRef.current?.pause()
      window.speechSynthesis.cancel()
    }
  }, [])

  if (!tramite) {
    return (
      <Container className="py-5 text-center">
        <h2 style={{ color: 'var(--retys-primary)' }}>Trámite no encontrado</h2>
        <p className="text-muted">El trámite con ID <strong>{id}</strong> no existe en este portal.</p>
        <Link to="/" className="btn btn-tramite mt-2">← Regresar al inicio</Link>
      </Container>
    )
  }

  // ── helpers ────────────────────────────────────────────────────────────────

  const stopAudio = () => {
    audioRef.current?.pause()
    audioRef.current = null
    window.speechSynthesis.cancel()
    setReproduciendo(false)
  }

  const usarWebSpeech = (text: string) => {
    const utt = new SpeechSynthesisUtterance(text.replace(/[#*`]/g, ''))
    utt.lang = 'es-MX'
    utt.onend = () => setReproduciendo(false)
    window.speechSynthesis.speak(utt)
  }

  // ── handlers ───────────────────────────────────────────────────────────────

  const handleToggleLF = async () => {
    if (modoLF) {
      stopAudio()
      setModoLF(false)
      return
    }

    // Already cached — just switch on
    if (accesibleData !== null) {
      setModoLF(true)
      return
    }

    // Fetch from backend
    setCargandoLF(true)
    const data = await consultarAccesible(tramite.homoclave)
    setAccesibleData(data)

    if (data.generado && data.url_documento) {
      try {
        const res = await fetch(`${BASE_URL}/${data.url_documento}`)
        if (res.ok) {
          const text = await res.text()
          setMdContent(text)
        }
      } catch {
        // mdContent stays null — the component will fall back gracefully
      }
    }

    setCargandoLF(false)
    setModoLF(true)
  }

  const handleEscuchar = () => {
    if (reproduciendo) {
      stopAudio()
      return
    }

    setReproduciendo(true)

    if (accesibleData?.url_audio) {
      const audio = new Audio(`${BASE_URL}/${accesibleData.url_audio}`)
      audioRef.current = audio
      audio.onended = () => setReproduciendo(false)
      audio.onerror = () => {
        // Fallback to Web Speech if the MP3 fails
        if (mdContent) usarWebSpeech(mdContent)
        else setReproduciendo(false)
      }
      void audio.play()
    } else if (mdContent) {
      usarWebSpeech(mdContent)
    } else {
      setReproduciendo(false)
    }
  }

  // ─────────────────────────────────────────────────────────────────────────

  return (
    <>
      {/* Encabezado del trámite */}
      <div className="tramite-page-header">
        <Container>
          <Breadcrumb className="mb-2" style={{ '--bs-breadcrumb-divider': "'>'", fontSize: '0.82rem' } as React.CSSProperties}>
            <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/' }} style={{ color: 'rgba(255,255,255,0.75)' }}>
              Inicio
            </Breadcrumb.Item>
            <Breadcrumb.Item linkAs="span" style={{ color: 'rgba(255,255,255,0.75)' }}>
              Trámites y Servicios
            </Breadcrumb.Item>
            <Breadcrumb.Item active style={{ color: '#fff' }}>
              {tramite.titulo}
            </Breadcrumb.Item>
          </Breadcrumb>
          <h1>{tramite.titulo}</h1>
          <div className="d-flex flex-wrap gap-2 align-items-center mt-2">
            <Badge bg="danger" className="badge-tramite">{tramite.dependencia}</Badge>
            <span style={{ fontSize: '0.8rem', opacity: 0.8 }}>ID: {tramite.id}</span>
          </div>
        </Container>
      </div>

      {/* Cuerpo principal */}
      <div className="tramite-detail-body">
        <Container>
          <Row>
            {/* Columna principal */}
            <Col xs={12} lg={8}>

              {/* ── Lectura Fácil toggle ───────────────────────────────────── */}
              <div className="d-flex gap-2 mb-4 align-items-center">
                <Button
                  variant={modoLF ? 'success' : 'outline-success'}
                  size="sm"
                  onClick={() => { void handleToggleLF() }}
                  disabled={cargandoLF}
                >
                  {cargandoLF
                    ? <><Spinner size="sm" className="me-1" />Cargando…</>
                    : modoLF ? '📄 Versión Normal' : '♿ Versión Lectura Fácil'}
                </Button>
                {modoLF && accesibleData?.generado && (
                  <Button
                    variant={reproduciendo ? 'danger' : 'outline-primary'}
                    size="sm"
                    onClick={handleEscuchar}
                  >
                    {reproduciendo ? '⏹ Detener' : '🔊 Escuchar'}
                  </Button>
                )}
              </div>

              {/* ── Contenido condicional ─────────────────────────────────── */}
              {modoLF ? (
                <>
                  {!accesibleData?.generado ? (
                    <Alert variant="info">
                      Esta versión de Lectura Fácil aún no ha sido generada.
                      Un administrador puede generarla desde el{' '}
                      <Alert.Link href="/admin">Panel de Administración</Alert.Link>.
                    </Alert>
                  ) : mdContent ? (
                    <div
                      className="lectura-facil-content p-3 rounded"
                      style={{
                        background: '#f8fff8',
                        border: '2px solid #28a745',
                        lineHeight: 1.8,
                        fontSize: '1rem',
                      }}
                      dangerouslySetInnerHTML={{ __html: markdownToHtml(mdContent) }}
                    />
                  ) : (
                    <Alert variant="warning">
                      No se pudo cargar el documento de Lectura Fácil. Intente de nuevo más tarde.
                    </Alert>
                  )}
                </>
              ) : (
                <>
                  {/* Descripción */}
                  <div className="section-label">Descripción del Trámite</div>
                  <p style={{ fontSize: '0.92rem', lineHeight: 1.7 }}>{tramite.descripcion}</p>

                  <Row className="g-3 mb-3">
                    <Col xs={6} sm={3}>
                      <div style={{ background: 'var(--retys-light-bg)', borderRadius: 6, padding: '0.75rem', textAlign: 'center' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--retys-text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Tiempo</div>
                        <div style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--retys-primary)', marginTop: 4 }}>{tramite.tiempoResolucion}</div>
                      </div>
                    </Col>
                    <Col xs={6} sm={3}>
                      <div style={{ background: 'var(--retys-light-bg)', borderRadius: 6, padding: '0.75rem', textAlign: 'center' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--retys-text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Vigencia</div>
                        <div style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--retys-primary)', marginTop: 4 }}>{tramite.vigencia}</div>
                      </div>
                    </Col>
                    <Col xs={12} sm={6}>
                      <div style={{ background: 'var(--retys-light-bg)', borderRadius: 6, padding: '0.75rem' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--retys-text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: 4 }}>Área responsable</div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--retys-primary)' }}>{tramite.area}</div>
                      </div>
                    </Col>
                  </Row>

                  {/* Fundamento legal */}
                  <div className="section-label">Fundamento Legal</div>
                  <p style={{ fontSize: '0.88rem', lineHeight: 1.7, color: 'var(--retys-text-muted)' }}>{tramite.fundamento}</p>

                  {/* Requisitos */}
                  <div className="section-label">Requisitos</div>
                  <Table bordered hover size="sm" responsive>
                    <thead>
                      <tr>
                        <th style={{ width: 50 }}>#</th>
                        <th>Descripción</th>
                        <th style={{ width: 180 }}>Notas</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tramite.requisitos.map((req) => (
                        <tr key={req.numero}>
                          <td className="text-center fw-bold">{req.numero}</td>
                          <td>{req.descripcion}</td>
                          <td style={{ fontSize: '0.8rem', color: 'var(--retys-text-muted)' }}>
                            {req.notas ?? '—'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>

                  {/* Costos */}
                  <div className="section-label">Costos / Derechos</div>
                  <Table bordered hover size="sm" responsive>
                    <thead>
                      <tr>
                        <th>Concepto</th>
                        <th style={{ width: 130 }}>Monto</th>
                        <th style={{ width: 220 }}>Fundamento</th>
                        <th style={{ width: 180 }}>Forma de Pago</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tramite.costos.map((costo, idx) => (
                        <tr key={idx}>
                          <td>{costo.concepto}</td>
                          <td className="fw-bold text-center">{costo.monto}</td>
                          <td style={{ fontSize: '0.8rem', color: 'var(--retys-text-muted)' }}>{costo.fundamento}</td>
                          <td style={{ fontSize: '0.85rem' }}>{costo.formaPago}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>

                  {/* Documentos / Descargas */}
                  <div className="section-label">Documentos para Descargar</div>
                  <div className="mb-2">
                    <p style={{ fontSize: '0.85rem', color: 'var(--retys-text-muted)', marginBottom: '0.75rem' }}>
                      Descargue los formatos y documentos necesarios para realizar este trámite:
                    </p>
                    <div className="d-flex flex-wrap gap-2">
                      {tramite.documentos.map((doc, idx) => (
                        <a
                          key={idx}
                          href={doc.archivo}
                          download={doc.nombre}
                          className={`btn-download${idx > 0 ? ' btn-download-secondary' : ''}`}
                        >
                          ⬇ {doc.nombre}
                          <span
                            style={{
                              background: 'rgba(255,255,255,0.2)',
                              borderRadius: 3,
                              padding: '0 5px',
                              fontSize: '0.72rem',
                              marginLeft: 4,
                            }}
                          >
                            {doc.tipo}
                          </span>
                        </a>
                      ))}
                    </div>
                  </div>
                </>
              )}

            </Col>

            {/* Sidebar */}
            <Col xs={12} lg={4} className="mt-4 mt-lg-0">

              {/* Contacto */}
              <div className="tramite-sidebar mb-3">
                <h6>📞 Información de Contacto</h6>
                <ul>
                  <li>
                    <strong>Dependencia:</strong><br />
                    <span style={{ fontSize: '0.82rem' }}>{tramite.dependencia}</span>
                  </li>
                  <li>
                    <strong>Dirección:</strong><br />
                    <span style={{ fontSize: '0.82rem' }}>{tramite.contacto.direccion}</span>
                  </li>
                  <li>
                    <strong>Teléfono:</strong><br />
                    <span style={{ fontSize: '0.82rem' }}>{tramite.contacto.telefono}</span>
                  </li>
                  <li>
                    <strong>Correo electrónico:</strong><br />
                    <a href={`mailto:${tramite.contacto.email}`} style={{ fontSize: '0.82rem' }}>
                      {tramite.contacto.email}
                    </a>
                  </li>
                  <li style={{ borderBottom: 'none' }}>
                    <strong>Horario de atención:</strong><br />
                    <span style={{ fontSize: '0.82rem' }}>{tramite.contacto.horario}</span>
                  </li>
                </ul>
              </div>

              {/* Trámites relacionados */}
              {tramite.tramitesRelacionados.length > 0 && (
                <div className="tramite-sidebar mb-3">
                  <h6>🔗 Trámites Relacionados</h6>
                  <ul>
                    {tramite.tramitesRelacionados.map((rel) => (
                      <li key={rel.id} style={{ borderBottom: 'none', paddingBottom: '0.5rem' }}>
                        <Link to={`/Portal/TyS/${rel.id}`}>{rel.titulo}</Link>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Nota importante */}
              <div
                style={{
                  background: '#fff8e1',
                  border: '1px solid #f5a800',
                  borderLeft: '4px solid #f5a800',
                  borderRadius: 6,
                  padding: '1rem',
                  fontSize: '0.82rem',
                  color: '#555',
                }}
              >
                <strong style={{ color: '#b37700', display: 'block', marginBottom: '0.4rem' }}>
                  ⚠ Aviso Importante
                </strong>
                Verifique la vigencia de todos los documentos requeridos antes de presentarse.
                Los requisitos pueden actualizarse. Consulte directamente con la dependencia
                para confirmar la información más reciente.
              </div>

            </Col>
          </Row>
        </Container>
      </div>
    </>
  )
}

export default TramitePage
