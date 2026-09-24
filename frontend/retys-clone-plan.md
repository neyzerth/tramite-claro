# Plan: Clon Estructural RETyS — tramite-claro

## Resumen General

**Objetivo:** Construir una réplica estructural en React del sitio https://retys.bajacalifornia.gob.mx y de 5 páginas de detalle de trámites específicos, incluyendo la funcionalidad de los botones de descarga de archivos. Stack: React + Vite + Bootstrap 5 + TypeScript + React Router.

**Alcance:**
- Scaffolding del proyecto React con Vite, TypeScript y React Router
- Análisis y mapeo de la estructura del sitio original (página principal + 5 páginas de trámite)
- Implementación de componentes estructurales por sección para la página principal
- Implementación de páginas de detalle de trámite con estructura replicada
- Navegación entre páginas con React Router
- Funcionalidad operativa de los botones "Descargar archivo" en las páginas de trámite
- Sin lógica de negocio adicional más allá de la descarga de archivos

**Páginas de trámite a replicar:**
- https://retys.bajacalifornia.gob.mx/Portal/TyS/1650
- https://retys.bajacalifornia.gob.mx/Portal/TyS/661
- https://retys.bajacalifornia.gob.mx/Portal/TyS/652
- https://retys.bajacalifornia.gob.mx/Portal/TyS/1618
- https://retys.bajacalifornia.gob.mx/Portal/TyS/1582

**Fuera de alcance:**
- Funcionalidades interactivas adicionales (búsqueda real, login, formularios de trámite)
- Backend o integración con servicios dinámicos
- Accesibilidad avanzada o SEO
- Animaciones o transiciones
- Páginas de trámite fuera de las 5 listadas

**Stack recomendado:** React 18 + Vite + TypeScript + Bootstrap 5 + react-bootstrap + React Router v6

---

## Sub-Tarea 1 — Scaffolding del Proyecto

**Status:** [x] done

### Intent
Inicializar el proyecto React con Vite y TypeScript, instalar las dependencias de Bootstrap 5 y configurar la estructura de carpetas base para el desarrollo por componentes.

### Expected Outcomes
- Proyecto React funcionando en `localhost` con `npm run dev`
- Bootstrap 5 importado y activo globalmente
- Estructura de carpetas definida: `src/components/`, `src/layouts/`, `src/assets/`
- `App.tsx` limpio y listo para recibir componentes
- `.gitignore` actualizado para ignorar `node_modules` y `dist`

### Todo List
1. Ejecutar `npm create vite@latest . -- --template react-ts` en la raíz del proyecto
2. Ejecutar `npm install` para instalar dependencias base
3. Ejecutar `npm install react-bootstrap bootstrap` para instalar Bootstrap 5
4. Ejecutar `npm install react-router-dom` para instalar React Router v6
5. Importar Bootstrap en `src/main.tsx`: `import 'bootstrap/dist/css/bootstrap.min.css'`
6. Crear estructura de carpetas:
   - `src/components/` — componentes reutilizables (Header, Footer, etc.)
   - `src/pages/` — páginas completas (HomePage, TramitePage)
   - `src/layouts/` — layout compartido con Header y Footer
   - `src/assets/` — imágenes, logos, fuentes, archivos descargables (PDFs placeholder)
7. Configurar `App.tsx` con `<BrowserRouter>` y rutas base
8. Verificar que `npm run dev` corre sin errores

### Relevant Context
- Raíz del proyecto: `c:\vsc_codes\Hackathon\tramite-claro\frontend`
- Rama activa: `Front-Estructura`
- No existe `package.json` aún — el proyecto está vacío

---

## Sub-Tarea 2 — Análisis y Mapa de Estructura del Sitio Original

**Status:** [x] done

### Intent
Documentar exhaustivamente la estructura visual y de componentes de la página principal y de las 5 páginas de trámite. Este mapa guía el desarrollo de todas las sub-tareas siguientes.

### Expected Outcomes
- Documento `site-map.md` en la raíz del proyecto con la estructura completa
- Secciones de la página principal documentadas en orden top-to-bottom
- Estructura de cada una de las 5 páginas de trámite documentada
- Identificación de secciones compartidas entre páginas de trámite (componentes reutilizables)
- Identificación y documentación de los botones de descarga: qué archivos sirven, formato (PDF, DOC, etc.) y URL de descarga
- Confirmación de la versión de Bootstrap usada por el sitio original

### Todo List
1. Abrir https://retys.bajacalifornia.gob.mx en un navegador
2. Inspeccionar el HTML con DevTools (F12) — identificar las secciones principales del `<body>`
3. Inspeccionar el `<head>` para confirmar si usa Bootstrap y qué versión (buscar `bootstrap.min.css` en Sources)
4. Documentar la página principal en orden top-to-bottom:
   - Header / Navbar
   - Banner / Hero
   - Sección de servicios destacados
   - Sección de trámites o categorías
   - Sección de noticias/avisos (si existe)
   - Footer
