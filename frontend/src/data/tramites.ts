export interface Documento {
  nombre: string
  archivo: string          // ruta relativa a /public/downloads/
  tipo: 'PDF' | 'DOC' | 'DOCX' | 'XLS'
}

export interface Requisito {
  numero: number
  descripcion: string
  notas?: string
}

export interface Costo {
  concepto: string
  monto: string
  fundamento: string
  formaPago: string
}

export interface Tramite {
  id: number
  homoclave: string
  titulo: string
  dependencia: string
  area: string
  descripcion: string
  fundamento: string
  tiempoResolucion: string
  vigencia: string
  requisitos: Requisito[]
  costos: Costo[]
  documentos: Documento[]
  contacto: {
    direccion: string
    telefono: string
    email: string
    horario: string
  }
  tramitesRelacionados: { id: number; titulo: string }[]
  urlOficial?: string
  metricas?: {
    inflesz: number
    nivel: string
    palabras: number
    terminosJuridicos: number
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Trámites reales del RETyS Baja California — fichas-dificiles.json
// Fuente de la verdad: texto_original de cada ficha (corpus/fichas/)
// ─────────────────────────────────────────────────────────────────────────────
const tramites: Tramite[] = [
  // ── 1. BC-CESPT-041 ─────────────────────────────────────────────────────────
  {
    id: 1634,
    homoclave: 'BC-CESPT-041',
    titulo: 'Registro o Revalidación de Exención de Permiso de Descarga de Aguas Residuales para Comercios y Empresas de Servicios',
    dependencia: 'Comisión Estatal de Servicios Públicos de Tijuana',
    area: 'Comisión Estatal de Servicios Públicos de Tijuana', // PENDIENTE: área específica no disponible en JSON
    descripcion:
      'Solicitar la exención del trámite de permiso de descargas, debido a que no se generan aguas residuales de procesos de producción de bienes o servicios.',
    fundamento:
      'Ley Que Reglamenta El Servicio De Agua Potable En El Estado De Baja California Artículos 94 y 109.; ' +
      'Ley de Comisiones Estatales de Servicios Públicos del Estado De Baja California Artículos 1 y 2.; ' +
      'Ley de Ingresos del Estado de Baja California para el Ejercicio Fiscal del año 2026 Artículo 9.',
    tiempoResolucion: '30 Días Hábiles',
    vigencia: '1 año',
    // PENDIENTE: texto_original contiene requisitos extendidos (Secciones 1–4); solo se muestran los 4 del JSON
    requisitos: [
      { numero: 1, descripcion: 'Original y copia de la Solicitud de Exención de Permiso de Descarga de Aguas Residuales FRM-022 debidamente llenado y firmado.' },
      { numero: 2, descripcion: 'Copia de Constancia de Situación Fiscal de la empresa.' },
      { numero: 3, descripcion: 'Fotografías a color de las áreas del interior de la empresa.' },
      { numero: 4, descripcion: 'Copia de documentales que acrediten la no generación de descargas de aguas residuales de proceso (manifiestos de disposición de residuos peligrosos, facturas del lavado de ropa de los últimos 6 meses, etc.).' },
    ],
    costos: [
      {
        concepto: 'Costo',
        monto: 'COSTO VARIABLE: Por expedición: $1,7999.46 pesos | Por la revalidación anual: $976.71 pesos | Septiembre 2026',
        fundamento: '',
        formaPago: '',
      },
    ],
    documentos: [], // PENDIENTE: formatos descargables no disponibles en JSON
    contacto: {
      direccion: '', // PENDIENTE: dirección no disponible en JSON
      telefono: '',  // PENDIENTE
      email: '',     // PENDIENTE
      horario: '',   // PENDIENTE
    },
    tramitesRelacionados: [], // PENDIENTE
    urlOficial: 'https://retys.bajacalifornia.gob.mx/Portal/TyS/1634',
    metricas: {
      inflesz: 70.3,
      nivel: 'bastante fácil',
      palabras: 1141,
      terminosJuridicos: 25,
    },
  },

  // ── 2. BC-SH-012 ─────────────────────────────────────────────────────────────
  {
    id: 661,
    homoclave: 'BC-SH-012',
    titulo: 'Expedición de Licencia de Conducir',
    dependencia: 'Secretaría de Hacienda de Baja California',
    area: 'Secretaría de Hacienda de Baja California', // PENDIENTE: área específica no disponible en JSON
    descripcion:
      'Colaborar con el ciudadano para cumplir con los requisitos establecidos para que obtenga su licencia de conducir, con la certeza de que se trata de un documento obtenido legalmente y buscando la seguridad en el manejo de vehículos automotor, con la protección individual como de terceros.',
    fundamento:
      'Ley de Ingresos del Estado de Baja California para el Ejercicio Fiscal del Año 2025, Artículo 10, Fracción I, Inciso A.; ' +
      'Ley que Regula los Servicios de Control Vehicular en el Estado de Baja California, Artículos 34 y 36.',
    tiempoResolucion: '45 Minutos',
    vigencia: '3 años, 5 años y provisionales 9 meses y 1 año.',
    requisitos: [
      { numero: 1, descripcion: 'Cita.' },
      { numero: 2, descripcion: 'Solicitud del trámite (formato de manifiesto que se captura en la Recaudación de Rentas).' },
      { numero: 3, descripcion: 'Identificación oficial con fotografía vigente en original y copia (INE, pasaporte mexicano vigente, cédula profesional, matrícula consular, cartilla militar). ORIGINAL Y COPIA.' },
      { numero: 4, descripcion: 'Comprobante de domicilio no mayor a tres meses de antigüedad en original y copia.' },
      { numero: 5, descripcion: 'Certificado médico, expedido por institución pública o privada de salud (original y copia).' },
      { numero: 6, descripcion: 'Acreditar no haber sido condenado por manejar vehículo de motor en estado de ebriedad o bajo el influjo de drogas en los últimos cinco años (carta de no antecedentes penales).' },
      { numero: 7, descripcion: 'Presentar examen antidoping.' },
      { numero: 8, descripcion: 'Certificado de estudios con fotografía (mínimo primaria); aplica solo para licencias tipo B y D.' },
      { numero: 9, descripcion: 'Presentar y aprobar exámenes teórico y práctico de manejo, con vehículo apropiado a la licencia solicitada y tarjeta de circulación vigente (original y copia).' },
      { numero: 10, descripcion: 'Realizar el pago correspondiente. Opciones: efectivo, cheque certificado, tarjeta débito/crédito (excepto American Express).' },
    ],
    costos: [
      {
        concepto: 'Costo',
        monto: 'COSTO VARIABLE: Mes de Septiembre de 2026. | Automovilista 3 años $ 1,120.39 M.N. | 5 años $ 1,493.85 M.N. | Motociclista 3 años $ 1,120.39 M.N.',
        fundamento: '',
        formaPago: '',
      },
    ],
    documentos: [], // PENDIENTE: formatos descargables no disponibles en JSON
    contacto: {
      direccion: '', // PENDIENTE
      telefono: '',  // PENDIENTE
      email: '',     // PENDIENTE
      horario: '',   // PENDIENTE
    },
    tramitesRelacionados: [], // PENDIENTE
    urlOficial: 'https://retys.bajacalifornia.gob.mx/Portal/TyS/661',
    metricas: {
      inflesz: 56.1,
      nivel: 'normal',
      palabras: 1246,
      terminosJuridicos: 22,
    },
  },

  // ── 3. BC-CEJUM-001 ───────────────────────────────────────────────────────────
  {
    id: 1238,
    homoclave: 'BC-CEJUM-001',
    titulo: 'Atención Integral a Mujeres Víctimas de Violencia',
    dependencia: 'Centro de Justicia para las Mujeres del Estado de Baja California',
    area: 'Centro de Justicia para las Mujeres del Estado de Baja California', // PENDIENTE: área específica no disponible en JSON
    descripcion:
      'Asesoría psicológica, asesoría legal, trabajo social, atención médica preventiva, ludoteca, estancia transitoria, área de empoderamiento y prevención.',
    fundamento:
      'Código Nacional de Procedimientos Penales Artículos 17, 18, 109, 110, 259, 261, 262, 272, 275, 277, 366, 368, 369 y 370.',
    tiempoResolucion: '30 Minutos',
    vigencia: 'Sin vigencia',
    requisitos: [
      { numero: 1, descripcion: 'Identificación Oficial.' },
    ],
    costos: [
      {
        concepto: 'Costo',
        monto: 'Sin costo',
        fundamento: '',
        formaPago: '',
      },
    ],
    documentos: [], // PENDIENTE
    contacto: {
      direccion: 'Avenida Moctezuma #1, Residencial de Cortez, Tijuana, 22190',
      telefono: '', // PENDIENTE
      email: '',    // PENDIENTE
      horario: '',  // PENDIENTE
    },
    tramitesRelacionados: [], // PENDIENTE
    urlOficial: 'https://retys.bajacalifornia.gob.mx/Portal/TyS/1238',
    metricas: {
      inflesz: 12.8,
      nivel: 'muy difícil',
      palabras: 117,
      terminosJuridicos: 11,
    },
  },

  // ── 4. BC-SHFP-002 ────────────────────────────────────────────────────────────
  {
    id: 1131,
    homoclave: 'BC-SHFP-002',
    titulo: 'Constancia de no inhabilitación.',
    dependencia: 'Secretaría Anticorrupción y Buen Gobierno',
    area: 'Secretaría Anticorrupción y Buen Gobierno', // PENDIENTE: área específica no disponible en JSON
    descripcion:
      'Trámite a través del cual la Secretaría Anticorrupción y Buen Gobierno, acredita que el solicitante, no cuenta con inhabilitación vigente, para desempeñar un empleo, cargo o comisión.',
    fundamento:
      'LEY DE INGRESOS DEL ESTADO DE BAJA CALIFORNIA PARA EL EJERCICIO FISCAL DEL AÑO 2026 18, FRACCIÓN V, INCISO E) DEL CAPÍTULO VII; ' +
      'REGLAMENTO INTERNO DE LA SECRETARÍA ANTICORRUPCIÓN Y BUEN GOBIERNO 32 Y 36 FRACCIÓN XIII.',
    tiempoResolucion: '48 Horas',
    vigencia: '90 DÍAS NATURALES.',
    requisitos: [
      { numero: 1, descripcion: 'Registro Federal de Contribuyentes (RFC).' },
      { numero: 2, descripcion: 'Indicar a qué dependencia se debe enviar la constancia, o si no lo sabes, se hará "a quien corresponda".' },
      { numero: 3, descripcion: 'Original y copia de una identificación oficial vigente: Credencial para votar (INE), Pasaporte mexicano, Cédula profesional (con foto), Cartilla militar, Licencia de conducir (junto con CURP o constancia de residencia).' },
      { numero: 4, descripcion: 'Formato para obtener la constancia de no inhabilitación.' },
      { numero: 5, descripcion: 'Recibo original del pago de derechos (se puede pagar en recaudación de rentas, "Farmacias Roma", o bancos).' },
    ],
    costos: [
      {
        concepto: 'Costo',
        monto: 'COSTO VARIABLE: $132.00 M.N. (Actualizándose mensualmente, de conformidad al Transitorio Séptimo de la Ley de Ingresos del Estado de Baja California para el ejercicio fiscal del año 2026).',
        fundamento: '',
        formaPago: '',
      },
    ],
    documentos: [], // PENDIENTE
    contacto: {
      direccion: '', // PENDIENTE
      telefono: '',  // PENDIENTE
      email: '',     // PENDIENTE
      horario: '',   // PENDIENTE
    },
    tramitesRelacionados: [], // PENDIENTE
    urlOficial: 'https://retys.bajacalifornia.gob.mx/Portal/TyS/1131',
    metricas: {
      inflesz: 55.4,
      nivel: 'normal',
      palabras: 605,
      terminosJuridicos: 15,
    },
  },

  // ── 5. BC-SSCBC-022 ───────────────────────────────────────────────────────────
  {
    id: 1618,
    homoclave: 'BC-SSCBC-022',
    titulo: 'Expedición de Constancia de Antecedentes Penales',
    dependencia: 'Secretaría de Seguridad Ciudadana del Estado de Baja California',
    area: 'Secretaría de Seguridad Ciudadana del Estado de Baja California', // PENDIENTE: área específica no disponible en JSON
    descripcion:
      'Documento donde se hace constar que el ciudadano cuenta o no, con antecedentes penales de carácter doloso del fuero común en el Estado de Baja California.',
    fundamento:
      'Ley Nacional de Ejecución Penal Artículo 27 fracción IV; ' +
      'Ley Orgánica del Poder Ejecutivo del Estado de Baja California Artículo 34 fracción XXXVI; ' +
      'Ley de Ingresos del Estado de Baja California para el ejercicio fiscal del año 2026 Artículo 18, fracción I, inciso H.',
    tiempoResolucion: '5 Minutos',
    vigencia: '3 MESES',
    requisitos: [
      { numero: 1, descripcion: 'Identificación oficial vigente (credencial de elector, pasaporte mexicano, licencia de conducir del Estado de Baja California, cartilla del servicio militar nacional liberada, cédula profesional con foto, título profesional).' },
    ],
    costos: [
      {
        concepto: 'Costo',
        monto: 'COSTO: $ 284.38 pesos',
        fundamento: '',
        formaPago: '',
      },
    ],
    documentos: [], // PENDIENTE
    contacto: {
      direccion: '', // PENDIENTE
      telefono: '',  // PENDIENTE
      email: '',     // PENDIENTE
      horario: '',   // PENDIENTE
    },
    tramitesRelacionados: [], // PENDIENTE
    urlOficial: 'https://retys.bajacalifornia.gob.mx/Portal/TyS/1618',
    metricas: {
      inflesz: 54.8,
      nivel: 'algo difícil',
      palabras: 425,
      terminosJuridicos: 16,
    },
  },
]

// ─────────────────────────────────────────────────────────────────────────────
// PENDIENTES (datos no disponibles en fichas-dificiles.json):
// - contacto.direccion: BC-CESPT-041, BC-SH-012, BC-SHFP-002, BC-SSCBC-022
// - contacto.telefono: todas las fichas
// - contacto.email: todas las fichas
// - contacto.horario: todas las fichas
// - tramitesRelacionados: todas las fichas
// - documentos (formatos descargables): todas las fichas
// - area (usa dependencia como placeholder): todas las fichas
// - BC-CESPT-041: requisitos extendidos (Secciones 1–4 de texto_original)
// ─────────────────────────────────────────────────────────────────────────────

export default tramites
