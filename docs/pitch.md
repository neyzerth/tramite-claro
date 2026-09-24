# Trámite Claro — Guión del Pitch (5 minutos)

> **Audiencia:** Técnicos IBM + Funcionarios del Gobierno de Baja California
> **Duración:** 5 minutos (~700 palabras de lectura en voz pausada)
> **Formato:** Presentación oral con diapositivas de apoyo

---

## Sección 1 — El Problema (45 segundos)

> 🎯 *[Diapositiva: cifras MUAC 2024 + número de trámites RETyS]*

Baja California tiene **731 trámites en el RETyS**, 141 de ellos disponibles en línea.
Tiene el MUAC: 10 canales activos, más de **270 mil atenciones en 2024**, 90% de satisfacción.
Es el estado más avanzado del país en atención ciudadana digital.

Y sin embargo, hay un problema que los números no muestran:

**La mayoría de los ciudadanos que más necesitan esos servicios no pueden entenderlos.**

El lenguaje del RETyS es burocrático, técnico, denso.
Para una persona con discapacidad cognitiva, para un adulto mayor,
para alguien con baja escolaridad o cuya primera lengua es la Lengua de Señas Mexicana —
ese lenguaje es una pared.

Y ante esa pared, la respuesta siempre ha sido la misma: **ir a la ventanilla**.

La digitalización no resuelve la exclusión si el lenguaje sigue siendo el mismo.

---

## Sección 2 — La Innovación (45 segundos)

> 🎯 *[Diapositiva: logo de Trámite Claro + los 3 diferenciales]*

**Trámite Claro** es un asistente de IA que guía al ciudadano a través de cualquier
trámite del RETyS usando el estándar internacional de **Lectura Fácil**:
oraciones cortas, vocabulario accesible, pasos claros, sin ambigüedades.

No es un buscador. No es un FAQ. Es un guía conversacional que:

1. **Explica paso a paso** cómo realizar el trámite, en el lenguaje que el ciudadano puede entender.
2. **Adapta el contenido** siguiendo los principios de Lectura Fácil — el mismo estándar
   que el MUAC ya exige en sus protocolos, pero que hoy no existe en el RETyS.
3. **Habla** — genera audio de las instrucciones para quienes no pueden leer el texto o
   prefieren escuchar.

Y lo más importante: **se integra al MUAC existente**.
No reemplaza nada. Le agrega inteligencia a los canales que ya tienen:
WhatsApp, chat, web, módulos físicos.

---

## Sección 3 — Por qué IBM Bob e IA (1 minuto)

> 🎯 *[Diapositiva: arquitectura con los tres agentes + logos de watsonx]*

La solución tiene tres agentes de IA que trabajan en conjunto:

- **Agente de Simplificación:** usa **IBM watsonx.ai** para reescribir el texto burocrático
  del RETyS siguiendo las pautas de Lectura Fácil. No es solo parafrasear —
  es una transformación estructural: detecta términos técnicos, divide instrucciones complejas
  y produce una versión que cualquier ciudadano puede seguir.

- **Agente de Voz:** usa **IBM watsonx Speech (TTS)** para convertir esas instrucciones
  simplificadas en audio. Esto cubre a personas con discapacidad visual, baja alfabetización
  o usuarios de LSM para quienes el español escrito es su segunda lengua.

- **Agente Orquestador:** recibe la intención del ciudadano y coordina a los otros agentes
  para dar una respuesta coherente, paso a paso y en el canal correcto.

Usamos **IBM Bob** como herramienta central de desarrollo durante el hackathon:
planeación de la arquitectura de agentes, generación de código, revisión técnica y documentación —
todo en el mismo flujo. Bob no fue solo una herramienta: fue parte del equipo.

La elección de IBM no es solo tecnológica: es estratégica.
Los datos de los ciudadanos de Baja California **no salen de IBM Cloud**.
Para el gobierno, eso significa confianza y cumplimiento normativo desde el primer día.

---

## Sección 4 — Impacto y Propuesta de Valor (1 minuto)

