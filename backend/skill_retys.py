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
