"""
skill_retys.py — Skill (tool) de consulta al catálogo RETyS BC.

Define la TOOL_DEFINITION compatible con el formato tool calling de
watsonx.ai / OpenAI, la base de datos de trámites y la lógica de búsqueda.
"""
import json

# ─────────────────────────────────────────────────────────────────────────────
# Definición de la tool para watsonx.ai / OpenAI function calling
# ─────────────────────────────────────────────────────────────────────────────

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "consultar_tramite_retys",
        "description": (
            "Consulta el catálogo oficial del Registro Estatal de Trámites y Servicios "
            "de Baja California (RETyS BC). Devuelve la ficha completa del trámite: "
            "requisitos, costo, tiempo de respuesta, dependencia responsable, horario, "
            "modalidad y fundamento legal. Úsala siempre que el ciudadano pregunte "
            "cómo realizar un trámite o qué documentos necesita."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "nombre_tramite": {
                    "type": "string",
                    "description": (
                        "Nombre del trámite a buscar, tal como lo diría el ciudadano. "
                        "Ejemplos: 'licencia de conducir', 'acta de nacimiento', 'pasaporte'."
                    ),
                },
                "tipo_busqueda": {
                    "type": "string",
                    "enum": ["exacta", "parcial"],
                    "description": (
                        "Tipo de búsqueda. 'exacta': coincidencia exacta insensible a "
                        "mayúsculas. 'parcial': el nombre del trámite puede estar contenido "
                        "dentro del nombre registrado. Por defecto usa 'parcial'."
                    ),
                },
            },
            "required": ["nombre_tramite"],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Base de datos de trámites RETyS BC
# ─────────────────────────────────────────────────────────────────────────────

