# Trámite Claro

> Trámites sin barreras para todas y todos.

**Trámite Claro** es un servicio de asistencia ciudadana con Inteligencia Artificial
que se integra a los canales existentes del MUAC (Módulo Único de Atención Ciudadana)
de Baja California. Convierte la información burocrática del RETyS en una experiencia
de orientación clara, interactiva e incluyente.

---

## El Problema

En Baja California, los ciudadanos pueden realizar trámites gubernamentales de forma
digital a través del MUAC y el RETyS (Registro Estatal de Trámites y Servicios).
Sin embargo, el lenguaje utilizado en estos portales es complejo y altamente burocrático,
lo que genera una barrera de acceso real para un segmento significativo de la población.

Esto provoca una **dependencia forzada en las ventanillas presenciales del Estado**,
haciendo que el ciudadano pierda autonomía, privacidad y dignidad.

---

## La Solución

Trámite Claro es un chatbot guiado que:

- Explica paso a paso cómo realizar cualquier trámite digital disponible.
- Adapta el lenguaje a los principios de **Lectura Fácil**.
- Responde en texto y en voz según las necesidades del usuario.

La solución se expone como una **API (FastAPI)** que el MUAC consume a través de sus
canales existentes (web, WhatsApp, llamadas, correo), acompañada de un portal web
de simulación desarrollado en **React**.

---

## Usuarios Objetivo

| Perfil | Barrera principal |
|---|---|
| Personas con discapacidad cognitiva | Vocabulario complejo e instrucciones confusas |
| Personas con discapacidad auditiva | Dependencia de atención presencial verbal |
| Personas con baja alfabetización | Textos extensos sin apoyo visual ni oral |
| Adultos mayores | Interfaces poco amigables y lenguaje técnico |

---

## Casos de Uso con IA

| Componente | Tecnología | Función |
|---|---|---|
| Simplificación de documentos | IBM watsonx.ai | Reescribe las instrucciones de cada trámite siguiendo la estructura de Lectura Fácil |
| Diálogos por voz | IBM watsonx Speech (TTS) | Genera audio de las instrucciones para personas con discapacidad visual o baja alfabetización |
| Asistente conversacional | IBM watsonx.ai | Guía al ciudadano a través del flujo del trámite seleccionado |

---

## Arquitectura

```
Canales MUAC (Web / WhatsApp / Teléfono / Correo)
│
▼
Trámite Claro API  ◄──────────────  RETyS (Catálogo de Trámites)
├── Agente Orquestador
├── Agente de Simplificación (Lectura Fácil)  →  watsonx.ai
├── Agente de Voz (TTS)                       →  watsonx Speech
└── Agente de Guía de Trámites                →  watsonx.ai

```
---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| API Backend | FastAPI (Python) |
| Portal Web (simulación) | React |
| IA — Texto | IBM watsonx.ai |
| IA — Voz | IBM watsonx Speech (TTS) |
| Desarrollo asistido | IBM Bob |
| Datos de trámites | RETyS — Baja California |
| Canal ciudadano | MUAC — Módulo Único de Atención Ciudadana |

---

## Licencia

Consultar [LICENSE](./LICENSE).