5. Abrir cada una de las 5 páginas de trámite y documentar para cada una:
   - Título del trámite
   - Secciones de la página (descripción, requisitos, costos, documentos, etc.)
   - Botones de descarga: texto del botón, URL del archivo, tipo de archivo
   - Elementos estructurales únicos vs. compartidos entre las 5 páginas
6. Anotar clases CSS relevantes, colores y fuentes del sitio original
7. Crear `site-map.md` con todo lo documentado (página principal + 5 páginas de trámite)
8. Revisar y aprobar el mapa antes de continuar con la Sub-Tarea 3

### Relevant Context
- El resultado de esta sub-tarea es el insumo principal para Sub-Tareas 3–9
- Las 5 páginas de trámite probablemente comparten la misma estructura base → un único componente `TramitePage` con datos diferentes
- Los botones de descarga del sitio original apuntan a URLs con archivos reales — documentar esas URLs para decidir si se usan archivos locales o se mantienen los links externos

---

## Sub-Tarea 3 — Componente Header / Navbar

**Status:** [x] done

### Intent
Implementar el encabezado de la página con el logo del gobierno, menú de navegación y buscador, replicando la estructura exacta del sitio original.

### Expected Outcomes
- Componente `src/components/Header.tsx` creado
- Navbar responsivo con logo, links de menú y buscador (input visible, sin lógica)
- Se ve correctamente en desktop y mobile (menú hamburguesa de Bootstrap)
- Integrado en `App.tsx`

### Todo List
1. Crear `src/components/Header.tsx`
2. Usar `Navbar`, `Container`, `Nav`, `NavLink` de `react-bootstrap`
3. Agregar logo del gobierno de BC (placeholder `<img>` si no se tiene el asset)
4. Replicar los links del menú principal según el mapa de Sub-Tarea 2
5. Agregar campo de búsqueda como elemento visual (sin `onSubmit`)
6. Importar y renderizar `<Header />` en `App.tsx`
7. Verificar responsividad en viewport móvil

### Relevant Context
- Ver `site-map.md` para los links exactos del menú
- Usar componentes de `react-bootstrap` para mantener coherencia con Bootstrap 5

---

## Sub-Tarea 4 — Componente Hero / Banner Principal

**Status:** [x] done

### Intent
Implementar la sección hero/banner que aparece inmediatamente debajo del header, que típicamente incluye una imagen de fondo, título y llamada a la acción visual.

### Expected Outcomes
- Componente `src/components/Hero.tsx` creado
- Banner con imagen de fondo (placeholder si no hay asset), título y subtítulo
- Layout replicado según el sitio original
- Integrado en `App.tsx` debajo del `<Header />`

### Todo List
1. Crear `src/components/Hero.tsx`
2. Replicar dimensiones y layout del banner según Sub-Tarea 2
3. Usar `Container`, `Row`, `Col` de `react-bootstrap` para el layout
4. Agregar `<img>` o `background-image` CSS para el banner (placeholder aceptable)
5. Agregar título, subtítulo y botón CTA como texto estático
6. Integrar `<Hero />` en `App.tsx`

### Relevant Context
- Ver `site-map.md` para dimensiones y contenido del banner

---

## Sub-Tarea 5 — Secciones de Contenido Principal

**Status:** [x] done

### Intent
Implementar todas las secciones de contenido de la página principal: servicios/trámites destacados, categorías, noticias/avisos. Cada sección será su propio componente.

### Expected Outcomes
- Componentes creados según la estructura del mapa (mínimo 2-3 secciones)
- Cards, listas y tablas estructuralmente correctas usando componentes de Bootstrap
- Todos los componentes integrados en `App.tsx` en el orden correcto
- Contenido de placeholder coherente con el sitio original

### Todo List
1. Crear `src/components/ServicesSection.tsx` — sección de servicios con cards
2. Crear `src/components/TramitesSection.tsx` — sección de trámites/categorías
3. Crear `src/components/NewsSection.tsx` — sección de noticias/avisos (si existe en el original)
4. Para cada componente: usar `Card`, `Row`, `Col`, `Container` de `react-bootstrap`
5. Usar texto y datos de placeholder (no datos reales)
6. Integrar todos los componentes en `App.tsx` en el orden correcto según el mapa
7. Verificar visualmente que el orden y estructura coincide con el sitio original

### Relevant Context
- Ver `site-map.md` para el número exacto de secciones y su contenido
- Priorizar fidelidad de estructura sobre fidelidad de contenido

---

## Sub-Tarea 6 — Componente Footer

