import Hero from '../components/Hero'
import { QuickAccess } from '../components/ServicesSection'
import ServicesSection from '../components/ServicesSection'
import TramitesSection from '../components/TramitesSection'
import NewsSection from '../components/NewsSection'

function HomePage() {
  return (
    <>
      <Hero />
      <QuickAccess />
      <ServicesSection />
      <TramitesSection />
      <NewsSection />
    </>
  )
}

export default HomePage
