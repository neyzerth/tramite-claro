import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

const dependencias = [
  'Registro Civil',
  'Secretaría de Salud',
  'Secretaría de Educación',
  'Secretaría de Finanzas',
  'Secretaría de Desarrollo Urbano',
  'Fiscalía General del Estado',
  'Secretaría de Economía',
  'Secretaría del Trabajo',
  'IMSS Baja California',
  'Comisión Estatal del Agua',
  'Secretaría de Seguridad',
  'Secretaría de Turismo',
  'ISSSTECALI',
  'Secretaría de Agricultura',
  'Municipio de Tijuana',
  'Municipio de Mexicali',
  'Municipio de Ensenada',
  'Municipio de Tecate',
  'Municipio de Rosarito',
]

function TramitesSection() {
  return (
    <section className="category-section" id="servicios">
      <Container>
        <h2 className="section-title">Dependencias y Organismos</h2>
        <Row>
          <Col xs={12}>
            <div className="d-flex flex-wrap">
              {dependencias.map((dep) => (
                <a key={dep} href="#" className="category-pill">
                  {dep}
                </a>
              ))}
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  )
}

export default TramitesSection