**Status:** [x] done

### Intent
Implementar el pie de página con links institucionales, información de contacto y redes sociales, replicando la estructura del footer original.

### Expected Outcomes
- Componente `src/components/Footer.tsx` creado
- Footer con columnas de links, info de contacto e íconos de redes sociales (estructura visual)
- Integrado en `App.tsx` al final de la página
- Visualmente consistente con el sitio original

### Todo List
1. Crear `src/components/Footer.tsx`
2. Usar `Container`, `Row`, `Col` de `react-bootstrap` para el layout de columnas
3. Replicar las columnas de links según `site-map.md`
4. Agregar íconos de redes sociales como texto o placeholder (sin íconos externos por ahora)
5. Integrar `<Footer />` en `App.tsx` como último elemento
6. Verificar visualmente contra el sitio original

### Relevant Context
- Ver `site-map.md` para la estructura exacta del footer

---

## Sub-Tarea 7 — Configuración de Rutas con React Router

**Status:** [x] done

### Intent
Configurar React Router v6 para que la aplicación tenga navegación entre la página principal y las 5 páginas de detalle de trámite, usando un layout compartido con Header y Footer.

### Expected Outcomes
- `src/layouts/MainLayout.tsx` creado con `<Header />`, `<Outlet />` y `<Footer />`
- `src/pages/HomePage.tsx` — agrupa los componentes de la página principal
- `src/pages/TramitePage.tsx` — página de detalle de trámite (recibe ID como parámetro de ruta)
- Rutas configuradas en `App.tsx`:
  - `/` → `HomePage`
  - `/Portal/TyS/:id` → `TramitePage`
- Navegación funcional entre página principal y páginas de trámite
- Header y Footer visibles en todas las páginas

### Todo List
1. Crear `src/layouts/MainLayout.tsx` usando `<Outlet />` de React Router
2. Crear `src/pages/HomePage.tsx` — importar y componer los componentes de las Sub-Tareas 3–6
3. Crear `src/pages/TramitePage.tsx` — estructura base con `useParams()` para leer el ID
4. Configurar `App.tsx` con `<BrowserRouter>`, `<Routes>` y `<Route>` para cada ruta
5. Agregar links desde las cards/items de trámite en la página principal hacia `/Portal/TyS/:id`
6. Verificar que la navegación entre páginas funciona correctamente
7. Verificar que Header y Footer aparecen en todas las rutas

### Relevant Context
- Rutas a configurar: `/` y `/Portal/TyS/1650`, `/Portal/TyS/661`, `/Portal/TyS/652`, `/Portal/TyS/1618`, `/Portal/TyS/1582`
- Usar `useParams()` en `TramitePage` para obtener el ID y renderizar los datos del trámite correspondiente
- Ver `site-map.md` para confirmar los IDs exactos de cada trámite

---

## Sub-Tarea 8 — Páginas de Detalle de Trámite

**Status:** [x] done

### Intent
Implementar la estructura visual de las 5 páginas de detalle de trámite, replicando fielmente el layout del sitio original. Cada página muestra información específica del trámite (descripción, requisitos, costos, documentos).

### Expected Outcomes
- `src/pages/TramitePage.tsx` completamente implementado con todas las secciones
- `src/data/tramites.ts` — archivo de datos estáticos con la info de los 5 trámites
- Las 5 URLs (`/Portal/TyS/1650`, `/Portal/TyS/661`, `/Portal/TyS/652`, `/Portal/TyS/1618`, `/Portal/TyS/1582`) renderizan la página correcta con sus datos
- Estructura visual idéntica al sitio original para cada página

### Todo List
1. Crear `src/data/tramites.ts` con un objeto/array que contenga los datos de los 5 trámites:
   - ID, título, descripción, requisitos, costos, documentos descargables (nombre + ruta de archivo)
2. Completar `src/pages/TramitePage.tsx`:
   - Leer el ID de la URL con `useParams()`
   - Buscar los datos del trámite en `tramites.ts`
   - Renderizar cada sección según el mapa de Sub-Tarea 2
3. Replicar las secciones encontradas en el sitio original (según `site-map.md`):
   - Breadcrumb de navegación
   - Título y descripción del trámite
   - Tabla/lista de requisitos
   - Tabla/lista de costos
   - Sección de documentos con botones de descarga
4. Usar componentes de `react-bootstrap` (`Accordion`, `Table`, `Badge`, `Breadcrumb`, `Card`, etc.)
5. Poblar con los datos reales de cada trámite (texto del sitio original)
6. Verificar que cada una de las 5 páginas renderiza su información correcta