> 🎯 *[Diapositiva: tres columnas: Ciudadano / Gobierno / Comunidad + cifras clave]*

**Para el ciudadano:**
Autonomía real. Resolver un trámite sin intermediarios, sin salir de casa,
sin sentir vergüenza por no entender un formulario. Eso no es comodidad — es dignidad.

Hay **más de 94 mil personas sordas o con debilidad auditiva en BC**.
El MUAC inauguró atención en LSM en marzo 2025 — un logro histórico.
Pero al primer aniversario, ese canal acumuló apenas **37 horas de atención total**
frente a una comunidad de casi 100 mil personas.
El cuello de botella no es la voluntad: son las horas de intérprete.
Trámite Claro libera esas horas para los casos que de verdad lo necesitan,
respondiendo las dudas de trámite que hoy saturan ese canal.

**Para el gobierno:**
El MUAC atendió **+270 mil solicitudes en 2024**. Cada consulta resuelta por IA
es tiempo del analista recuperado para casos complejos.
Además, cada interacción genera datos accionables: qué trámites confunden más,
dónde se abandona el proceso — inteligencia de servicio público que hoy no existe.

**Para la comunidad:**
BC ya tiene el modelo. La ADBC incluso ofrece su código a otros estados.
Con Trámite Claro encima, ese modelo se convierte en un **kit de accesibilidad exportable**
que otros gobiernos pueden adoptar sin partir de cero.

---

## Sección 5 — Viabilidad y Escalabilidad (1 minuto)

> 🎯 *[Diapositiva: mapa de expansión BC → Nacional → LATAM]*

La integración es por API sobre la infraestructura existente del MUAC.
El ciudadano no aprende nada nuevo. El funcionario no cambia su flujo.
**Trámite Claro se conecta a lo que ya existe.**

La fuente de datos es el RETyS, que ya está estructurado:
**731 trámites disponibles, todos accesibles desde el primer sprint.**

**¿Puede crecer?** Sí, y de forma natural:

- **Fase 1:** Piloto con los trámites más consultados del MUAC — canal web + WhatsApp.
- **Fase 2:** Cobertura completa del RETyS. Integración con los módulos físicos LSM (tablets en sedes).
- **Fase 3:** La ADBC ya quiere exportar su modelo a otros estados. Trámite Claro viaja con él.
- **Fase 4:** El problema del lenguaje burocrático no es exclusivo de BC — el patrón aplica
  a cualquier portal de gobierno en LATAM.

El estándar de Lectura Fácil existe en español, inglés y otros idiomas.
La arquitectura de agentes es reutilizable. El costo marginal de expansión es bajo.

---

## Sección 6 — Cierre y Call to Action (30 segundos)

> 🎯 *[Diapositiva: logo + tagline "Trámites sin barreras para todas y todos"]*

Baja California ya tiene la infraestructura.
Ya tiene los trámites digitalizados.
Ya tiene el MUAC — el canal ciudadano más avanzado del país.

Lo que faltaba era que alguien le hablara al ciudadano en su idioma.

**Trámite Claro hace exactamente eso.**

El siguiente paso que proponemos:
**Un piloto de 90 días con los trámites más consultados del MUAC,
integrado al canal web y WhatsApp, con métricas de adopción y satisfacción ciudadana.**

Gracias.

---

## Notas para el Presentador

- **Tono:** Cálido con el gobierno (dignidad, autonomía, servicio), técnico con IBM (agentes, watsonx, API).
- **Énfasis emocional clave:** El dato de las 37 horas de LSM vs. 94 mil personas sordas en BC — es el momento más poderoso del pitch. Pausa ahí.
- **Demo (si aplica):** Mostrar el flujo conversacional después de la Sección 2 (La Innovación).
- **Evitar:** No decir "solo es un chatbot". Es un sistema de agentes especializados con contexto de accesibilidad.
- **Cifras ancla a repetir:** "731 trámites en el RETyS" y "270 mil atenciones en 2024" — úsalas para validar que BC ya tiene escala.
- **Argumento diferenciador frente a otros equipos:** No construimos infraestructura nueva. Amplificamos la que BC ya construyó.
