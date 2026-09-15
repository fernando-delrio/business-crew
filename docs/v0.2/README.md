# Business Crew v0.2 — índice ejecutivo

> **Índice de los 26 documentos de v0.2.** Diseño (2026-09-09) y ejecución de las fases
> 0 a 3 (2026-09-14).
>
> Lo que sigue describe el **diseño inicial**. Lo que realmente se ejecutó y midió está en
> [`phase1-report.md`](phase1-report.md), [`phase2-report.md`](phase2-report.md) y
> [`tier3-baseline.md`](tier3-baseline.md) — y en varios puntos **corrige** a este
> documento: la predicción de colisiones de §"Lo primero" falló a medias, y está
> documentado en [`evals-baseline.md`](evals-baseline.md) §5.

---

## El diagnóstico, en una cifra

| | Business Crew | `addyosmani/agent-skills` |
|---|--:|--:|
| Personas / agentes | **18** | 4 |
| Skills / procedimientos | **3** | 25 |
| Evals | **0** | 3 niveles, en CI |
| Workflows | **0** | ciclo de vida documentado |

**El ratio está invertido.** El repo tiene el *quién* casi completo y el *cómo* casi vacío.

Y la consecuencia es observable, no teórica: **`analista-datos` llevaba instalado desde el
06/09 mientras un proyecto consumidor tenía cero analítica en entregas repetidas.** El agente existía, era el
correcto, y nada lo invocó. **Un agente sin workflow que lo convoque es un documento, no
una capacidad.**

---

## Los cinco problemas

| # | Problema | Evidencia |
|---|---|---|
| **P1** | **No hay orquestación — y la que hay no puede ejecutarse** | `scrum-master` es un router persona, y **un subagente no puede lanzar otro subagente**. Su tabla de 17 filas es texto, no mecanismo |
| **P2** | **Ratio invertido:** 18 opiniones, 3 procedimientos | Un paquete sustancial de diseño y varios ADRs en un proyecto real sin que ninguna skill dijera cómo se escribe un ADR |
| **P3** | **Cero salidas verificables** | La palabra "gate" **no aparece en ningún archivo del repo** |
| **P4** | **Cero evaluación** | 8 de 18 descripciones dicen *"Sirve para cualquier tipo de producto"*. Nadie ha medido si colisionan |
| **P5** | **El aprendizaje no se acumula** | **2 commits en todo el repo, ambos con el mismo mensaje** |

---

## La propuesta, en una frase

> **Cero agentes nuevos. Cero agentes borrados. Se construyen las capas que faltan.**

| | Ahora | Propuesto |
|---|--:|--:|
| Agentes | 18 | **18** |
| Skills | 3 | **6** |
| Comandos | 4 | **7** |
| Rules | 0 | **3** |
| Evals | 0 | **Tier 1+2** |

**~14 archivos nuevos, repartidos en cuatro fases con disparador propio.**

---

## Lo primero — y son 90 minutos

Ejecutar el **Tier 2 de evals** sobre las 21 descripciones actuales. Determinista, gratis,
y es el único paso que **produce datos en lugar de consumir criterio**.

> **Predicción comprobable:** encontrará colisión alta entre `director-arte` ↔
> `design-direction` y entre `scrum-master` ↔ `/crew`. Si la encuentra, confirma todo este
> diagnóstico con datos. **Si no la encuentra, hay que revisar el diagnóstico.**

Todo lo demás espera al cierre del ciclo comercial abierto: rediseñar el sistema operativo
mientras hay descubrimiento pendiente es exactamente el rabbit hole nº 1 de ese ciclo.

---

## Los documentos

### Estado y capacidades

| Documento | Qué contesta |
|---|---|
| [`current-state-audit.md`](current-state-audit.md) | Qué hay de verdad. 41 archivos, verificados uno a uno |
| [`capability-map.md`](capability-map.md) | **5 capacidades completas de 56.** El mapa por capacidad, no por persona |
| [`agent-audit.md`](agent-audit.md) | Ficha de los 18 + **MINIMUM NECESSARY CREW** (techo de 3) |

### El sistema

| Documento | Qué contesta |
|---|---|
| [`orchestrator-contract.md`](orchestrator-contract.md) | FACT / INFERENCE / RECOMMENDATION / UNKNOWN, y el formato de ejecución |
| [`workflow-design.md`](workflow-design.md) | **De 8 workflows propuestos a 3**, con el motivo de cada recorte |
| [`quality-gates.md`](quality-gates.md) | Los 8 gates, todos con evidencia comprobable |
| [`model-routing.md`](model-routing.md) | El enrutado que **ya existe** en el frontmatter, y la política que le faltaba |
| [`human-authority.md`](human-authority.md) | Qué exige autoridad humana. **La barrera de git no se toca** |

### Los dos huecos

| Documento | Qué contesta |
|---|---|
| [`automation-capability.md`](automation-capability.md) | El hueco confirmado → **una skill, no un agente** |
| [`data-capability.md`](data-capability.md) | **Corrige a la auditoría anterior**: `saas-toolkit` ya cubre esquema y aislamiento. El hueco real es el ciclo de vida |

