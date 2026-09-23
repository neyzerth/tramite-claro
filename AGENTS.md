# Agentes de Trámite Claro

Este documento describe los agentes de IA que componen Trámite Claro,
sus responsabilidades, tecnologías, entradas/salidas y criterios de activación.

---

## Agente Orquestador

**Rol:** Punto de entrada principal. Recibe la solicitud del ciudadano,
determina la intención y delega al agente especializado correspondiente.
Gestiona el flujo de la conversación de inicio a fin.

**Tecnología:** IBM watsonx.ai

**Entradas:** Mensaje de texto del usuario, historial de conversación, canal de origen.

**Salidas:** Respuesta final al usuario (texto y/o audio).

**Herramientas disponibles:**
- `invoke_simplification_agent` — delega al Agente de Simplificación
- `invoke_tts_agent` — delega al Agente de Voz
- `invoke_guide_agent` — delega al Agente de Guía de Trámites

---

## Agente de Simplificación (Lectura Fácil)

**Rol:** Recibe el texto oficial de un trámite (proveniente del RETyS) y lo
reescribe siguiendo los principios de Lectura Fácil: oraciones cortas,
vocabulario sencillo, estructura clara y sin ambigüedades.

**Tecnología:** IBM watsonx.ai

**Entradas:** Texto burocrático original del trámite.

**Salidas:** Texto simplificado en formato Lectura Fácil.

**Criterios de activación:** El Orquestador lo llama cuando el usuario solicita
información sobre un trámite y se detecta que el texto fuente requiere simplificación.

**Referencia:** `docs/Resumen-pautas-lectura-facil.pdf`

---

## Agente de Voz (TTS)

**Rol:** Convierte texto simplificado en audio narrado para usuarios con
discapacidad visual, baja alfabetización o preferencia auditiva.

**Tecnología:** IBM watsonx Speech (Text-To-Speech)

**Entradas:** Texto simplificado (salida del Agente de Simplificación o respuesta del Orquestador).

**Salidas:** Archivo de audio (MP3/WAV) con la narración del texto.

**Criterios de activación:** El Orquestador lo llama cuando el canal lo soporta
y el usuario activa el modo de voz, o cuando se detecta que el usuario tiene
preferencia auditiva.

---

## Agente de Guía de Trámites

**Rol:** Guía al ciudadano paso a paso a través del proceso de un trámite específico.
Consulta el catálogo del RETyS para obtener los requisitos, pasos y documentos necesarios,
y los presenta de forma progresiva y conversacional.

**Tecnología:** IBM watsonx.ai

**Entradas:** Nombre o tipo de trámite solicitado por el usuario.

**Salidas:** Secuencia de pasos simplificados, lista de requisitos y documentos,
y confirmación de disponibilidad digital del trámite.

**Herramientas disponibles:**
- `get_tramite_info` — consulta el RETyS para obtener datos del trámite
- `check_digital_availability` — verifica si el trámite puede realizarse en línea

**Criterios de activación:** El Orquestador lo llama cuando el usuario expresa
la intención de realizar o conocer los pasos de un trámite específico.