### Relevant Context
- Los datos de los 5 trámites deben extraerse manualmente del sitio original durante Sub-Tarea 2
- Si los 5 trámites comparten exactamente la misma estructura, un solo componente `TramitePage` con datos dinámicos es suficiente
- Si algún trámite tiene secciones únicas, crear sub-componentes específicos para esas diferencias

---

## Sub-Tarea 9 — Funcionalidad de Botones de Descarga

**Status:** [x] done

### Intent
Implementar la funcionalidad operativa de los botones "Descargar archivo" en las páginas de trámite, de modo que el usuario pueda hacer clic y obtener el archivo correspondiente.

### Expected Outcomes
- Todos los botones de descarga en las 5 páginas de trámite funcionan al hacer clic
- El navegador inicia la descarga del archivo correspondiente a cada botón
- Si se usan archivos locales: archivos placeholder en `src/assets/downloads/` y en `public/downloads/`
- Si se usan URLs externas: links directos a las URLs del sitio original con atributo `download`
- Comportamiento consistente en Chrome, Firefox y Edge

### Todo List
1. Revisar `site-map.md` para la lista de archivos descargables por trámite (URLs y tipos de archivo)
2. Decidir estrategia de descarga:
   - **Opción A (recomendada para archivos reales):** Mantener las URLs externas del sitio original con `<a href="URL_ORIGINAL" download target="_blank">`
   - **Opción B (archivos locales):** Colocar PDFs placeholder en `public/downloads/` y usar rutas relativas `/downloads/nombre.pdf`
3. Implementar los botones como elementos `<a>` con atributo `download` (no como `<button>` sin href)
4. Asegurarse de que el atributo `download` esté presente para forzar la descarga (no abrir en el navegador)
5. Para Opción B: crear al menos un PDF de placeholder por trámite en `public/downloads/`
6. Probar cada botón de descarga en las 5 páginas
7. Verificar que los archivos se descargan correctamente (no se abren en el navegador)

### Relevant Context
- La estrategia entre Opción A y B depende de si las URLs del sitio original son accesibles públicamente sin autenticación
- Si las URLs del original requieren sesión/autenticación, se debe usar la Opción B con archivos locales
- El atributo HTML `download` solo funciona para mismo origen o con encabezado `Content-Disposition: attachment` en el servidor
- Para URLs de origen diferente (cross-origin), se puede usar `fetch` + `Blob` + `URL.createObjectURL()` para forzar la descarga

---

## Sub-Tarea 10 — Revisión Visual Final y Ajustes

**Status:** [x] done

### Intent
Comparar el resultado final (página principal y las 5 páginas de trámite) con el sitio original, documentar diferencias y aplicar ajustes de CSS custom mínimos para mejorar la fidelidad visual.

### Expected Outcomes
- La página principal y las 5 páginas de trámite se ven estructuralmente idénticas al sitio original
- Todos los botones de descarga funcionan correctamente en las 5 páginas
- Cualquier ajuste de color/fuente documentado en `src/assets/custom.css`
- `npm run build` corre sin errores ni warnings
- Código revisado y commiteado en rama `Front-Estructura`

### Todo List
1. Abrir la aplicación React en `localhost` y el sitio original lado a lado
2. Verificar la página principal sección por sección
3. Verificar cada una de las 5 páginas de trámite contra su original
4. Probar todos los botones de descarga y confirmar que descargan el archivo correcto
5. Identificar diferencias visuales: colores, espaciados, tipografías
6. Crear `src/assets/custom.css` e importarlo en `main.tsx` para overrides mínimos
7. Aplicar ajustes de CSS únicamente donde sea necesario
8. Ejecutar `npm run build` y verificar que no hay errores
9. Commit final con mensaje descriptivo en rama `Front-Estructura`

### Relevant Context
- No agregar funcionalidades en este paso más allá de ajustes visuales
- `custom.css` debe ser mínimo (preferir clases de Bootstrap cuando sea posible)

---

## Notas de Arquitectura

- **Patrón de componentes:** Un archivo `.tsx` por componente en `src/components/`, un archivo por página en `src/pages/`
- **Routing:** React Router v6 con rutas `/` y `/Portal/TyS/:id`; layout compartido en `src/layouts/MainLayout.tsx`
- **Datos:** Archivo de datos estáticos `src/data/tramites.ts` con la info de los 5 trámites — no hay estado global ni llamadas a API
- **Descargas:** Botones de descarga implementados como `<a download>` — estrategia (URLs externas vs archivos locales en `public/downloads/`) se decide en Sub-Tarea 9 según accesibilidad de las URLs originales
- **Estilo:** Bootstrap 5 como base, `custom.css` solo para overrides necesarios
- **Naming:** PascalCase para componentes y páginas, kebab-case para archivos CSS, camelCase para archivos de datos
- **No usar:** Redux, Context API, llamadas a API externas, formularios funcionales
