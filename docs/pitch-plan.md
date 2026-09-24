# Plan: Pitch de Trámite Claro — Hackathon

## Objetivo

Producir el guión estructurado del pitch de 5 minutos de **Trámite Claro**,
orientado a una audiencia mixta de técnicos IBM y funcionarios del gobierno de Baja California.
El documento final se guarda en `docs/pitch.md`.

El pitch debe responder con claridad los 4 ejes de evaluación del hackathon:
1. El problema y la innovación
2. La relevancia del uso de Bob y la IA
3. Impacto y propuesta de valor
4. Viabilidad y escalabilidad

---

## Sub-Tareas

---

### Sub-Tarea 1 — Sección: Hook y Problema

**Intent:** Capturar la atención del jurado en los primeros 45 segundos con un dato de impacto
y dejar claro cuál es la barrera real que enfrenta el ciudadano.

**Expected Outcomes:**
- Párrafo de apertura con dato concreto (ej. ~300 trámites en RETyS, porcentaje de atención presencial)
- Descripción del problema en lenguaje de gobierno (exclusión digital, pérdida de autonomía)
- Enunciado claro del problema central: "el lenguaje burocrático excluye a quienes más necesitan el servicio"

**Todo List:**
- [ ] Redactar hook de apertura con dato del RETyS (~300 trámites digitalizados en BC)
- [ ] Describir la barrera: lenguaje técnico/burocrático inaccesible
- [ ] Nombrar los perfiles afectados (adultos mayores, baja alfabetización, discapacidad cognitiva/auditiva)
- [ ] Concluir con la pregunta-problema: ¿de qué sirve digitalizar si nadie puede entender cómo usarlo?

**Relevant Context:** `README.md` sección "El Problema", tabla de usuarios objetivo

**Status:** [ ] pending

---

### Sub-Tarea 2 — Sección: La Innovación

**Intent:** Describir qué hace Trámite Claro de forma concreta y por qué es una solución
nueva, no solo otro chatbot.

**Expected Outcomes:**
- Descripción en 3 puntos de la propuesta diferenciadora
- Mención explícita del estándar de Lectura Fácil como eje de innovación
- Distinguir claramente: no es un buscador, es un guía conversacional con lenguaje adaptado

**Todo List:**
- [ ] Definir la propuesta en una sola oración poderosa ("Trámite Claro es...")
- [ ] Listar los 3 diferenciales: guía paso a paso, Lectura Fácil, voz
- [ ] Mencionar la integración al canal existente (MUAC) como ventaja — no requiere nueva infraestructura
- [ ] Vincular la innovación al contexto del RETyS (datos reales del catálogo estatal)

**Relevant Context:** `README.md` sección "La Solución", `docs/Plan-AGENTS.md`

**Status:** [ ] pending

---

### Sub-Tarea 3 — Sección: Relevancia de Bob e IA

**Intent:** Justificar ante los técnicos de IBM por qué watsonx y Bob son la elección
correcta, más allá de ser el patrocinador del hackathon.

**Expected Outcomes:**
- Mapa claro de qué hace cada componente IBM (watsonx.ai, Speech TTS, Bob)
- Argumento de valor: Bob como acelerador del desarrollo del hackathon (calidad + velocidad)
- Argumento técnico: watsonx.ai como motor de simplificación con prompts especializados en Lectura Fácil
- Argumento diferenciador: soberanía de datos con IBM Cloud vs. soluciones externas

**Todo List:**
- [ ] Describir el rol de watsonx.ai en la simplificación de lenguaje burocrático
- [ ] Describir el rol de watsonx Speech TTS para accesibilidad auditiva
- [ ] Describir el rol de Bob como herramienta de desarrollo: planeación, generación de código, agentes
- [ ] Agregar argumento de confianza/soberanía para el gobierno (IBM Cloud, datos en BC)

**Relevant Context:** `README.md` sección "Casos de Uso con IA" y "Stack Tecnológico"

**Status:** [ ] pending

---

### Sub-Tarea 4 — Sección: Impacto y Propuesta de Valor

**Intent:** Cuantificar y cualificar el beneficio que genera la solución para los
tres actores clave: ciudadanos, gobierno y comunidad.

**Expected Outcomes:**
- Propuesta de valor clara para cada actor (ciudadano, gobierno, comunidad)
- Al menos un indicador medible por actor (tiempo, costo, autonomía, descongestión)
- Framing emocional para los funcionarios: dignidad ciudadana y modernización del Estado

**Todo List:**
- [ ] Redactar beneficio para el ciudadano: autonomía, dignidad, acceso sin intermediarios
- [ ] Redactar beneficio para el gobierno: descongestión de ventanillas, trazabilidad, imagen de modernización
- [ ] Redactar beneficio para la comunidad: inclusión digital real, reducción de brecha de acceso
- [ ] Incluir métricas o estimados: si el 20% de consultas presenciales se digitalizan, ¿cuánto ahorra el Estado?

**Relevant Context:** `README.md` tabla de usuarios objetivo, datos del MUAC

**Status:** [ ] pending

---

### Sub-Tarea 5 — Sección: Viabilidad y Escalabilidad

**Intent:** Demostrar que la solución es implementable en el corto plazo y que puede
crecer más allá de Baja California.

**Expected Outcomes:**
- Argumento de integración sin fricción (API sobre el MUAC existente, sin reemplazar infraestructura)
- Ruta de escalabilidad: otros estados, otros países hispanohablantes
- Modelo de replicabilidad: el catálogo RETyS es un patrón que otros gobiernos pueden adoptar

**Todo List:**
- [ ] Describir la integración técnica con el MUAC como API sin reemplazar lo existente
- [ ] Argumentar el bajo costo de adopción (no requiere capacitación masiva de funcionarios)
- [ ] Proponer ruta de expansión: BC → otros estados con RETyS → LATAM con portales similares
- [ ] Mencionar el modelo de mantenimiento vía IBM Cloud

**Relevant Context:** `README.md` sección "Arquitectura"

**Status:** [ ] pending

---

### Sub-Tarea 6 — Sección: Cierre y Call to Action

**Intent:** Cerrar con fuerza, dejar una frase memorable y una acción concreta que
el jurado pueda tomar.

**Expected Outcomes:**
- Frase de cierre poderosa que refuerce el nombre y propósito de la solución
- Call to action específico: siguiente paso concreto (piloto en X municipio, alianza con MUAC, etc.)

**Todo List:**
- [ ] Redactar frase de cierre que conecte el nombre "Trámite Claro" con su propósito
- [ ] Proponer un siguiente paso concreto y realista como call to action
- [ ] Confirmar que el guión completo cabe en 5 minutos (~650-700 palabras de lectura)

**Relevant Context:** Todo el pitch

**Status:** [ ] pending

---

## Archivo de Salida

`docs/pitch.md` — Guión completo del pitch, estructurado por secciones con notas de presentación.
