# Plan de implementación v0.2

> **2026-09-09.** Nada de esto se ejecuta sin aprobación.
> **Restricción que manda sobre todo lo demás:** hay un ciclo comercial activo con 0 de 10
> conversaciones.

---

## 1. La restricción, antes del plan

Este plan se escribe mientras el proyecto que lo usa tiene un ciclo abierto cuya meta
es **hablar con clientes potenciales**, y cuyo primer rabbit hole declarado es:

> *"Refugiarse en construir. La excusa técnica siempre es legítima y siempre está a mano."*

**Rediseñar Business Crew es una excusa técnica legítima.** Es trabajo cómodo que desplaza
al incómodo, que es llamar a alguien.

> **Por eso la Fase 0 de este plan es: no hacer nada hasta que cierre el ciclo activo, con
> una excepción de 90 minutos.**

Y hay un argumento que no es solo de disciplina: **`/discover` se escribe mejor después de
tres conversaciones reales que antes de ninguna.** Escribirlo ahora sería documentar la
entrevista que imaginamos.

---

## 2. Las fases

### FASE 0 — Hasta que cierre el ciclo activo · **90 minutos en total**

Solo lo que es gratis, determinista y no depende de ninguna conversación.

| # | Tarea | Coste | Por qué ahora |
|---|---|---|---|
| 0.1 | **Ejecutar el Tier 2 de evals sobre las 21 descripciones actuales** | 60 min | Determinista, gratis, y **da el dato que falta**: si las descripciones colisionan. Sin él, todo lo demás es teoría |
| 0.2 | Arreglar las descripciones que el Tier 2 señale | 30 min | Es arreglar un defecto, no construir |

**Y nada más.** Ni skills, ni workflows, ni reorganizar carpetas.

> **La predicción, para poder comprobarla:** el Tier 2 encontrará colisión alta entre
> `director-arte` ↔ `design-direction` y entre `scrum-master` ↔ `/crew`. Si la encuentra,
> confirma el diagnóstico de todo este paquete con datos. **Si no la encuentra, hay que
> revisar el diagnóstico.**

### FASE 1 — Cierre del ciclo · en el cool-down

Cerrar lo que ya existe antes de añadir nada.

| # | Tarea | Entrega |
|---|---|---|
| 1.1 | Añadir **`Verification`** a las 3 skills | Las 3 declaran cuándo terminan |
| 1.2 | Añadir **output verificable** a los 18 agentes | Una línea por archivo |
| 1.3 | Quitar de `director-arte` lo que duplica a `design-direction` | 83 → ~45 líneas |
| 1.4 | Mover la tabla de derivación de `scrum-master` a `rules/orchestration.md` | El enrutado pasa a ser ejecutable |
| 1.5 | Escribir `rules/orchestration.md` | Contrato de evidencia + mapa de intención + minimum crew |
| 1.6 | Crear `evals/` con los casos de 0.1 | El Tier 2 queda reproducible |

**Coste: un cool-down.** Cero archivos nuevos salvo dos reglas y los evals. **Cero agentes,
cero skills nuevas.**

> **Esta fase, sola, arregla los cinco problemas de la auditoría** salvo los dos huecos de
> capacidad. Es la de mejor retorno de todo el plan.

### FASE 2 — Con el primer caso real

Cada entrada tiene su disparador. **Ninguna se hace "porque toca".**

| # | Tarea | Disparador |
|---|---|---|
| 2.1 | Skill `discovery-interview` | **Después de 3 conversaciones reales**, no antes |
| 2.2 | Comando `/discover` | Junto a 2.1 |
| 2.3 | `intelligence/patterns.md` con los 3 patrones atrapados en el repositorio del proyecto | Con la Fase 1, es barato |
| 2.4 | `rules/human-authority.md` y `rules/model-routing.md` | Con la Fase 1 |

### FASE 3 — Cuando haya cliente

| # | Tarea | Disparador |
|---|---|---|
| 3.1 | Skill `automation-architecture` | Primera automatización real **decidida** |
| 3.2 | Skill `data-lifecycle` | Antes de la primera migración con datos de terceros |
| 3.3 | Comando `/design` | Primera propuesta a un cliente |
| 3.4 | Comando `/release` | Primer despliegue con cliente detrás |
| 3.5 | Plantilla de ADR en `skills/decision-framing/` | Con 3.3 |

### FASE 4 — Cuando haya rodaje

