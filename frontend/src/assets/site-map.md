# Site Map — RETyS Baja California
> Análisis estructural de https://retys.bajacalifornia.gob.mx

## Framework CSS
Bootstrap 4.x (confirmado por clases como `col-md-*`, `navbar-expand-lg`, `card`)

---

## Página Principal (/)

### 1. Top Bar
- Barra delgada azul marino (#003876) en la parte superior
- Lado izquierdo: "Gobierno del Estado de Baja California"
- Lado derecho: links de "Inicio", "Mapa del sitio", "Accesibilidad", idioma

### 2. Header / Navbar
- Fondo blanco con borde inferior rojo (#e8161e)
- Logo: Gobierno de Baja California (izquierda)
- Logo: RETyS (centro-izquierda)
- Menú horizontal:
  - Inicio
  - Trámites y Servicios
  - Dependencias
  - Consulta tu Trámite
  - Contáctanos
- Buscador: input + botón "Buscar" (derecha)

### 3. Banner / Hero
- Fondo gradiente azul (primario)
- Título: "Registro Estatal de Trámites y Servicios"
- Subtítulo: descripción del portal
- Botón CTA: "Consultar Trámites"
- Imagen decorativa (escudo o ilustración)

### 4. Acceso Rápido
- Fila de íconos con accesos directos
- 4-6 íconos con texto:
  - 🏛 Trámites
  - 📄 Servicios
  - 🔍 Consultar
  - 📋 Dependencias
  - 📞 Contacto

### 5. Trámites Más Consultados
- Título de sección con borde izquierdo rojo
- Grid de cards (3 columnas en desktop):
  - Cada card: header azul (dependencia), título trámite, descripción breve, botón "Ver trámite"
- Cards incluyen links a: /Portal/TyS/{id}

### 6. Categorías / Dependencias
- Lista de pills/badges con nombres de dependencias
- Filtro visual por organismo

### 7. Noticias / Avisos
- Fondo gris claro
- Grid 3 columnas de noticias:
  - Imagen placeholder, fecha, título, extracto, link "Leer más"

### 8. Footer
- Fondo azul marino (#003876)
- Columna 1: Logo + descripción del portal
- Columna 2: Links útiles (Inicio, Trámites, Dependencias, Contáctanos)
- Columna 3: Contacto (dirección, teléfono, email)
- Columna 4: Redes sociales (Facebook, Twitter/X, YouTube)
- Footer bottom (azul más oscuro): copyright + links legales

---

## Páginas de Trámite (/Portal/TyS/:id)

### Estructura Común (Compartida por los 5 trámites)

1. **Breadcrumb**: Inicio > Trámites y Servicios > [Nombre del Trámite]
2. **Encabezado de Trámite** (fondo azul):
   - Nombre del trámite (h1)
   - Dependencia responsable (badge)
3. **Cuerpo Principal** (layout 8+4 columnas)
   - **Columna principal (col-8)**:
     - Sección: Descripción del trámite
     - Sección: Fundamento legal
     - Sección: Requisitos (tabla o lista numerada)
     - Sección: Costos / Derechos (tabla con costo, fundamento, forma de pago)
     - Sección: Tiempo de resolución
     - Sección: Documentos a descargar (botones de descarga)
   - **Sidebar (col-4)**:
     - Información de contacto de la dependencia
     - Links relacionados / Otros trámites de la misma dependencia
4. **Botones de Descarga**:
   - Botones azules con ícono de descarga
   - Texto: "Descargar [nombre del documento]"
   - Tipos de archivo: PDF, DOC, DOCX
   - URLs del patrón: /Portal/Download/{id_doc}

---

## Trámites Individuales

### Trámite 1650
- **Título**: Solicitud de Inscripción al Registro Civil (estimado)
- **Dependencia**: Registro Civil del Estado de Baja California
- **Documentos descargables**: Formato de solicitud (PDF)

### Trámite 661
- **Título**: Licencia de Funcionamiento
- **Dependencia**: Dirección de Licencias y Permisos
- **Documentos descargables**: Solicitud de licencia (PDF), Reglamento (PDF)

### Trámite 652
- **Título**: Permiso de Uso de Suelo
- **Dependencia**: Secretaría de Desarrollo Urbano
- **Documentos descargables**: Formato de solicitud (PDF)

### Trámite 1618
- **Título**: Certificado de Estudios
- **Dependencia**: Secretaría de Educación Pública del Estado
- **Documentos descargables**: Solicitud (PDF)

### Trámite 1582
- **Título**: Constancia de No Antecedentes Penales
- **Dependencia**: Procuraduría General de Justicia
- **Documentos descargables**: Formato de solicitud (PDF), Requisitos (PDF)

---

## Notas de Implementación

- Los 5 trámites comparten EXACTAMENTE la misma estructura → usar `TramitePage` con datos dinámicos
- Los botones de descarga apuntan a `/Portal/Download/{id}` en el sitio original — implementar con archivos locales en `public/downloads/`
- Colores: primario #003876, secundario #e8161e, acento #f5a800
- Fuente: Segoe UI / Arial (sans-serif del sistema)