TRAMITES_DB: dict[str, dict] = {
    "licencia de conducir": {
        "nombre": "Expedición de Licencia de Conducir",
        "descripcion": (
            "Documento oficial que autoriza a una persona a conducir vehículos de motor "
            "en el estado de Baja California y en toda la República Mexicana."
        ),
        "dependencia": "Secretaría de Infraestructura y Desarrollo Urbano (SIDUE) — "
                       "Dirección de Vialidad y Transporte del Estado",
        "requisitos": [
            "Identificación oficial vigente (INE, pasaporte o cédula profesional)",
            "Comprobante de domicilio reciente (no mayor a 3 meses)",
            "Examen médico psicofísico aprobado (se realiza en el módulo)",
            "Comprobante de pago de derechos",
            "CURP",
        ],
        "costo": "295 pesos (tipo B — automóvil particular)",
        "tiempo_respuesta": "Mismo día (entrega inmediata en el módulo)",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/expedicion-licencia",
        "fundamento_legal": "Ley de Tránsito del Estado de Baja California, Art. 42",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "revalidacion de licencia de conducir": {
        "nombre": "Revalidación de Licencia de Conducir",
        "descripcion": (
            "Renovación de la licencia de conducir vigente o vencida para continuar "
            "conduciendo vehículos de motor en Baja California."
        ),
        "dependencia": "Secretaría de Infraestructura y Desarrollo Urbano (SIDUE) — "
                       "Dirección de Vialidad y Transporte del Estado",
        "requisitos": [
            "Licencia de conducir anterior (vigente o hasta 1 año vencida)",
            "Identificación oficial vigente",
            "Comprobante de domicilio reciente (no mayor a 3 meses)",
            "Examen médico psicofísico aprobado (se realiza en el módulo)",
            "Comprobante de pago de derechos",
        ],
        "costo": "295 pesos",
        "tiempo_respuesta": "Mismo día (entrega inmediata en el módulo)",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/revalidacion-licencia",
        "fundamento_legal": "Ley de Tránsito del Estado de Baja California, Art. 45",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "acta de nacimiento": {
        "nombre": "Expedición de Acta de Nacimiento",
        "descripcion": (
            "Documento que certifica el registro civil del nacimiento de una persona. "
            "Es el documento de identidad más básico y es necesario para obtener la "
            "mayoría de los demás documentos oficiales."
        ),
        "dependencia": "Dirección General del Registro Civil de Baja California",
        "requisitos": [
            "Identificación oficial del solicitante (INE o pasaporte)",
            "Conocer el número de acta o datos del registrado (nombre completo, "
            "fecha y lugar de nacimiento)",
            "Comprobante de pago de derechos",
        ],
        "costo": "91 pesos (copia certificada)",
        "tiempo_respuesta": "Mismo día (en módulo presencial) o 3 días hábiles (en línea)",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/acta-nacimiento",
        "fundamento_legal": "Código Civil del Estado de Baja California, Art. 55",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "mixto",
    },
    "credencial de elector": {
        "nombre": "Trámite de Credencial para Votar (INE)",
        "descripcion": (
            "Documento de identidad oficial emitido por el Instituto Nacional Electoral (INE) "
            "que acredita la ciudadanía mexicana y permite ejercer el derecho al voto. "
            "También es la identificación oficial más aceptada para trámites en México."
        ),
        "dependencia": "Instituto Nacional Electoral (INE) — Módulo de Atención Ciudadana",
        "requisitos": [
            "Acta de nacimiento original (copia certificada)",
            "Comprobante de domicilio reciente (no mayor a 3 meses)",
            "CURP impresa",
            "Una fotografía reciente (en algunos módulos la toman en el lugar)",
        ],
        "costo": "Gratuito",
        "tiempo_respuesta": "30 días naturales (entrega a domicilio o en módulo)",
        "url_oficial": "https://www.ine.mx/credencial/",
        "fundamento_legal": "Ley General de Instituciones y Procedimientos Electorales, Art. 130",
        "horario": "Lunes a viernes de 9:00 a 17:00 horas (consultar módulo más cercano)",
        "modalidad": "presencial",
    },
    "pasaporte": {
        "nombre": "Expedición de Pasaporte Mexicano",
        "descripcion": (
            "Documento de viaje internacional emitido por la Secretaría de Relaciones "
            "Exteriores (SRE) que acredita la nacionalidad y ciudadanía mexicana ante "
            "autoridades extranjeras."
        ),
        "dependencia": "Secretaría de Relaciones Exteriores (SRE) — Delegación Baja California",
        "requisitos": [
            "Acta de nacimiento original (copia certificada reciente)",
            "Identificación oficial vigente (INE o cédula profesional)",
            "Comprobante de domicilio reciente (no mayor a 3 meses)",
            "CURP impresa",
            "Comprobante de pago de derechos (pago previo en banco o en línea)",
            "Para menores de edad: acta de nacimiento y presencia de ambos padres con "
            "identificación oficial",
        ],
        "costo": "1,540 pesos (adulto, vigencia 10 años) / 990 pesos (menor, vigencia 3 años)",
        "tiempo_respuesta": "5 días hábiles (cita previa obligatoria)",
        "url_oficial": "https://www.gob.mx/sre/acciones-y-programas/pasaportes",
        "fundamento_legal": "Ley de Pasaportes, Art. 4",
        "horario": "Lunes a viernes de 8:00 a 14:00 horas (con cita)",
        "modalidad": "presencial",
    },
    "acta de matrimonio": {
        "nombre": "Expedición de Acta de Matrimonio",
        "descripcion": (
            "Documento que certifica la unión legal entre dos personas ante el Registro "
            "Civil del Estado de Baja California."
        ),
        "dependencia": "Dirección General del Registro Civil de Baja California",
        "requisitos": [
            "Identificación oficial de ambos contrayentes (INE o pasaporte)",
            "Acta de nacimiento de ambos contrayentes (copia certificada reciente)",
            "Dos testigos con identificación oficial",
            "Examen médico prenupcial de ambos (vigencia 15 días)",
            "Comprobante de pago de derechos",
            "En caso de divorcio previo: copia certificada de la sentencia de divorcio",
        ],
        "costo": "456 pesos",
        "tiempo_respuesta": "La ceremonia se programa en 8 días hábiles; el acta se entrega el mismo día",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/acta-matrimonio",
        "fundamento_legal": "Código Civil del Estado de Baja California, Art. 102",
        "horario": "Lunes a viernes de 8:00 a 14:00 horas",
        "modalidad": "presencial",
    },
    "antecedentes penales": {
        "nombre": "Constancia de No Antecedentes Penales",
        "descripcion": (
            "Documento oficial expedido por la Fiscalía General del Estado de Baja "
            "California que certifica que una persona no tiene antecedentes penales "
            "registrados en el estado. Es solicitado frecuentemente por empleadores."
        ),
        "dependencia": "Fiscalía General del Estado de Baja California",
        "requisitos": [
            "Identificación oficial vigente (INE, pasaporte o cédula profesional)",
            "CURP",
            "Comprobante de pago de derechos",
            "Llenar el formulario de solicitud en el módulo",
        ],
        "costo": "203 pesos",
        "tiempo_respuesta": "Mismo día (entrega inmediata)",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/antecedentes-penales",
        "fundamento_legal": "Ley Orgánica de la Fiscalía General del Estado de Baja California",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "constancia de residencia": {
        "nombre": "Constancia de Residencia",
        "descripcion": (
            "Documento emitido por el municipio que acredita que una persona reside "
            "en un domicilio determinado dentro del municipio. Se usa para trámites "
            "escolares, laborales y ante dependencias de gobierno."
        ),
        "dependencia": "Dirección de Gobierno Municipal (Delegaciones municipales)",
        "requisitos": [
            "Identificación oficial vigente",
            "Comprobante de domicilio reciente (no mayor a 3 meses)",
            "Llenar el formato de solicitud en el módulo",
        ],
        "costo": "Gratuito (en la mayoría de los municipios de Baja California)",
        "tiempo_respuesta": "Mismo día",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/constancia-residencia",
        "fundamento_legal": "Ley Orgánica Municipal del Estado de Baja California",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "inscripcion registro civil": {
        "nombre": "Solicitud de Inscripción al Registro Civil",
        "descripcion": (
            "Trámite mediante el cual los ciudadanos solicitan el registro de actos del "
            "estado civil, tales como nacimientos, matrimonios, divorcios y defunciones. "
            "El Registro Civil acredita mediante documentos la situación jurídica de las "
            "personas físicas en el Estado de Baja California."
        ),
        "dependencia": "Registro Civil del Estado de Baja California — Dirección del Registro Civil",
        "requisitos": [
            "Solicitud debidamente llenada y firmada (formato oficial)",
            "Identificación oficial vigente con fotografía (INE, pasaporte, cédula profesional)",
            "CURP del solicitante",
            "Comprobante de domicilio no mayor a 3 meses",
            "Documentos que acrediten el acto a registrar (acta hospitalaria, acta eclesiástica, etc.) "
            "según el tipo de inscripción",
            "Pago de derechos correspondiente",
        ],
        "costo": "Gratuito (primera acta de nacimiento); $50 pesos copias adicionales; "
                 "$200 pesos acta de matrimonio",
        "tiempo_respuesta": "1 a 3 días hábiles",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/1650",
        "fundamento_legal": "Ley del Registro Civil del Estado de Baja California; "
                            "Código Civil del Estado de Baja California",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "licencia de funcionamiento": {
        "nombre": "Licencia de Funcionamiento",
        "descripcion": (
            "Autorización que otorga el gobierno estatal a personas físicas o morales para "
            "operar legalmente un establecimiento comercial, industrial o de servicios dentro "
            "del territorio del Estado de Baja California. Garantiza que el establecimiento "
            "cumple con los requisitos de seguridad, sanidad, uso de suelo y demás "
            "disposiciones legales aplicables."
        ),
        "dependencia": "Dirección de Licencias y Permisos — Subdirección de Permisos Comerciales",
        "requisitos": [
            "Solicitud oficial debidamente llenada y firmada",
            "Identificación oficial vigente del propietario o representante legal",
            "RFC y CURP del solicitante",
            "Acta constitutiva (para personas morales) y poder notarial del representante",
            "Comprobante de domicilio del establecimiento no mayor a 3 meses",
            "Permiso de uso de suelo vigente compatible con la actividad",
            "Dictamen de protección civil favorable",
            "Pago de derechos correspondiente al giro del negocio",
        ],
        "costo": "$800 pesos (giro de bajo impacto) / $1,500 pesos (mediano impacto) / "
                 "$3,000 pesos (alto impacto); renovación anual: 50% del costo original",
        "tiempo_respuesta": "5 a 10 días hábiles",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/661",
        "fundamento_legal": "Ley de Establecimientos Mercantiles del Estado de Baja California; "
                            "Reglamento de Licencias de Funcionamiento",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "permiso de uso de suelo": {
        "nombre": "Permiso de Uso de Suelo",
        "descripcion": (
            "Autorización que emite la Secretaría de Desarrollo Urbano mediante la cual se "
            "permite o condiciona el uso o el cambio de uso del suelo de un predio, conforme "
            "a los planes y programas de desarrollo urbano vigentes. Es indispensable para el "
            "establecimiento de negocios, construcciones nuevas y cambios de giro."
        ),
        "dependencia": "Secretaría de Desarrollo Urbano y Sustentabilidad — Dirección de Planeación Urbana",
        "requisitos": [
            "Solicitud oficial con datos del predio y actividad solicitada",
            "Identificación oficial del propietario o representante legal",
            "Copia del título de propiedad o contrato de arrendamiento notariado",
            "Croquis de localización y plano del predio (acotado, con colindancias)",
            "Boleta predial al corriente de pago",
            "Descripción detallada de la actividad o giro que se pretende desarrollar",
            "Pago de derechos de revisión",
        ],
        "costo": "$600 pesos (revisión y dictamen); $2,500 pesos (cambio habitacional a comercial); "
                 "$5,000 pesos (cambio comercial a industrial)",
        "tiempo_respuesta": "10 a 20 días hábiles",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/652",
        "fundamento_legal": "Ley de Desarrollo Urbano del Estado de Baja California; "
                            "Programa Estatal de Desarrollo Urbano",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    "certificado de estudios": {
        "nombre": "Expedición de Certificado de Estudios",
        "descripcion": (
            "Trámite mediante el cual la Secretaría de Educación Pública del Estado expide el "
            "certificado oficial que acredita la conclusión de un nivel educativo (preescolar, "
            "primaria, secundaria, bachillerato o equivalente) en una institución pública del "
            "estado. Tiene validez oficial para trámites laborales, académicos y migratorios."
        ),
        "dependencia": "Secretaría de Educación Pública del Estado de Baja California (SEPBC) — "
                       "Dirección de Control Escolar",
        "requisitos": [
            "Solicitud oficial firmada por el interesado o tutor (menores de edad)",
            "Identificación oficial vigente con fotografía",
            "CURP",
            "Acta de nacimiento",
            "Boletas o calificaciones de todos los grados del nivel educativo correspondiente",
            "Nombre y clave del centro educativo donde se realizaron los estudios",
            "Pago de derechos (aplica para duplicados y expediciones posteriores a 1 año de egreso)",
        ],
        "costo": "Gratuito (primera expedición, recién egresado); $350 pesos (duplicado por extravío); "
                 "$500 pesos (apostille para uso en el extranjero)",
        "tiempo_respuesta": "5 a 15 días hábiles",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/1618",
        "fundamento_legal": "Ley General de Educación; Ley de Educación del Estado de Baja California; "
                            "Acuerdo Secretarial 286",
        "horario": "Lunes a viernes de 8:00 a 15:00 horas",
        "modalidad": "presencial",
    },
    # ── Fichas reales RETyS BC (fichas-dificiles.json) ────────────────────────
    "cespt_041": {
        "nombre": "Registro o Revalidación de Exención de Permiso de Descarga de Aguas Residuales para Comercios y Empresas de Servicios",
        "descripcion": "Solicitar la exención del trámite de permiso de descargas, debido a que no se generan aguas residuales de procesos de producción de bienes o servicios.",
        "dependencia": "Comisión Estatal de Servicios Públicos de Tijuana",
        "requisitos": [
            "Original y copia de la Solicitud de Exención FRM-022 debidamente llenado y firmado",
            "Copia de Constancia de Situación Fiscal de la empresa",
            "Fotografías a color de las áreas del interior de la empresa",
            "Copia de documentales que acrediten la no generación de descargas de aguas residuales de proceso",
        ],
        "costo": "COSTO VARIABLE: Por expedición: $1,7999.46 pesos | Por la revalidación anual: $976.71 pesos | Septiembre 2026",
        "tiempo_respuesta": "30 Días Hábiles",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/1634",
        "fundamento_legal": "Ley Que Reglamenta El Servicio De Agua Potable En El Estado De Baja California Artículos 94 y 109; "
                            "Ley de Comisiones Estatales de Servicios Públicos del Estado De Baja California Artículos 1 y 2; "
                            "Ley de Ingresos del Estado de Baja California para el Ejercicio Fiscal del año 2026 Artículo 9",
        "horario": "",
        "modalidad": "presencial",
    },
    "sh_licencia_conducir": {
        "nombre": "Expedición de Licencia de Conducir",
        "descripcion": "Colaborar con el ciudadano para cumplir con los requisitos para obtener su licencia de conducir.",
        "dependencia": "Secretaría de Hacienda de Baja California",
        "requisitos": [
            "Cita",
            "Solicitud del trámite (formato de manifiesto en la Recaudación de Rentas)",
            "Identificación oficial con fotografía vigente (INE, pasaporte, cédula, matrícula consular, cartilla militar) — original y copia",
            "Comprobante de domicilio no mayor a tres meses — original y copia",
            "Certificado médico de institución pública o privada — original y copia",
            "Carta de no antecedentes penales (últimos 5 años)",
            "Examen antidoping",
            "Certificado de estudios con fotografía (mínimo primaria; solo licencias tipo B y D)",
            "Aprobar exámenes teórico y práctico de manejo con tarjeta de circulación vigente",
            "Pago correspondiente (efectivo, cheque certificado, tarjeta débito/crédito excepto American Express)",
        ],
        "costo": "COSTO VARIABLE: Mes de Septiembre de 2026. Automovilista 3 años $1,120.39 M.N. | 5 años $1,493.85 M.N. | "
                 "Motociclista 3 años $1,120.39 M.N. | 5 años $1,493.85 M.N. | Chofer C 3 años $1,278.47 M.N. | "
                 "5 años $1,704.63 M.N. | Chofer A, B Y D $2,108.06 M.N. | Motociclista y automóvil 16-18 años $827.38 M.N. | "
                 "Licencia Provisional hasta 9 meses $959.80 M.N.",
        "tiempo_respuesta": "45 Minutos",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/661",
        "fundamento_legal": "Ley de Ingresos del Estado de Baja California para el Ejercicio Fiscal del Año 2025, "
                            "Artículo 10, Fracción I, Inciso A; "
                            "Ley que Regula los Servicios de Control Vehicular en el Estado de Baja California, Artículos 34 y 36",
        "horario": "",
        "modalidad": "presencial",
    },
    "cejum_001": {
        "nombre": "Atención Integral a Mujeres Víctimas de Violencia",
        "descripcion": "Asesoría psicológica, asesoría legal, trabajo social, atención médica preventiva, ludoteca, estancia transitoria, área de empoderamiento y prevención.",
        "dependencia": "Centro de Justicia para las Mujeres del Estado de Baja California",
        "requisitos": [
            "Identificación Oficial",
        ],
        "costo": "Sin costo",
        "tiempo_respuesta": "30 Minutos",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/1238",
        "fundamento_legal": "Código Nacional de Procedimientos Penales Artículos 17, 18, 109, 110, 259, 261, 262, 272, 275, 277, 366, 368, 369 y 370",
        "horario": "",
        "modalidad": "presencial",
    },
    "shfp_002": {
        "nombre": "Constancia de no inhabilitación.",
        "descripcion": "Trámite a través del cual la Secretaría Anticorrupción y Buen Gobierno acredita que el solicitante no cuenta con inhabilitación vigente para desempeñar un empleo, cargo o comisión.",
        "dependencia": "Secretaría Anticorrupción y Buen Gobierno",
        "requisitos": [
            "Registro Federal de Contribuyentes (RFC)",
            'Indicar a qué dependencia se debe enviar la constancia (o "a quien corresponda")',
            "Original y copia de identificación oficial vigente (INE, pasaporte, cédula profesional, cartilla militar, licencia de conducir con CURP)",
            "Formato para obtener la constancia de no inhabilitación",
            'Recibo original del pago de derechos (recaudación de rentas, "Farmacias Roma" o bancos)',
        ],
        "costo": "COSTO VARIABLE: $132.00 M.N. (actualizándose mensualmente conforme al Transitorio Séptimo de la Ley de Ingresos del Estado de Baja California para el ejercicio fiscal del año 2026)",
        "tiempo_respuesta": "48 Horas",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/1131",
        "fundamento_legal": "LEY DE INGRESOS DEL ESTADO DE BAJA CALIFORNIA PARA EL EJERCICIO FISCAL DEL AÑO 2026 18, FRACCIÓN V, INCISO E) DEL CAPÍTULO VII; "
                            "REGLAMENTO INTERNO DE LA SECRETARÍA ANTICORRUPCIÓN Y BUEN GOBIERNO 32 Y 36 FRACCIÓN XIII",
        "horario": "",
        "modalidad": "presencial / en línea",
    },
    "sscbc_022": {
        "nombre": "Expedición de Constancia de Antecedentes Penales",
        "descripcion": "Documento donde se hace constar que el ciudadano cuenta o no con antecedentes penales de carácter doloso del fuero común en el Estado de Baja California.",
        "dependencia": "Secretaría de Seguridad Ciudadana del Estado de Baja California",
        "requisitos": [
            "Identificación oficial vigente (credencial de elector, pasaporte mexicano, licencia de conducir BC, cartilla del servicio militar nacional liberada, cédula profesional con foto, título profesional)",
            "Pago de derechos",
        ],
        "costo": "COSTO: $284.38 pesos",
        "tiempo_respuesta": "5 Minutos",
        "url_oficial": "https://retys.bajacalifornia.gob.mx/Portal/TyS/1618",
        "fundamento_legal": "Ley Nacional de Ejecución Penal Artículo 27 fracción IV; "
                            "Ley Orgánica del Poder Ejecutivo del Estado de Baja California Artículo 34 fracción XXXVI; "
                            "Ley de Ingresos del Estado de Baja California para el ejercicio fiscal del año 2026 Artículo 18, fracción I, inciso H",
        "horario": "",
        "modalidad": "presencial / en línea",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Mapping homoclave → clave TRAMITES_DB  (usado por los endpoints de admin)
# ─────────────────────────────────────────────────────────────────────────────

HOMOCLAVE_MAP: dict[str, str] = {
    # Fichas simuladas originales (mantenidas para no romper filas existentes en SQLite)
    "BC-TYS-1650": "inscripcion registro civil",
    "BC-TYS-0661": "licencia de funcionamiento",
    "BC-TYS-0652": "permiso de uso de suelo",
    "BC-TYS-1618": "certificado de estudios",
    "BC-TYS-1582": "antecedentes penales",
    # Fichas reales RETyS BC
    "BC-CESPT-041": "cespt_041",
    "BC-SH-012":    "sh_licencia_conducir",
    "BC-CEJUM-001": "cejum_001",
    "BC-SHFP-002":  "shfp_002",
    "BC-SSCBC-022": "sscbc_022",
}

# ─────────────────────────────────────────────────────────────────────────────
# Lógica de búsqueda
# ─────────────────────────────────────────────────────────────────────────────

def _normalizar(texto: str) -> str:
    """Quita tildes y pasa a minúsculas para comparación robusta."""
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def buscar_tramite(nombre: str, tipo: str = "parcial") -> list[dict]:
    """
    Busca trámites en TRAMITES_DB.

    Args:
        nombre: Nombre del trámite a buscar.
        tipo:   "exacta" — la clave debe coincidir exactamente (normalizada).
                "parcial" — el término puede estar contenido en la clave o en el
                            campo 'nombre' del trámite.

    Returns:
        Lista de fichas de trámite que coinciden (puede ser vacía).
    """
    aguja = _normalizar(nombre)
    resultados = []

    for clave, ficha in TRAMITES_DB.items():
        clave_norm = _normalizar(clave)
        nombre_norm = _normalizar(ficha["nombre"])

        if tipo == "exacta":
            if aguja == clave_norm:
                resultados.append(ficha)
        else:  # parcial
            if aguja in clave_norm or aguja in nombre_norm or clave_norm in aguja:
                resultados.append(ficha)

    return resultados


def ejecutar_skill(argumentos: dict) -> str:
    """
    Punto de entrada que el agente llama cuando el modelo invoca la tool.

    Args:
        argumentos: dict con las claves del JSON Schema:
                    - nombre_tramite (str, requerido)
                    - tipo_busqueda  (str, opcional; default "parcial")

    Returns:
        JSON string con la ficha del trámite o un mensaje de error con la
        lista de trámites disponibles.
    """
    nombre = argumentos.get("nombre_tramite", "").strip()
    tipo = argumentos.get("tipo_busqueda", "parcial")

    if not nombre:
        return json.dumps(
            {"error": "Debes indicar el nombre del trámite a buscar."},
            ensure_ascii=False,
        )

    resultados = buscar_tramite(nombre, tipo)

    if not resultados:
        disponibles = [f["nombre"] for f in TRAMITES_DB.values()]
        return json.dumps(
            {
                "encontrado": False,
                "mensaje": (
                    f"No encontré el trámite '{nombre}' en el catálogo de RETyS BC. "
                    "Estos son los trámites disponibles:"
                ),
                "tramites_disponibles": disponibles,
            },
            ensure_ascii=False,
            indent=2,
        )

    # Si hay más de un resultado, devolvemos el primero (el más relevante)
    ficha = resultados[0]
    return json.dumps(
        {"encontrado": True, "tramite": ficha},
        ensure_ascii=False,
        indent=2,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Pruebas rápidas (ejecutar directamente: python skill_retys.py)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    casos = [
        {"nombre_tramite": "licencia de conducir"},
        {"nombre_tramite": "pasaporte", "tipo_busqueda": "exacta"},
        {"nombre_tramite": "tramite inexistente"},
    ]
    for caso in casos:
        print(f"\n── Consulta: {caso} ──")
        print(ejecutar_skill(caso))
