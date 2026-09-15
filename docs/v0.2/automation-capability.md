# Capacidad de arquitectura de automatización

> **2026-09-09.** El hueco confirmado. Diseño, no implementación.

---

## 1. El hueco, verificado

| Capacidad | Quién la cubre hoy |
|---|---|
| ¿Automatizar o hacerlo a mano? | 🟢 `coo-graham` — con regla de volumen explícita |
| **Cómo se arquitecta un flujo** | 🔴 **nadie** |
| Idempotencia · reintentos · dead-letter | 🔴 **nadie** |
| Frontera orquestador / dominio | 🔴 **nadie** |
| Adaptadores de proveedor | 🔴 **nadie** |
| Handoff humano | 🔴 **nadie** |
| Observabilidad de flujos | 🔴 **nadie** |

Lo más cercano es `devops-hightower`, que cubre **infraestructura** —dónde corre, cómo se
despliega, qué hacer si se cae—, no **flujos de negocio**.

`coo-graham` decide *si*. Nadie decide *cómo*. Y la fase que viene en el proyecto
consumidor es entera de *cómo*.

---

## 2. Por qué es urgente y no teórico

La fase de arquitectura de un proyecto consumidor real produjo un paquete sustancial de
diseño y varios ADRs sobre exactamente este dominio: fronteras de n8n, outbox transaccional, idempotencia de
entrada y de salida, adaptadores, handoff. **Todo ese criterio vive en el repositorio
privado de ese proyecto.**

Es el sitio equivocado para el criterio genérico. Ese repositorio contiene *qué
construimos*; *cómo decidimos construirlo* pertenece aquí. Hoy, si se empieza otro
proyecto con automatizaciones, ese conocimiento no viaja.

**Ese es el problema observado.** No es "falta una skill": es que el criterio ya existe, ya
se pagó, y está atrapado en un producto.

---

## 3. Qué debe cubrir

Los quince puntos del encargo, agrupados por el momento en que se responden:

### Antes de tocar nada — la frontera

| # | Decisión |
|---|---|
| 1 | **Process mapping** — el proceso manual, paso a paso, con sus tiempos. Entrada: la ficha de `/discover` |
| 2 | **Trigger** — qué lo dispara: persona, reloj, evento, webhook |
| 3 | **Input schema** — qué datos entran y cuáles son obligatorios |
| 4 | **Frontera determinista** — qué decide el dominio y qué ejecuta el orquestador. La regla: *el orquestador vive después del commit y nunca es autoridad* |
| 5 | **Data ownership** — dónde vive el estado. **Nunca en el orquestador** |

### Al diseñar el flujo — la robustez

| # | Decisión |
|---|---|
| 6 | **Idempotencia** — entrada (clave del cliente) y salida (una entrega por evento y canal) |
| 7 | **Reintentos** — qué es reintentable y qué no. *Reintentar algo no idempotente es peor que fallar* |
| 8 | **Dead-letter y recuperación manual** — dónde cae lo que agotó reintentos |
| 9 | **Handoff humano** — quién se entera, con qué contexto, y en cuánto tiempo |
| 10 | **Failure modes** — qué se rompe y qué pasa entonces, uno a uno |

### Antes de entregar — la operación

| # | Decisión |
|---|---|
| 11 | **Integración de proveedor** — por adaptador, nunca llamada directa desde el dominio |
| 12 | **Credenciales** — dónde viven, quién rota, cada cuánto |
| 13 | **Observabilidad** — poder contestar *"¿salió el aviso?"* sin entrar en el orquestador |
| 14 | **Coste** — por ejecución y al mes. Se cobra una cuota; sin esto el margen es una suposición |
| 15 | **Runbook manual** — cómo se hace a mano cuando falla |

---

## 4. La pregunta que este dominio contesta mal por defecto

> **¿Esto necesita un modelo de lenguaje?**

De las automatizaciones catalogadas para los sectores de un proyecto real, **dos de cada
tres son calendarios, contadores y tablas de reglas**. Avisar 10/5/2 días antes es un cron.
Enrutar una avería de ascensor al mantenedor del ascensor es un `switch`.

La capacidad tiene que llevar el criterio de corte dentro, porque es el error más caro del
dominio y el más fácil de cometer con entusiasmo:

> Si la respuesta correcta se puede escribir como una tabla o una condición, el modelo no
> aporta: añade coste, latencia y una forma nueva de fallar en silencio.

---

## 5. Forma: ¿agente, skill o workflow?

