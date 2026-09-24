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
}

const tramites: Tramite[] = [
  {
    id: 1650,
    titulo: 'Solicitud de Inscripción al Registro Civil',
    dependencia: 'Registro Civil del Estado de Baja California',
    area: 'Dirección del Registro Civil',
    descripcion:
      'Trámite mediante el cual los ciudadanos solicitan el registro de actos del estado civil, tales como nacimientos, matrimonios, divorcios y defunciones. El Registro Civil es el organismo público encargado de hacer constar y dar fe de los actos y hechos del estado civil de las personas, y de acreditar mediante documentos la situación jurídica de las personas físicas.',
    fundamento:
      'Ley del Registro Civil del Estado de Baja California; Código Civil del Estado de Baja California; Reglamento de la Ley del Registro Civil.',
    tiempoResolucion: '1 a 3 días hábiles',
    vigencia: 'Permanente',
    requisitos: [
      { numero: 1, descripcion: 'Solicitud debidamente llenada y firmada (formato oficial).' },
      { numero: 2, descripcion: 'Identificación oficial vigente con fotografía (INE, pasaporte, cédula profesional).' },
      { numero: 3, descripcion: 'CURP del solicitante.' },
      { numero: 4, descripcion: 'Comprobante de domicilio no mayor a 3 meses.' },
      { numero: 5, descripcion: 'Documentos que acrediten el acto a registrar (acta de nacimiento hospitalaria, acta de matrimonio eclesiástico, etc.), según el tipo de inscripción.' },
      { numero: 6, descripcion: 'Pago de derechos correspondiente.', notas: 'Ver tabla de costos.' },
    ],
    costos: [
      {
        concepto: 'Acta de Nacimiento (primera copia)',
        monto: 'Gratuito',
        fundamento: 'Ley de Ingresos del Estado',
        formaPago: 'N/A',
      },
      {
        concepto: 'Acta de Nacimiento (copias adicionales)',
        monto: '$50.00 MXN',
        fundamento: 'Ley de Ingresos del Estado, Art. 12',
        formaPago: 'Efectivo / Transferencia',
      },
      {
        concepto: 'Acta de Matrimonio',
        monto: '$200.00 MXN',
        fundamento: 'Ley de Ingresos del Estado, Art. 14',
        formaPago: 'Efectivo / Transferencia',
      },
      {
        concepto: 'Acta de Defunción',
        monto: 'Gratuito',
        fundamento: 'Ley de Ingresos del Estado',
        formaPago: 'N/A',
      },
    ],
    documentos: [
      {
        nombre: 'Formato de Solicitud de Inscripción',
        archivo: '/downloads/tramite-1650-solicitud.pdf',
        tipo: 'PDF',
      },
    ],
    contacto: {
      direccion: 'Av. Álvaro Obregón 1262, Col. Nueva, Mexicali, B.C.',
      telefono: '(686) 552-2220',
      email: 'registrocivil@bajacalifornia.gob.mx',
      horario: 'Lunes a Viernes 8:00 - 15:00 hrs',
    },
    tramitesRelacionados: [
      { id: 661, titulo: 'Licencia de Funcionamiento' },
      { id: 1618, titulo: 'Certificado de Estudios' },
    ],
  },
  {
    id: 661,
    titulo: 'Licencia de Funcionamiento',
    dependencia: 'Dirección de Licencias y Permisos',
    area: 'Subdirección de Permisos Comerciales',
    descripcion:
      'Autorización que otorga el gobierno estatal a personas físicas o morales para operar legalmente un establecimiento comercial, industrial o de servicios dentro del territorio del Estado de Baja California. La licencia garantiza que el establecimiento cumple con los requisitos de seguridad, sanidad, uso de suelo y demás disposiciones legales aplicables.',
    fundamento:
      'Ley de Establecimientos Mercantiles del Estado de Baja California; Reglamento de Licencias de Funcionamiento; Ley de Ingresos del Estado.',
    tiempoResolucion: '5 a 10 días hábiles',
    vigencia: 'Anual (renovación obligatoria)',
    requisitos: [
      { numero: 1, descripcion: 'Solicitud oficial debidamente llenada y firmada.' },
      { numero: 2, descripcion: 'Identificación oficial vigente del propietario o representante legal.' },
      { numero: 3, descripcion: 'RFC y CURP del solicitante.' },
      { numero: 4, descripcion: 'Acta constitutiva (para personas morales) y poder notarial del representante.' },
      { numero: 5, descripcion: 'Comprobante de domicilio del establecimiento no mayor a 3 meses.' },
      { numero: 6, descripcion: 'Permiso de uso de suelo vigente compatible con la actividad.' },
      { numero: 7, descripcion: 'Dictamen de protección civil favorable.' },
      { numero: 8, descripcion: 'Pago de derechos correspondiente al giro del negocio.' },
    ],
    costos: [
      {
        concepto: 'Licencia de Funcionamiento — Giro de Bajo Impacto',
        monto: '$800.00 MXN',
        fundamento: 'Ley de Ingresos, Art. 22 fracción I',
        formaPago: 'Efectivo / Tarjeta / Transferencia',
      },
      {
        concepto: 'Licencia de Funcionamiento — Giro de Mediano Impacto',
        monto: '$1,500.00 MXN',
        fundamento: 'Ley de Ingresos, Art. 22 fracción II',
        formaPago: 'Efectivo / Tarjeta / Transferencia',
      },
      {
        concepto: 'Licencia de Funcionamiento — Giro de Alto Impacto',
        monto: '$3,000.00 MXN',
        fundamento: 'Ley de Ingresos, Art. 22 fracción III',
        formaPago: 'Efectivo / Tarjeta / Transferencia',
      },
      {
        concepto: 'Renovación anual',
        monto: '50% del costo original',
        fundamento: 'Ley de Ingresos, Art. 22 fracción IV',
        formaPago: 'Efectivo / Tarjeta / Transferencia',
      },
    ],
    documentos: [
      {
        nombre: 'Solicitud de Licencia de Funcionamiento',
        archivo: '/downloads/tramite-661-solicitud.pdf',
        tipo: 'PDF',
      },
      {
        nombre: 'Reglamento de Establecimientos Mercantiles',
        archivo: '/downloads/tramite-661-reglamento.pdf',
        tipo: 'PDF',
      },
    ],
    contacto: {
      direccion: 'Blvd. Benito Juárez 1025, Col. Centro, Mexicali, B.C.',
      telefono: '(686) 558-3400',
      email: 'licencias@bajacalifornia.gob.mx',
      horario: 'Lunes a Viernes 8:00 - 15:00 hrs',
    },
    tramitesRelacionados: [
      { id: 652, titulo: 'Permiso de Uso de Suelo' },
      { id: 1582, titulo: 'Constancia de No Antecedentes Penales' },
    ],
  },
  {
    id: 652,
    titulo: 'Permiso de Uso de Suelo',
    dependencia: 'Secretaría de Desarrollo Urbano y Sustentabilidad',
    area: 'Dirección de Planeación Urbana',
    descripcion:
      'Autorización que emite la Secretaría de Desarrollo Urbano mediante la cual se permite o condiciona el uso o el cambio de uso del suelo de un predio, conforme a los planes y programas de desarrollo urbano vigentes en el municipio o localidad. Este permiso es indispensable para el establecimiento de negocios, construcciones nuevas, cambios de giro y regularización de inmuebles.',
    fundamento:
      'Ley de Desarrollo Urbano del Estado de Baja California; Programa Estatal de Desarrollo Urbano; Plan Municipal de Desarrollo Urbano vigente.',
    tiempoResolucion: '10 a 20 días hábiles',
    vigencia: '1 año (prorrogable)',
    requisitos: [
      { numero: 1, descripcion: 'Solicitud oficial con datos del predio y actividad solicitada.' },
      { numero: 2, descripcion: 'Identificación oficial del propietario o representante legal.' },
      { numero: 3, descripcion: 'Copia del título de propiedad o contrato de arrendamiento notariado.' },
      { numero: 4, descripcion: 'Croquis de localización y plano del predio (acotado, con colindancias).' },
      { numero: 5, descripcion: 'Boleta predial al corriente de pago.' },
      { numero: 6, descripcion: 'Descripción detallada de la actividad o giro que se pretende desarrollar.' },
      { numero: 7, descripcion: 'Pago de derechos de revisión.', notas: 'Ver tabla de costos.' },
    ],
    costos: [
      {
        concepto: 'Revisión y expedición de dictamen de uso de suelo',
        monto: '$600.00 MXN',
        fundamento: 'Ley de Ingresos, Art. 35',
        formaPago: 'Efectivo / Transferencia',
      },
      {
        concepto: 'Cambio de uso de suelo — Habitacional a Comercial',
        monto: '$2,500.00 MXN',
        fundamento: 'Ley de Ingresos, Art. 36 fracción I',
        formaPago: 'Efectivo / Transferencia',
      },
      {
        concepto: 'Cambio de uso de suelo — Comercial a Industrial',
        monto: '$5,000.00 MXN',
        fundamento: 'Ley de Ingresos, Art. 36 fracción II',
        formaPago: 'Efectivo / Transferencia',
      },
    ],
    documentos: [
      {
        nombre: 'Formato de Solicitud de Uso de Suelo',
        archivo: '/downloads/tramite-652-solicitud.pdf',
        tipo: 'PDF',
      },
    ],
    contacto: {
      direccion: 'Calle L s/n entre Av. Reforma y Calle M, Col. Nueva, Mexicali, B.C.',
      telefono: '(686) 558-2900',
      email: 'usosuelo@bajacalifornia.gob.mx',
      horario: 'Lunes a Viernes 8:00 - 15:00 hrs',
    },
    tramitesRelacionados: [
      { id: 661, titulo: 'Licencia de Funcionamiento' },
      { id: 1650, titulo: 'Inscripción al Registro Civil' },
    ],
  },
  {
    id: 1618,
    titulo: 'Expedición de Certificado de Estudios',
    dependencia: 'Secretaría de Educación Pública del Estado de Baja California (SEPBC)',
    area: 'Dirección de Control Escolar',
    descripcion:
      'Trámite mediante el cual la Secretaría de Educación Pública del Estado expide el certificado oficial que acredita la conclusión de un nivel educativo (preescolar, primaria, secundaria, bachillerato o equivalente) en una institución pública del estado. Este documento tiene validez oficial para trámites laborales, académicos y migratorios.',
    fundamento:
      'Ley General de Educación; Ley de Educación del Estado de Baja California; Acuerdo Secretarial 286 (revalidación y equivalencia de estudios).',
    tiempoResolucion: '5 a 15 días hábiles',
    vigencia: 'Permanente',
    requisitos: [
      { numero: 1, descripcion: 'Solicitud oficial firmada por el interesado o tutor (menores de edad).' },
      { numero: 2, descripcion: 'Identificación oficial vigente con fotografía.' },
      { numero: 3, descripcion: 'CURP.' },
      { numero: 4, descripcion: 'Acta de nacimiento.' },
      { numero: 5, descripcion: 'Boletas o calificaciones de todos los grados del nivel educativo correspondiente.' },
      { numero: 6, descripcion: 'Nombre y clave del centro educativo donde se realizaron los estudios.' },
      { numero: 7, descripcion: 'Pago de derechos (aplica para duplicados y expediciones posteriores a 1 año de egreso).' },
    ],
    costos: [
      {
        concepto: 'Primera expedición (recién egresado)',
        monto: 'Gratuito',
        fundamento: 'Ley General de Educación, Art. 6',
        formaPago: 'N/A',
      },
      {
        concepto: 'Duplicado por extravío o deterioro',
        monto: '$350.00 MXN',
        fundamento: 'Ley de Ingresos del Estado, Art. 18',
        formaPago: 'Efectivo / Transferencia',
      },
      {
        concepto: 'Apostille o legalización para uso en el extranjero',
        monto: '$500.00 MXN',
        fundamento: 'Ley de Ingresos del Estado, Art. 18 bis',
        formaPago: 'Efectivo / Transferencia',
      },
    ],
    documentos: [
      {
        nombre: 'Formato de Solicitud de Certificado de Estudios',
        archivo: '/downloads/tramite-1618-solicitud.pdf',
        tipo: 'PDF',
      },
    ],
    contacto: {
      direccion: 'Blvd. Lázaro Cárdenas 1220, Col. Ex-Ejido Coahuila, Mexicali, B.C.',
      telefono: '(686) 558-4000 ext. 4201',
      email: 'controlescolar@sepbc.gob.mx',
      horario: 'Lunes a Viernes 8:00 - 15:00 hrs',
    },
    tramitesRelacionados: [
      { id: 1650, titulo: 'Inscripción al Registro Civil' },
      { id: 1582, titulo: 'Constancia de No Antecedentes Penales' },
    ],
  },
  {
    id: 1582,
    titulo: 'Constancia de No Antecedentes Penales',
    dependencia: 'Fiscalía General del Estado de Baja California',
    area: 'Dirección de Antecedentes Penales',
    descripcion:
      'Documento oficial expedido por la Fiscalía General del Estado de Baja California que certifica que el solicitante no cuenta con antecedentes penales registrados en el estado. Este documento es requerido para trámites laborales, migratorios, académicos, de adopción y diversos procesos administrativos tanto en el sector público como privado.',
    fundamento:
      'Ley Orgánica de la Fiscalía General del Estado de Baja California; Código de Procedimientos Penales del Estado; Acuerdo A/005/2018 de la Fiscalía General.',
    tiempoResolucion: '1 a 3 días hábiles',
    vigencia: '90 días naturales a partir de su expedición',
    requisitos: [
      { numero: 1, descripcion: 'Solicitud oficial llenada y firmada por el interesado.' },
      { numero: 2, descripcion: 'Identificación oficial vigente con fotografía (INE, pasaporte, cédula profesional).' },
      { numero: 3, descripcion: 'CURP.' },
      { numero: 4, descripcion: 'Comprobante de domicilio vigente (no mayor a 3 meses).' },
      { numero: 5, descripcion: 'Huellas dactilares (se toman en el momento del trámite).' },
      { numero: 6, descripcion: 'Pago de derechos correspondiente.' },
      { numero: 7, descripcion: 'En caso de personas morales: poder notarial del representante legal e identificación oficial del mismo.' },
    ],
    costos: [
      {
        concepto: 'Constancia de No Antecedentes Penales',
        monto: '$180.00 MXN',
        fundamento: 'Ley de Ingresos del Estado, Art. 25 fracción VIII',
        formaPago: 'Efectivo / Transferencia electrónica',
      },
      {
        concepto: 'Constancia con apostille para uso en el extranjero',
        monto: '$500.00 MXN',
        fundamento: 'Ley de Ingresos del Estado, Art. 25 fracción IX',
        formaPago: 'Efectivo / Transferencia electrónica',
      },
    ],
    documentos: [
      {
        nombre: 'Formato de Solicitud de No Antecedentes Penales',
        archivo: '/downloads/tramite-1582-solicitud.pdf',
        tipo: 'PDF',
      },
      {
        nombre: 'Requisitos Detallados y Consideraciones',
        archivo: '/downloads/tramite-1582-requisitos.pdf',
        tipo: 'PDF',
      },
    ],
    contacto: {
      direccion: 'Av. Independencia 1012, Col. Ex-Ejido Coahuila, Mexicali, B.C.',
      telefono: '(686) 558-5700',
      email: 'antecedentes@fgebc.gob.mx',
      horario: 'Lunes a Viernes 8:00 - 16:00 hrs',
    },
    tramitesRelacionados: [
      { id: 661, titulo: 'Licencia de Funcionamiento' },
      { id: 1618, titulo: 'Certificado de Estudios' },
    ],
  },
]

export default tramites