| # | Tarea | Disparador |
|---|---|---|
| 4.1 | Evals Tier 3 para las skills nuevas | Duda real de si se siguen o se ignoran |
| 4.2 | Revisar `ceo-bezos` y `analista-thompson` | 2 ciclos con registro de uso |
| 4.3 | Reconsiderar OPERATE y CLIENT DELIVERY | Primer incidente · primera entrega |
| 4.4 | `templates/` | Cuando haya 3 plantillas compartidas |

---

## 3. Qué NO se hace

| No | Por qué |
|---|---|
| Crear agentes nuevos | Los dos huecos son procedimiento, no criterio |
| Borrar agentes | Cero datos de uso. Se decide en 4.2 |
| Crear `workflows/` | Un workflow es un comando |
| Crear `playbooks/` | Cero contenido |
| Crear `templates/` ahora | Un archivo no justifica un directorio |
| Importar skills de `agent-skills` | Triplicaría el solape con `superpowers` y `saas-toolkit` |
| Soporte multi-harness | Un harness |
| Tier 3 de evals ahora | Cuesta tokens sin pregunta que responder |
| Tocar el `deny` de git | Ver `human-authority.md` §1 |
| Escribir skills antes de su primer caso | Documentaría lo que imaginamos |

---

## 4. Orden y dependencias

```
FASE 0 (90 min, ahora)
  0.1 evals Tier 2  ──►  0.2 arreglar descripciones
        │
        │  ← el dato que valida o refuta el diagnóstico
        ▼
FASE 1 (cool-down)
  1.1 Verification ──┐
  1.2 outputs      ──┤
  1.3 director-arte──┼──►  1.5 rules/orchestration.md  ──►  1.6 evals/
  1.4 scrum-master ──┘
        ▼
FASE 2 (tras 3 conversaciones)
  2.1 skill discovery ──► 2.2 /discover
  2.3 patterns · 2.4 rules
        ▼
FASE 3 (con cliente)        FASE 4 (con rodaje)
```

**Dependencia dura: 0.1 antes que todo.** Es el único paso que produce datos en lugar de
consumir criterio.

---

## 5. Matriz de decisión

| Item | Actual | Propuesto | Acción | Valor | Coste | Riesgo | ¿Autoridad humana? |
|---|---|---|---|:--:|:--:|:--:|:--:|
| **Agentes** | 18 | **18** | Mantener | — | — | — | — |
| ↳ con output verificable | 0 | **18** | Añadir 1 línea × 18 | 🟢 Alto | Bajo | Bajo | No |
| ↳ `director-arte` | duplica skill | limpio | Quitar duplicación | 🟢 Alto | Bajo | Bajo | No |
| ↳ `scrum-master` | router roto | guardián del ciclo | Mover tabla a `rules/` | 🟢 Alto | Bajo | Medio | **Sí** |
| ↳ `ceo-bezos` | activo | candidato | Medir 2 ciclos | 🟡 Medio | Bajo | Bajo | **Sí** |
| ↳ `analista-thompson` | activo | candidato | Medir 2 ciclos | 🟡 Medio | Bajo | Bajo | **Sí** |
| ↳ agentes nuevos | — | **0** | Ninguno | — | — | — | — |
| ↳ agentes borrados | — | **0** | Ninguno | — | — | — | — |
| **Skills** | 3 | **3 → 6** | +3, por fases | 🟢 Alto | Medio | Bajo | **Sí** |
| ↳ las 3 actuales | sin Verification | con | Añadir sección | 🟢 Alto | Bajo | Bajo | No |
| ↳ `discovery-interview` | — | nueva | Fase 2 | 🟢 Alto | Medio | Bajo | **Sí** |
| ↳ `automation-architecture` | — | nueva | Fase 3 | 🟢 Alto | Medio | Medio | **Sí** |
| ↳ `data-lifecycle` | — | nueva, delgada | Fase 3 | 🟡 Medio | Bajo | Bajo | **Sí** |
| **Comandos / workflows** | 4 | **4 → 7** | +3, por fases | 🟢 Alto | Medio | Medio | **Sí** |
| ↳ `/discover` | — | nuevo | Fase 2 | 🟢 Alto | Medio | Bajo | **Sí** |
| ↳ `/design` | — | nuevo | Fase 3 | 🟢 Alto | Medio | Medio | **Sí** |
| ↳ `/release` | — | nuevo | Fase 3 | 🟢 Alto | Medio | Bajo | **Sí** |
| ↳ colisión `/ship` | sin resolver | documentada | Renombrar el nuevo | 🟡 Medio | Nulo | Bajo | **Sí** |
| ↳ OPERATE, LEARN, CLIENT DELIVERY, BUILD, VALIDATE | — | **no se crean** | Fusionar o aplazar | — | — | — | — |
| **Rules** | 0 | **3** | Crear | 🟢 Alto | Bajo | Bajo | **Sí** |
| **Templates** | 0 | **0** (1 dentro de skill) | Aplazar directorio | 🟡 Medio | Nulo | Bajo | No |
| **Evals** | 0 | **Tier 1 + 2** | Crear | 🟢 **Muy alto** | **Bajo** | Bajo | No |
| ↳ casos | 0 | **21** | Uno por capacidad | 🟢 Alto | Medio | Bajo | No |
| ↳ fixtures | 0 | **6** | Anonimizados | 🟢 Alto | Bajo | 🔴 **PII si se hace mal** | **Sí** |
| ↳ Tier 3 | 0 | bajo demanda | Fase 4 | 🟡 Medio | Alto | Bajo | **Sí** |
| **Intelligence** | 0 | **2 archivos** | Crear | 🟢 Alto | Bajo | 🔴 **PII si se hace mal** | **Sí** |
| **Docs** | 0 | 18 | ✅ Hecho | 🟢 Alto | — | — | — |
| **Directorios** | 6 | **10** | +4 | 🟡 Medio | Bajo | Bajo | **Sí** |
| **Hooks / scripts** | 2 / 2 | igual | Mantener | — | — | — | — |

