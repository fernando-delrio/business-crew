# Mapa de capacidades

> **2026-09-09.** Organizado por **capacidad**, no por nombre de agente — que es
> justamente lo que el encargo pide y lo que el repo no hace hoy.

---

## 1. Cómo leer esto

Cada capacidad se clasifica por **cobertura real**, no por si existe alguien que podría
opinar:

| Nivel | Significa |
|---|---|
| 🟢 **CUBIERTA** | Hay criterio **y** procedimiento **y** un artefacto de salida |
| 🟡 **PARCIAL** | Hay criterio (una persona opina) pero no procedimiento ni artefacto |
| 🔴 **AUSENTE** | Nadie la cubre |
| ⚪ **FUERA** | No nos toca — o la cubre algo ya instalado fuera de este repo |

**Casi todo el sistema está en amarillo, y eso es el hallazgo.** Tener a alguien que
opina no es tener la capacidad.

---

## 2. El mapa

### STRATEGY

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| Business discovery | 🟡 | `pm-producto` · `analista-thompson` | **No hay procedimiento de entrevista.** Hay conversaciones de descubrimiento pendientes y ninguna guía repetible |
| Positioning | 🟡 | `cmo-godin` | Sin artefacto |
| Competitive research | 🟡 | `analista-thompson` | Sin procedimiento de búsqueda ni de verificación de fuentes |
| Offer design | 🔴 | — | Nadie. En un proyecto consumidor, la línea de automatizaciones se diseñó sin capacidad que la sostuviera |
| Pricing | 🟢 | `cfo-precios` | Es de las pocas con método explícito (valor → eje → tres planes → unit economics) |
| Validation | 🟡 | `munger-critico` (pre-mortem) + `shape-up-cycle` | **No hay bucle hipótesis → experimento → decisión** |

### PRODUCT

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| Requirements | 🟡 | `pm-producto` | El formato de PRD está descrito, no plantillado |
| User journeys | 🔴 | — | `ux-norman` diagnostica un flujo existente; nadie diseña uno nuevo |
| Prioritization | 🟢 | `shape-up-cycle` + `/bet` + `decision-framing` | La capacidad mejor cubierta del repo |
| Acceptance criteria | 🔴 | — | Nadie define cuándo algo está terminado |

### DESIGN

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| UX | 🟡 | `ux-norman` | Sin artefacto |
| UI | 🟡 | `ui-duarte` | Sin artefacto |
| Visual direction | 🟢 | `design-direction` + `director-arte` | Cubierta, con duplicación entre los dos |
| Accessibility | ⚪ | Skill `accessibility` instalada fuera | No duplicar |
| Conversion | 🟡 | `cmo-godin` + `analista-datos` | Repartida entre dos, sin dueño |

### ENGINEERING

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| Architecture | 🟡 | `dev-dhh` | **Sin ADR.** Un proyecto consumidor produjo varios ADRs sin que este repo dijera cómo se escribe uno |
| Frontend | ⚪ | `conventions-reviewer`, skills de diseño | Fuera |
| Backend | ⚪ | `backend-reviewer` | Fuera |
| APIs | 🔴 | — | Nadie. `api-and-interface-design` existe en `agent-skills`, no aquí |
| Testing | 🟡 | `qa-bach` (exploratorio) · `test-writer` fuera | `qa-bach` piensa qué probar; nada lo ejecuta |
| Performance | ⚪ | Skill `performance` fuera | Fuera |

### AUTOMATION 🔴 **El hueco confirmado**

| Capacidad | Cobertura | Quién / qué |
|---|:--:|---|
| Workflow discovery | 🟡 | `coo-graham` decide **si**, no **cómo** |
| Arquitectura n8n | 🔴 | Nadie |
| Integraciones / adaptadores | 🔴 | Nadie |
| Idempotencia | 🔴 | Nadie |
| Reintentos / dead-letter | 🔴 | Nadie |
| Human handoff | 🔴 | Nadie |
| Observabilidad de flujos | 🔴 | Nadie |

Lo más cercano es `devops-hightower`, que cubre **infraestructura**, no flujos de negocio.
Ver [`automation-capability.md`](automation-capability.md).

### DATA 🟡 **El hueco es menor de lo que decía la auditoría anterior**

| Capacidad | Cobertura | Quién / qué |
|---|:--:|---|
| Modelado de entidades | 🟡 | `dev-dhh` de refilón |
| Persistencia / esquema | ⚪ | **`schema-reviewer`** (saas-toolkit) — antipatrones de Karwin |
| Aislamiento multi-tenant | ⚪ | **`saas-multitenant-architecture`** (saas-toolkit) — estrategias + checklist IDOR |
| Migraciones | 🔴 | Nadie |
| **Ownership del dato** | 🔴 | **Nadie** |
| **Retención / borrado / exportación** | 🔴 | **Nadie** |
| **Clasificación de PII** | 🔴 | Repartida entre `seguridad` y `legal-basico`, sin dueño |
| **Qué va en un audit trail** | 🔴 | **Nadie** |
| Analytics | 🟡 | `analista-datos` |
| Reporting | 🔴 | Nadie |

