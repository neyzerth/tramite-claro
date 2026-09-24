import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

interface NewsItem {
  id: number
  date: string
  title: string
  excerpt: string
}

const newsItems: NewsItem[] = [
  {
    id: 1,
    date: '15 de enero, 2025',
    title: 'Nuevos trámites disponibles en línea para ciudadanos de BC',
    excerpt: 'El Gobierno del Estado incorpora 12 nuevos trámites al portal RETyS para facilitar la gestión ciudadana sin necesidad de presentarse a las oficinas.',
  },
  {
    id: 2,
    date: '8 de enero, 2025',
    title: 'Actualización del sistema de consulta de trámites',
    excerpt: 'A partir de esta fecha el portal cuenta con una interfaz mejorada para el seguimiento del estado de cada trámite en tiempo real.',
  },
  {
    id: 3,
    date: '20 de diciembre, 2024',
    title: 'Horarios especiales de atención en temporada decembrina',
    excerpt: 'Las oficinas de atención ciudadana operarán con horarios reducidos del 23 de diciembre al 3 de enero. Consulta los horarios en cada dependencia.',
  },
]

function NewsSection() {
  return (
    <section className="news-section" id="noticias">
      <Container>
        <h2 className="section-title">Avisos y Noticias</h2>
        <Row className="g-3">
          {newsItems.map((item) => (
            <Col key={item.id} xs={12} md={4}>
              <div className="news-card">
                <div className="news-img-placeholder">📰</div>
                <div className="p-3">
                  <p className="news-date">{item.date}</p>
                  <h6 className="news-title">{item.title}</h6>
                  <p className="news-excerpt">{item.excerpt}</p>
                  <a href="#" className="news-link">Leer más →</a>
                </div>
              </div>
            </Col>
          ))}
        </Row>
      </Container>
    </section>
  )
}

export default NewsSection
