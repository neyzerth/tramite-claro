import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Link } from 'react-router-dom'

function Footer() {
  return (
    <>
      <footer className="footer-main">
        <Container>
          <Row className="g-4">
            {/* Col 1: Logo + descripción */}
            <Col xs={12} md={4} lg={3}>
              <div className="d-flex align-items-center gap-2 mb-3">
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: '50%',
                    background: 'rgba(255,255,255,0.15)',
                    border: '2px solid rgba(255,255,255,0.3)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.4rem',
                  }}
                >
                  🏛
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#fff' }}>RETyS</div>
                  <div style={{ fontSize: '0.72rem', opacity: 0.8 }}>Baja California</div>
                </div>
              </div>
              <p style={{ fontSize: '0.82rem', lineHeight: 1.6, opacity: 0.85 }}>
                Registro Estatal de Trámites y Servicios del Gobierno del Estado de
                Baja California. Transparencia y acceso ciudadano.
              </p>
            </Col>

            {/* Col 2: Links útiles */}
            <Col xs={6} md={2} lg={2}>
              <h6>Links Útiles</h6>
              <Link to="/">Inicio</Link>
              <a href="#">Trámites y Servicios</a>
              <a href="#">Dependencias</a>
              <a href="#">Consulta tu Trámite</a>
              <a href="#">Preguntas Frecuentes</a>
              <a href="#">Mapa del Sitio</a>
            </Col>

            {/* Col 3: Trámites destacados */}
            <Col xs={6} md={3} lg={3}>
              <h6>Trámites Destacados</h6>
              <Link to="/Portal/TyS/1650">Registro Civil</Link>
              <Link to="/Portal/TyS/661">Licencia de Funcionamiento</Link>
              <Link to="/Portal/TyS/652">Uso de Suelo</Link>
              <Link to="/Portal/TyS/1618">Certificado de Estudios</Link>
              <Link to="/Portal/TyS/1582">No Antecedentes Penales</Link>
            </Col>

            {/* Col 4: Contacto + Redes */}
            <Col xs={12} md={3} lg={4}>
              <h6>Contacto</h6>
              <p style={{ fontSize: '0.82rem', marginBottom: '0.25rem' }}>
                📍 Blvd. Lázaro Cárdenas 1477, Mexicali, B.C.
              </p>
              <p style={{ fontSize: '0.82rem', marginBottom: '0.25rem' }}>
                📞 (686) 558-3300
              </p>
              <p style={{ fontSize: '0.82rem', marginBottom: '1rem' }}>
                ✉️ retys@bajacalifornia.gob.mx
              </p>
              <h6>Redes Sociales</h6>
              <div className="footer-social">
                <a href="#" rel="noopener">Facebook</a>
                <a href="#" rel="noopener">Twitter/X</a>
                <a href="#" rel="noopener">YouTube</a>
              </div>
            </Col>
          </Row>
        </Container>
      </footer>

      {/* Footer Bottom */}
      <div className="footer-bottom">
        <Container>
          <div className="d-flex flex-column flex-md-row justify-content-between align-items-center gap-1">
            <span>
              © {new Date().getFullYear()} Gobierno del Estado de Baja California — RETyS. Todos los derechos reservados.
            </span>
            <div className="d-flex gap-3">
              <a href="#">Aviso de Privacidad</a>
              <a href="#">Términos de Uso</a>
              <a href="#">Accesibilidad</a>
            </div>
          </div>
        </Container>
      </div>
    </>
  )
}

export default Footer
