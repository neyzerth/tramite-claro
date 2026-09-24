import { BrowserRouter, Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import HomePage from './pages/HomePage'
import TramitePage from './pages/TramitePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/Portal/TyS/:id" element={<TramitePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