| Forma | ¿Encaja? | Razonamiento |
|---|:--:|---|
| **AGENT** | ❌ | Un agente se justifica cuando falta **criterio y enrutado**. Aquí lo que falta es un **procedimiento**: quince decisiones en un orden concreto con un gate al final. Eso es una skill. Y ya hay quien aporta el criterio: `coo-graham` decide si, `dev-dhh` vigila la complejidad, `devops-hightower` el despliegue. Un agente nº 19 duplicaría a los tres y **no tendría ningún caso construido** |
| **SKILL** | ✅ | Reutilizable · tiene procedimiento · tiene gate (G4) · se invoca desde `/design`, desde build y desde `/release` |
| **WORKFLOW** | ❌ | No coordina varias capacidades: **es** una capacidad. Se invoca *dentro* de `/design` |
| **RULE** | 🟡 | La frontera orquestador/dominio es tan corta y tan siempre-aplicable que podría ser una regla. Pero sin las otras catorce decisiones alrededor no sirve de nada |

### Decisión: **una skill — `automation-architecture`**

**Anti-bloat gate:**

| Pregunta | Respuesta |
|---|---|
| ¿Resuelve un problema observado? | ✅ La fase siguiente de un proyecto consumidor, entera |
| ¿Existe algo que lo resuelva? | ❌ Verificado: nada en business-crew ni en saas-toolkit |
| ¿Puede ser sección de otro archivo? | ❌ Quince decisiones no caben en la sección de otro |
| ¿≥2 workflows lo usarán? | ✅ `/design`, build, `/release` |
| ¿Tiene owner? | ✅ Invocada por `/design`; el criterio de si automatizar sigue siendo de `coo-graham` |
| ¿Criterio para eliminarla? | ✅ Si tras 2 automatizaciones reales no aportó nada que `dev-dhh` no dijera ya |

### Y una ampliación, no un agente nuevo

`coo-graham` gana una línea en *"Cuándo NO aportas"*:

> *Cómo se arquitecta el flujo, una vez decidido que se automatiza → skill
> `automation-architecture`.*

Eso cierra el hueco de enrutado sin añadir una persona.

---

## 6. Estructura propuesta de la skill

Siguiendo la anatomía de `agent-skills` (ver [`agent-skills-study.md`](agent-skills-study.md)):

```
skills/automation-architecture/
  SKILL.md          ≤ 300 líneas
```

| Sección | Contenido |
|---|---|
| **Overview** | El orquestador ejecuta, el dominio decide, el estado vive fuera |
| **When to Use** | Tras un "sí" de `coo-graham`. **NO** para decidir si automatizar, ni para desplegar |
| **Core Process** | Las 15 decisiones de §3, en tres bloques |
| **El corte de IA** | §4, con la tabla determinista vs modelo |
| **Common Rationalizations** | Ver abajo |
| **Red Flags** | El orquestador guarda estado · un flujo sin rama de error · un `Wait` largo dentro del flujo · credenciales de base de datos en el orquestador |
| **Verification** | El gate G4, sus siete puntos |

### La tabla de racionalizaciones

Es la sección más distintiva del formato de `agent-skills`, y este dominio la necesita más
que ninguno:

| Racionalización | Realidad |
|---|---|
| *"Es un flujo pequeño, no hace falta idempotencia"* | Los pequeños son los que se reintentan sin que nadie mire. Dos citas es dos citas |
| *"El historial del orquestador ya me dice qué pasó"* | Se purga. Y se purga justo antes de que alguien pregunte |
| *"Meto un `Wait` de 24 h y listo"* | Si el orquestador se reinicia, el recordatorio desaparece. Y si se cancela la cita, el `Wait` sigue vivo |
| *"Le doy acceso a la base de datos, es más rápido"* | Salta el dominio, las restricciones y la auditoría. Estados imposibles sin nada que los explique |
| *"El runbook manual lo escribo después"* | Si no se puede escribir, el flujo no está listo para un cliente que paga |
| *"Le pongo IA para que clasifique"* | Si cabe en una tabla, la tabla es más barata, más rápida y auditable |

---

## 7. Lo que NO entra en esta skill

| Fuera | Dónde va |
|---|---|
| Si automatizar o hacerlo a mano | `coo-graham` |
| Dónde se aloja el orquestador | `devops-hightower` + ADR en el repositorio del proyecto |
| Workflows concretos de un cliente | El repositorio privado de ese proyecto |
| Credenciales | Ningún repositorio |
| Tutorial de n8n | No es nuestro trabajo. La skill es agnóstica de herramienta |

**La skill no menciona n8n como obligación.** Si mañana el orquestador es otro, la skill
sigue valiendo — y eso es lo que la hace genérica y, por tanto, propiedad de business-crew
y no de ningún proyecto concreto.

---

## 8. Cuándo se escribe

**No en esta fase.** Y tampoco inmediatamente después.

| Precondición | Estado |
|---|---|
| Aprobación humana | Pendiente |
| Ciclo comercial de descubrimiento cerrado | Pendiente |
| ≥1 automatización real decidida | Pendiente |

**El motivo del tercer punto:** una skill escrita antes del primer caso real documenta la
automatización que imaginamos, no la que hace falta. El criterio del proyecto consumidor ya existe y está
escrito; trasladarlo aquí es barato y puede esperar a tener un caso que lo valide.
