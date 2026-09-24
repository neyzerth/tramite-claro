# tramite-claro — Frontend

Clon estructural del portal **RETyS** (Registro Estatal de Trámites y Servicios) de Baja California, construido con React 19 + Vite + TypeScript + Bootstrap 5.

> Portal original de referencia: https://retys.bajacalifornia.gob.mx

---

## 🏛 Descripción del Proyecto

**tramite-claro** es una réplica estructural del portal gubernamental RETyS de Baja California. Replica fielmente el layout, secciones, navegación y estructura de información del sitio original, incluyendo las páginas de detalle de los trámites más consultados con sus respectivos documentos descargables.

El proyecto **no incluye** lógica de negocio, llamadas a APIs ni autenticación — su propósito es estructural y visual.

---

## ⚙️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|---|---|---|
| React | 19.x | Framework UI |
| Vite | 8.x | Bundler y servidor de desarrollo |
| TypeScript | 6.x | Tipado estático |
| Bootstrap | 5.3.x | Framework CSS |
| react-bootstrap | 2.10.x | Componentes Bootstrap para React |
| React Router DOM | 7.x | Navegación entre páginas |

---

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

La aplicación quedará disponible en `http://localhost:5173`.

---

## 📁 Estructura del Proyecto

```
frontend/
├── public/
│   └── downloads/              # Archivos PDF descargables por trámite
│       ├── tramite-1650-solicitud.pdf
│       ├── tramite-661-solicitud.pdf
│       ├── tramite-661-reglamento.pdf
│       ├── tramite-652-solicitud.pdf
│       ├── tramite-1618-solicitud.pdf
│       ├── tramite-1582-solicitud.pdf
│       └── tramite-1582-requisitos.pdf
├── src/
│   ├── App.tsx                 # Configuración de rutas (BrowserRouter)
│   ├── main.tsx                # Punto de entrada — importa Bootstrap y CSS custom
│   ├── assets/
│   │   ├── custom.css          # Variables CSS y overrides del tema RETyS
│   │   └── site-map.md         # Documentación de la estructura del sitio original
│   ├── components/             # Componentes reutilizables
│   │   ├── Header.tsx          # Top bar + Navbar responsivo + buscador
│   │   ├── Hero.tsx            # Banner principal con CTA
│   │   ├── ServicesSection.tsx # Acceso rápido + cards de trámites destacados
│   │   ├── TramitesSection.tsx # Pills de dependencias y organismos
│   │   ├── NewsSection.tsx     # Sección de noticias y avisos
│   │   └── Footer.tsx          # Pie de página con columnas y redes sociales
│   ├── layouts/
│   │   └── MainLayout.tsx      # Layout compartido (Header + Outlet + Footer)
│   ├── pages/
│   │   ├── HomePage.tsx        # Página principal — compone todas las secciones
│   │   └── TramitePage.tsx     # Página de detalle de trámite individual
│   └── data/
│       └── tramites.ts         # Datos estáticos de los 5 trámites implementados
```

---

## 🗺 Páginas Implementadas

### Página Principal (`/`)
Replica la página de inicio del portal RETyS con las siguientes secciones:

1. **Top Bar** — Barra institucional con links de navegación secundaria
2. **Navbar** — Menú principal con logo, navegación y buscador responsivo
3. **Hero / Banner** — Cabecera con título del portal y llamadas a la acción
4. **Acceso Rápido** — Íconos de acceso directo a las secciones principales
5. **Trámites Destacados** — Grid de 6 cards con los trámites más consultados y links directos a sus páginas de detalle
6. **Dependencias y Organismos** — Pills filtrables por dependencia del gobierno
7. **Noticias y Avisos** — Sección de comunicados institucionales
8. **Footer** — Pie de página de 4 columnas con links, contacto y redes sociales

### Páginas de Detalle de Trámite (`/Portal/TyS/:id`)

Cada página incluye:
- **Breadcrumb** de navegación
- **Encabezado** con título, dependencia responsable e ID del trámite
- **Descripción** completa del trámite
- **Indicadores** de tiempo de resolución, vigencia y área responsable
- **Fundamento legal**
- **Tabla de requisitos** numerada
- **Tabla de costos/derechos** con montos y formas de pago
- **Botones de descarga** de formatos oficiales (archivos PDF)
- **Sidebar** con información de contacto, trámites relacionados y aviso importante

#### Trámites disponibles

| ID | Trámite | Dependencia |
|---|---|---|
| 1650 | Solicitud de Inscripción al Registro Civil | Registro Civil del Estado de BC |
| 661 | Licencia de Funcionamiento | Dirección de Licencias y Permisos |
| 652 | Permiso de Uso de Suelo | Secretaría de Desarrollo Urbano |
| 1618 | Expedición de Certificado de Estudios | SEPBC |
| 1582 | Constancia de No Antecedentes Penales | Fiscalía General del Estado |

---

## ⬇️ Descargas de Archivos

Los botones de descarga en las páginas de trámite utilizan elementos `<a href="..." download>` que apuntan a archivos PDF locales servidos desde `public/downloads/`. Al hacer clic, el navegador inicia la descarga automáticamente sin abrir el archivo en el visor del navegador.

> **Nota:** Los archivos en `public/downloads/` son placeholders de texto para efectos de desarrollo. En producción deben reemplazarse con los formatos oficiales reales.

---

## 🎨 Sistema de Diseño

El tema visual replica los colores institucionales del Gobierno de Baja California:

| Variable CSS | Color | Uso |
|---|---|---|
| `--retys-primary` | `#003876` | Azul institucional (navbar, headers, botones) |
| `--retys-secondary` | `#e8161e` | Rojo (acentos, bordes, botones secundarios) |
| `--retys-accent` | `#f5a800` | Dorado (avisos, destacados) |
| `--retys-light-bg` | `#f4f6f9` | Fondo de secciones alternas |

Los estilos custom están definidos en [`src/assets/custom.css`](src/assets/custom.css). Bootstrap 5 es la base; `custom.css` solo agrega overrides necesarios para el tema RETyS.

---

## 📋 Notas de Desarrollo

- **Sin estado global**: No se usa Redux ni Context API. Los datos son texto estático en `src/data/tramites.ts`.
- **Sin llamadas a API**: Toda la información es estática para esta etapa estructural.
- **TypeScript strict**: El proyecto compila con `tsc --noEmit` sin errores.
- **Linting**: Se usa `oxlint` — ejecutar con `npm run lint`.
- **Componentes Bootstrap**: Se importan individualmente desde `react-bootstrap` para optimizar el bundle (e.g. `import Container from 'react-bootstrap/Container'`).

---

## 📄 Documentación Adicional

- [`retys-clone-plan.md`](retys-clone-plan.md) — Plan de desarrollo con las 10 sub-tareas ejecutadas
- [`src/assets/site-map.md`](src/assets/site-map.md) — Mapa de estructura del sitio original analizado

---

## 📜 Licencia

Ver archivo [LICENSE](LICENSE).
