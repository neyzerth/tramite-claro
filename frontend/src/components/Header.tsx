import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import NavDropdown from 'react-bootstrap/NavDropdown'
import { Link, NavLink } from 'react-router-dom'

function Header() {
  return (
    <>
      {/* Top Bar */}
      <div className="top-bar d-none d-md-block">
        <Container>
          <div className="d-flex justify-content-between align-items-center">
            <span>Gobierno del Estado de Baja California</span>
            <div className="d-flex gap-3">
              <Link to="/">Inicio</Link>
              <a href="#">Mapa del sitio</a>
              <a href="#">Accesibilidad</a>
            </div>
          </div>
        </Container>
      </div>

      {/* Main Navbar */}
      <Navbar expand="lg" className="navbar-retys py-2">
        <Container>
          <Navbar.Brand as={Link} to="/" className="d-flex align-items-center gap-3">
            {/* Logo Gobierno BC — placeholder texto */}
            <div
              style={{
                width: 52,
                height: 52,
                borderRadius: '50%',
                background: 'var(--retys-primary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                fontWeight: 700,
                fontSize: '0.7rem',
                textAlign: 'center',
                lineHeight: 1.2,
              }}
            >
              GOB<br />BC
            </div>
            <div>
              <div style={{ fontSize: '0.65rem', color: 'var(--retys-text-muted)', lineHeight: 1.1 }}>
                Gobierno del Estado de
              </div>
              <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--retys-primary)', lineHeight: 1.2 }}>
                Baja California
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--retys-secondary)', fontWeight: 600, lineHeight: 1.1 }}>
                RETyS
              </div>
            </div>
          </Navbar.Brand>

          <Navbar.Toggle aria-controls="navbar-main" />

          <Navbar.Collapse id="navbar-main">
            <Nav className="mx-auto">
              <Nav.Link as={NavLink} to="/" end>
                Inicio
              </Nav.Link>
              <NavDropdown title="Trámites y Servicios" id="nav-tramites">
                <NavDropdown.Item as={Link} to="/Portal/TyS/1650">
                  Registro Civil
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/Portal/TyS/661">
                  Licencias y Permisos
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/Portal/TyS/652">
                  Uso de Suelo
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/Portal/TyS/1618">
                  Educación
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/Portal/TyS/1582">
                  No Antecedentes Penales
                </NavDropdown.Item>
              </NavDropdown>
              <Nav.Link href="#">Dependencias</Nav.Link>
              <Nav.Link href="#">Consulta tu Trámite</Nav.Link>
              <Nav.Link href="#">Contáctanos</Nav.Link>
            </Nav>

            {/* Buscador */}
            <form className="d-flex align-items-center" onSubmit={(e) => e.preventDefault()}>
              <input
                type="search"
                placeholder="Buscar trámite..."
                className="search-input"
                aria-label="Buscar"
              />
              <button type="submit" className="search-btn ms-1">
                Buscar
              </button>
            </form>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default Header