### Recuento

| | Ahora | Propuesto |
|---|--:|--:|
| Agentes | 18 | **18** (0 nuevos, 0 borrados, 2 mejorados, 2 en observación) |
| Skills | 3 | **6** (3 mejoradas, 3 nuevas por fases) |
| Comandos | 4 | **7** |
| Rules | 0 | **3** |
| Templates | 0 | **0** (1 dentro de una skill) |
| Evals | 0 | **Tier 1+2 · 21 casos · 6 fixtures** |
| Archivos nuevos totales | — | **~14**, repartidos en cuatro fases |

---

## 6. Decisiones que necesitan autoridad humana

| # | Decisión | Impacto |
|---|---|---|
| 1 | 🔴 **¿Se acepta la Fase 0 de 90 minutos, o se espera al cierre del ciclo sin excepción?** Mi recomendación: hacerla — es el único paso que produce datos y no depende de ninguna conversación | Bloquea todo |
| 2 | 🔴 **¿18 agentes, 0 nuevos?** Contradice la expectativa de cubrir los huecos con agentes | Estructural |
| 3 | 🟠 **¿Mover la tabla de derivación fuera de `scrum-master`?** Le quita su función más visible | `scrum-master` |
| 4 | 🟠 **¿`/discover`, `/design`, `/release` en `commands/` en vez de `workflows/`?** | Estructura |
| 5 | 🟠 **¿Se renombra el nuevo a `/release` por la colisión con `/ship`?** | Nomenclatura |
| 6 | 🟠 **¿Se aceptan `ceo-bezos` y `analista-thompson` en observación con criterio de 2 ciclos?** | 2 agentes |
| 7 | 🟡 **¿Se acepta que el hueco de datos era menor de lo que dijo la auditoría anterior**, y que la skill sea delgada y enlace a `saas-toolkit`? | Alcance |
| 8 | 🟡 **¿Se añade `merge` al `deny` de git?** | Seguridad |
| 9 | 🟡 **¿Se revisan los modelos de `seguridad` y `legal-basico`** (sonnet → superior)? | Coste/calidad |

---

## 7. Cómo se sabrá si v0.2 funcionó

El sistema debe poder evaluarse a sí mismo. Cuatro señales, medibles en dos ciclos:

| Señal | Hoy | Objetivo |
|---|---|---|
| Rank-1 de enrutado (Tier 2) | **desconocido** | ≥90 %, subiendo |
| Pares de descripciones con colisión ≥75 % | **desconocido** | 0 |
| Capacidades convocadas por decisión | **sin techo** | ≤3 |
| Patrones ascendidos desde un caso real | **0** | ≥2 |

**Y una señal de fracaso, escrita ahora para poder reconocerla:** si dentro de dos ciclos
la persona operadora sigue invocando agentes sueltos y ningún workflow, v0.2 habrá añadido estructura
que nadie usa. En ese caso **se retiran los workflows y se deja el sistema como estaba**,
que ya era razonable.