**Corrección a la auditoría anterior:** dijo *"no hay ningún rol de datos/persistencia"*.
Verificado: **sí lo hay, instalado, en `saas-toolkit`**. El hueco real es el **ciclo de
vida del dato**, que es otra cosa. Ver [`data-capability.md`](data-capability.md).

### SECURITY

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| Threat modelling | 🔴 | — | `seguridad` revisa lo construido; nadie modela amenazas antes |
| Secretos | 🟡 | `seguridad` | Sin checklist ejecutable |
| Auth / authz | 🟡 | `seguridad` + `backend-reviewer` fuera | — |
| Privacy | 🟡 | `seguridad` + `legal-basico` | Se pisan justo donde más duele |
| Data minimization | 🔴 | — | Nadie |

### LEGAL / RISK

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| Claims (qué se puede prometer) | 🔴 | — | Nadie. Y ya ha ocurrido: ayudas públicas ya cerradas, ofrecidas como disponibles |
| Contratos | 🟡 | `legal-basico` | — |
| Preguntas de RGPD | 🟡 | `legal-basico` | — |
| **Disparador de revisión profesional** | 🟢 | `legal-basico` §"Señales de alarma" | Bien resuelto |

### GROWTH

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| SEO | ⚪ | Skill `seo` fuera | — |
| Analytics | 🟡 | `analista-datos` | **Existe y no se usó**: un proyecto consumidor con cero analítica durante entregas sucesivas |
| Contenido | 🟡 | `cmo-godin` | — |
| Embudos | 🟡 | `analista-datos` | — |
| Outreach | 🟡 | `ventas-ross` | Sin guion reutilizable |

### OPERATIONS

| Capacidad | Cobertura | Quién / qué | Hueco |
|---|:--:|---|---|
| Delivery | 🔴 | — | Nadie |
| QA | 🟡 | `qa-bach` | — |
| Incident response | 🟡 | `devops-hightower` | Sin runbook |
| Client handoff | 🔴 | — | Nadie |
| Mantenimiento | 🔴 | — | **Se cobra una cuota mensual recurrente y nadie define qué incluye** |

### LEARNING 🔴

| Capacidad | Cobertura | Quién / qué |
|---|:--:|---|
| Retrospectivas | 🟢 | `/ship` |
| Extracción de patrones | 🔴 | Nadie |
| Promoción a skill | 🔴 | Nadie |
| Historial de decisiones | 🔴 | Nadie — 2 commits en todo el repo |

---

## 3. Recuento

| Nivel | Capacidades |
|---|--:|
| 🟢 CUBIERTA | **5** |
| 🟡 PARCIAL | **23** |
| 🔴 AUSENTE | **22** |
| ⚪ FUERA | 6 |

**Cinco capacidades completas de 56.** Y las cinco son las que ya tienen procedimiento
escrito: el ciclo de Shape Up, la priorización, el pricing, la dirección visual y el
disparador legal.

Eso confirma el diagnóstico: **lo que convierte una opinión en capacidad es el
procedimiento, no la persona.**

---

## 4. Qué se propone construir, y qué no

Aplicando el anti-bloat gate a las 22 ausentes. La pregunta de corte es
**"¿hay un problema observado, hoy, en un proyecto real?"**

### Se construye ahora — 3 capacidades

| Capacidad | Problema observado | Forma |
|---|---|---|
| **Discovery / entrevista** | Ciclo de descubrimiento abierto y sin guion repetible | SKILL |
| **Arquitectura de automatización** | La fase que viene entera. Un paquete de diseño sustancial sin capacidad que lo sostenga | SKILL |
| **Ciclo de vida del dato** | Un negocio con requisitos documentales sensibles: documentos sin ownership ni retención definidos | SKILL (delgada) |

### Se construye ahora como capa, no como capacidad — 4 piezas

Orquestación · gates · contrato de evidencia · evals. No son capacidades de dominio: son
lo que hace que las capacidades existentes se puedan invocar y verificar.

### Se aplaza — 15 capacidades

Offer design · user journeys · acceptance criteria · APIs · migraciones · reporting ·
threat modelling · data minimization · claims · delivery · client handoff · mantenimiento
· incident runbook · extracción de patrones · historial de decisiones.

**Motivo común: cero casos observados.** No hay clientes, no hay incidentes, no hay
entregas. Construir la capacidad de *client handoff* sin un cliente es exactamente el
error que `coo-graham` está ahí para señalar.

Las tres primeras que volverán a la mesa —y su disparador escrito ahora:

| Capacidad | Se construye cuando |
|---|---|
| **Mantenimiento** | El primer cliente pague la primera cuota mensual |
| **Client handoff** | Se entregue la primera web |
| **Incident runbook** | Ocurra el primer incidente real |