### Aprender

| Documento | Qué contesta |
|---|---|
| [`intelligence-lifecycle.md`](intelligence-lifecycle.md) | De evidencia a patrón a skill, con **cuatro filtros** |
| [`skill-promotion.md`](skill-promotion.md) | El pre-flight. **De 5 candidatas de ejemplo, 3 rechazadas** |
| [`evaluation-strategy.md`](evaluation-strategy.md) | Tres niveles, 6 fixtures anonimizados |

### Medición — Tier 2 (enrutado)

| Documento | Qué contesta |
|---|---|
| [`evals-baseline.md`](evals-baseline.md) | **Fase 0.** El baseline antes de tocar nada. 25 unidades, 300 pares, 0 colisiones, **50 % de capacidades inalcanzables** |
| [`routing-analysis.md`](routing-analysis.md) | Cobertura del enrutado y *CAPABILITY EXISTS / NO RELIABLE ROUTE* |
| [`phase1-report.md`](phase1-report.md) | **Fase 1.** 18 descripciones, contratos de salida, `Verification`, las dos fuentes de verdad. UNREACHABLE 50 % → 8 % |
| [`phase2-report.md`](phase2-report.md) | **Fase 2.** Generalización. Holdout 38 % → 75 %, tercer fixture externo, `DOMAIN FIRST / PROCEDURE SECOND` |

### Medición — Tier 3 (comportamiento)

| Documento | Qué contesta |
|---|---|
| [`tier3-design.md`](tier3-design.md) | El diseño previo: qué evaluar y cómo evitar el auto-calificado ingenuo |
| [`tier3-implementation.md`](tier3-implementation.md) | **Fase 3.** El examen construido: 12 fixtures, 6 dimensiones, severidad P0-P3 |
| [`tier3-baseline.md`](tier3-baseline.md) | 🔴 **NOT EXECUTED**, con el bloqueador verificado: los agentes instalados no son los de este repositorio |

### Futuro, diseñado y sin implementar

| Documento | Qué contesta |
|---|---|
| [`usage-telemetry-design.md`](usage-telemetry-design.md) | Cómo saber qué capacidades se usan de verdad, sin PII y sin plataforma |

### Estructura


| Documento | Qué contesta |
|---|---|
| [`repository-target.md`](repository-target.md) | **Se rechazan 3 de las carpetas propuestas**, con argumento |
| [`project-boundaries.md`](project-boundaries.md) | Qué cruza y qué no entre el core y el proyecto. **El repo es público y MIT** |
| [`agent-skills-study.md`](agent-skills-study.md) | 28 patrones: **14 adoptar · 10 adaptar · 4 rechazar** |
| [`implementation-plan.md`](implementation-plan.md) | Cuatro fases, la matriz de decisión y las **9 decisiones humanas** |

---

## Lo que se rechaza, y por qué

| Rechazado | Motivo |
|---|---|
| Agentes nuevos para los dos huecos | Lo que falta es **procedimiento**, no criterio. Un agente 19 duplicaría a `coo-graham`, `dev-dhh` y `devops-hightower` |
| `workflows/` como directorio | Un workflow **es** un comando. Dos sitios para lo mismo se desincronizan |
| `playbooks/` | Cero contenido y cero casos observados |
| `templates/` ahora | Un archivo no justifica un directorio. La plantilla de ADR vive dentro de su skill |
| 5 de los 8 workflows | BUILD ya existe fuera · VALIDATE es la misma conversación que DISCOVER · LEARN es `/ship` + promoción · OPERATE y CLIENT DELIVERY: **cero casos** |
| Importar skills de `agent-skills` | Triplicaría el solape con `superpowers` y `saas-toolkit` |
| Soporte multi-harness | Un harness |
| Tocar el `deny` de git | Se probó el 09/09 y funcionó como debía |

---

## Las decisiones que necesitan autoridad humana

Nueve, en [`implementation-plan.md`](implementation-plan.md) §6. Las tres que bloquean:

1. 🔴 **¿Se hace la Fase 0 de 90 minutos, o se espera al cierre del ciclo sin excepción?**
2. 🔴 **¿18 agentes, 0 nuevos?** — contradice la expectativa de cubrir huecos con agentes.
3. 🟠 **¿Se saca la tabla de derivación de `scrum-master`?** — le quita su función más visible.

---

## Cómo se sabrá si esto funcionó

| Señal | Hoy | Objetivo |
|---|---|---|
| Rank-1 de enrutado | **desconocido** | ≥90 % |
| Colisiones ≥75 % | **desconocido** | 0 |
| Capacidades por decisión | **sin techo** | ≤3 |
| Patrones ascendidos desde un caso real | 0 | ≥2 |

**Y la señal de fracaso:** si en dos ciclos la persona operadora sigue invocando agentes sueltos y
ningún workflow, v0.2 habrá añadido estructura que nadie usa. Entonces se retiran los
workflows y se deja el sistema como estaba — que ya era razonable.
