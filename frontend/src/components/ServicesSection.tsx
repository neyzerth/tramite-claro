import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Link } from 'react-router-dom'

interface QuickItem {
  icon: string
  label: string
  href: string
}

const items: QuickItem[] = [
  { icon: '📋', label: 'Trámites', href: '#tramites' },
  { icon: '⚙️', label: 'Servicios', href: '#servicios' },
  { icon: '🔍', label: 'Consultar Estado', href: '#' },
  { icon: '🏢', label: 'Dependencias', href: '#' },
  { icon: '📞', label: 'Contáctanos', href: '#' },
  { icon: '📄', label: 'Descargas', href: '#' },
]

function QuickAccess() {
  return (
    <section className="quick-access" id="inicio">
      <Container>
        <Row className="justify-content-center">
          {items.map((item) => (
            <Col key={item.label} xs={4} sm={3} md={2} className="mb-2">
              <a href={item.href} className="quick-access-item">
                <div className="qa-icon">{item.icon}</div>
                <span>{item.label}</span>
              </a>
            </Col>
          ))}
        </Row>
      </Container>
    </section>
  )
}

// ===== Services Section =====
interface TramiteCard {
  id: number
  dependencia: string
  titulo: string
  descripcion: string
}

const tramitesDestacados: TramiteCard[] = [
  {
    id: 1650,
    dependencia: 'Registro Civil',
    titulo: 'Solicitud de Inscripción al Registro Civil',
    descripcion: 'Registro de nacimientos, matrimonios, defunciones y otros actos del estado civil de las personas.',
  },
  {
    id: 661,
    dependencia: 'Licencias y Permisos',
    titulo: 'Licencia de Funcionamiento',
    descripcion: 'Obtén el permiso para operar un establecimiento comercial, industrial o de servicios en el estado.',
  },
  {
    id: 652,
    dependencia: 'Desarrollo Urbano',
    titulo: 'Permiso de Uso de Suelo',
    descripcion: 'Autorización para el uso o cambio de uso de suelo de un predio conforme a los planes de desarrollo urbano.',
  },
  {
    id: 1618,
    dependencia: 'Secretaría de Educación',
    titulo: 'Certificado de Estudios',
    descripcion: 'Solicita la expedición de certificados y constancias de estudios de nivel básico, medio y superior.',
  },
  {
    id: 1582,
    dependencia: 'Fiscalía General del Estado',
    titulo: 'Constancia de No Antecedentes Penales',
    descripcion: 'Documento oficial que certifica que el solicitante no cuenta con antecedentes penales en el estado.',
  },
  {
    id: 0,
    dependencia: 'Secretaría de Finanzas',
    titulo: 'Pago de Derechos y Contribuciones',
    descripcion: 'Realiza el pago de derechos, contribuciones y aprovechamientos del estado a través del portal oficial.',
  },
]

function ServicesSection() {
  return (
    <section id="tramites" style={{ padding: '2.5rem 0', background: '#fff' }}>
      <Container>
        <h2 className="section-title">Trámites y Servicios Más Consultados</h2>
        <Row className="g-3">
          {tramitesDestacados.map((t) => (
            <Col key={t.id} xs={12} sm={6} lg={4}>
              <div className="tramite-card card h-100">
                <div className="card-header">{t.dependencia}</div>
                <div className="card-body d-flex flex-column">
                  <h5 className="card-title">{t.titulo}</h5>
                  <p className="card-text flex-grow-1">{t.descripcion}</p>
                  {t.id > 0 ? (
                    <Link to={`/Portal/TyS/${t.id}`} className="btn btn-tramite align-self-start">
                      Ver trámite →
                    </Link>
                  ) : (
                    <a href="#" className="btn btn-tramite align-self-start">
                      Ver trámite →
                    </a>
                  )}
                </div>
              </div>
            </Col>
          ))}
        </Row>
      </Container>
    </section>
  )
}

export { QuickAccess, ServicesSection }
export default ServicesSection
