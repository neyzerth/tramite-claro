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
    id: 1634,
    dependencia: 'Comisión Estatal de Servicios Públicos de Tijuana',
    titulo: 'Registro o Revalidación de Exención de Permiso de Descarga de Aguas Residuales',
    descripcion: 'Para comercios y empresas de servicios que no generan aguas residuales de procesos productivos.',
  },
  {
    id: 661,
    dependencia: 'Secretaría de Hacienda de Baja California',
    titulo: 'Expedición de Licencia de Conducir',
    descripcion: 'Obtén tu licencia de conducir para automovilista, motociclista, chofer o menor de edad.',
  },
  {
    id: 1238,
    dependencia: 'Centro de Justicia para las Mujeres',
    titulo: 'Atención Integral a Mujeres Víctimas de Violencia',
    descripcion: 'Asesoría psicológica, legal, trabajo social, atención médica y acompañamiento integral. Sin costo.',
  },
  {
    id: 1131,
    dependencia: 'Secretaría Anticorrupción y Buen Gobierno',
    titulo: 'Constancia de no inhabilitación',
    descripcion: 'Acredita que no cuentas con inhabilitación vigente para desempeñar un empleo, cargo o comisión.',
  },
  {
    id: 1618,
    dependencia: 'Secretaría de Seguridad Ciudadana',
    titulo: 'Expedición de Constancia de Antecedentes Penales',
    descripcion: 'Documento que hace constar si tienes o no antecedentes penales del fuero común en Baja California.',
  },
  {
    id: 0,
    dependencia: 'RETyS Baja California',
    titulo: 'Más trámites disponibles',
    descripcion: 'Consulta el catálogo completo del Registro Estatal de Trámites y Servicios de Baja California.',
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
