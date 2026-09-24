import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Link } from 'react-router-dom'

function Hero() {
  return (
    <section className="hero-banner">
      <Container>
        <Row className="align-items-center">
          <Col md={8} lg={7}>
            <p className="mb-1" style={{ fontSize: '0.85rem', opacity: 0.8, letterSpacing: '0.04em' }}>
              GOBIERNO DEL ESTADO DE BAJA CALIFORNIA
            </p>
            <h1>Registro Estatal de Trámites y Servicios</h1>
            <p>
              Consulta, descarga y realiza tus trámites y servicios gubernamentales
              de forma rápida, sencilla y transparente.
            </p>
            <div className="d-flex flex-wrap gap-2 mt-3">
              <Link to="/" className="btn btn-hero">
                Consultar Trámites
              </Link>
              <a href="#" className="btn" style={{ background: 'rgba(255,255,255,0.15)', color: '#fff', borderRadius: 4, padding: '0.55rem 1.4rem', fontWeight: 600, fontSize: '0.95rem' }}>
                ¿Cómo funciona?
              </a>
            </div>
          </Col>
          <Col md={4} lg={5} className="d-none d-md-flex justify-content-center">
            {/* Escudo / Ilustración placeholder */}
            <div
              style={{
                width: 170,
                height: 170,
                borderRadius: '50%',
                background: 'rgba(255,255,255,0.12)',
                border: '3px solid rgba(255,255,255,0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
                color: '#fff',
                textAlign: 'center',
              }}
            >
              <div style={{ fontSize: '3.5rem', lineHeight: 1 }}>🏛</div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.5rem', opacity: 0.85 }}>
                Baja California
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  )
}

export default Hero
