# Estado real de Business Crew

> **2026-09-09.** Inventario verificado archivo a archivo sobre el repositorio, no sobre
> las cifras de la auditoría anterior. Solo lectura: no se ha modificado ni borrado nada.

---

## 1. Inventario exacto

Repo: `fernando-delrio/business-crew` · rama `main` · **41 archivos versionados** ·
local sincronizado con `origin` (`6d95f9b`).

| Carpeta | Existe | Archivos | Líneas | Estado |
|---|:--:|--:|--:|---|
| `agents/` | ✅ | 18 | 1.493 | Contenido denso y de buena calidad |
| `skills/` | ✅ | 3 | 554 | Pocas para lo que el sistema promete |
| `commands/` | ✅ | 4 | 351 | `/bet` `/hill` `/ship` `/crew` |
| `hooks/` | ✅ | 1 | — | `SessionStart` + `Stop` |
| `scripts/` | ✅ | 2 | 131 | `cargar-ciclo.sh` · `recordar-cierre.sh` |
| `.claude-plugin/` | ✅ | 2 | — | `plugin.json` v2.0.0 + `marketplace.json` |
| `.github/` | ✅ | 3 | — | Plantillas de issue |
| **`workflows/`** | ❌ | — | — | **No existe** |
| **`rules/`** | ❌ | — | — | **No existe** |
| **`templates/`** | ❌ | — | — | Solo `PORTFOLIO.template.md` en la raíz |
| **`intelligence/`** | ❌ | — | — | **No existe** |
| **`evals/`** | ❌ | — | — | **No existe** |
| **`docs/`** | ❌ | — | — | **No existe** (este directorio lo crea esta fase) |
| **`playbooks/`** | ❌ | — | — | **No existe** |

Meta en la raíz: `README.md` (11 KB) · `CHANGELOG.md` · `CONTRIBUTING.md` · `SECURITY.md`
· `LICENSE` (MIT) · `PORTFOLIO.template.md` · `.gitattributes` · `.gitignore`.

**Las cifras de la auditoría anterior eran correctas.** 18 agentes, 4 comandos, 3 skills,
2 hooks. Confirmado, no heredado.

### Anomalías encontradas

| # | Qué | Gravedad |
|---|---|---|
| 1 | **Dos commits consecutivos con el mensaje idéntico** — `bc60ca6` y `6d95f9b`, ambos *"feat(business-crew): equipo de 18 agentes con ciclo Shape Up"*. Todo el repo entró en dos commits gemelos | 🟡 Historial sin granularidad: no se puede bisecar ni atribuir un cambio a una decisión |
| 2 | `.github/social-preview.png` sin versionar | 🟢 |
| 3 | El plugin `saas-claude-toolkit` está cacheado **dos veces** (`1.0.0` y `e1043df70418`) con skills duplicadas | 🟢 Fuera de este repo, pero afecta al enrutado |

---

## 2. El diagnóstico, en una cifra

| | Business Crew | `addyosmani/agent-skills` |
|---|--:|--:|
| **Personas / agentes** | **18** | **4** |
| **Skills / procedimientos** | **3** | **25** |
| Comandos | 4 | varios |
| Evals | **0** | 3 niveles, en CI |
| Workflows explícitos | **0** | Mapeo de ciclo de vida documentado |

**El ratio está invertido.** Business Crew tiene el *quién* casi completo y el *cómo* casi
vacío.

Y la consecuencia es observable, no teórica: **`analista-datos` lleva instalado desde el
06/09 y un proyecto consumidor estuvo con cero analítica en entregas repetidas.** El agente
existía, era exactamente el correcto, y nada lo invocó. Un agente sin workflow que lo
convoque es un documento, no una capacidad.

---

## 3. Elemento por elemento

### 3.1 Agentes (18)

Los 18 comparten una estructura sólida y consistente: frontmatter con `name`,
`description`, `model`; sección *"Contexto — siempre antes de responder"*; *"Ajuste por
tipo de producto"*; y —lo más valioso— **"Cuándo NO aportas" con derivación nominal**.

| Agente | Líneas | Modelo | Output | Clasificación |
|---|--:|---|---|---|
| `analista-datos` | 106 | sonnet | Métrica única + embudo + instrumentación | **KEEP** |
| `analista-thompson` | 76 | opus | Análisis de cadena de valor | **DEPRECATE-CANDIDATE** |
| `ceo-bezos` | 63 | opus | Una recomendación de prioridad | **DEPRECATE-CANDIDATE** |
| `cfo-precios` | 67 | sonnet | Precio + unit economics | **KEEP** |
| `cmo-godin` | 70 | sonnet | Posicionamiento anti-genérico | **KEEP** |
| `coo-graham` | 60 | sonnet | Automatizar vs a mano, con regla de volumen | **KEEP** |
| `dev-dhh` | 81 | opus | Opinión de arquitectura | **KEEP** |
| `devops-hightower` | 78 | sonnet | Diagnóstico infra vs código | **KEEP** |
| `director-arte` | 83 | opus | Brief visual | **IMPROVE** (duplica la skill) |
| `legal-basico` | 79 | sonnet | Riesgo + qué preguntar a un abogado | **KEEP** |
| `munger-critico` | 71 | opus | Pre-mortem 3-5 riesgos + mitigación | **KEEP** |
| `pm-producto` | 84 | sonnet | PRD de media pantalla | **KEEP** |
| `qa-bach` | 76 | sonnet | Charter de exploración | **KEEP** |
| `scrum-master` | 90 | sonnet | 2-3 pasos + **derivación** | **IMPROVE** (router roto) |
| `seguridad` | 90 | sonnet | Lista corta de hallazgos | **KEEP** |
| `ui-duarte` | 127 | opus | Sistema de tokens | **KEEP** |
| `ux-norman` | 115 | opus | Diagnóstico de usabilidad | **KEEP** |
| `ventas-ross` | 77 | sonnet | Proceso de venta repetible | **KEEP** |

**Ninguno declara un artefacto verificable.** Todos producen "una respuesta". Las 4
personas de `agent-skills` (`code-reviewer`, `security-auditor`, `test-engineer`,
`web-performance-auditor`) producen **informes con formato**, y por eso se pueden
componer en paralelo y sintetizar. Esa es la diferencia estructural.

### 3.2 Skills (3)

| Skill | Líneas | Propósito | Clasificación |
|---|--:|---|---|
| `shape-up-cycle` | 216 | Appetite, hill chart, circuit breaker, sin backlog | **KEEP** — es el activo más valioso del repo |
| `decision-framing` | 134 | Compare-and-contrast, reversibilidad | **KEEP** |
| `design-direction` | 204 | Brief de 5 decisiones, rúbrica Awwwards, enrutado | **KEEP** — y recuperar lo que `director-arte` le duplica |

Las tres son de calidad alta. **Ninguna tiene sección de verificación ni criterios de
salida**, que es lo que separa una skill de un buen documento.

### 3.3 Comandos (4)

| Comando | Qué hace | Lee | Clasificación |
|---|---|---|---|
| `/bet` | Abre ciclo: apuesta, appetite, no-go | `shape-up-cycle`, `.crew/estado.md` | **KEEP** |
| `/hill` | Actualiza el hill chart, detecta atascos | idem | **KEEP** |
| `/ship` | Cierra ciclo: verificación, retro, cool-down | idem | **KEEP** ⚠️ ver colisión |
| `/crew` | Convoca al equipo y sintetiza posturas | `~/.claude/PORTFOLIO.md` | **IMPROVE** |

⚠️ **Colisión de nombre detectada.** `/ship` aquí significa *cerrar el ciclo de Shape Up*.
En el resto del ecosistema —y en el diseño de workflows que se pedía— "ship" significa
*publicar a producción*. Son dos cosas distintas y el nombre está ocupado. Cualquier
workflow de publicación debe llamarse de otra forma.

### 3.4 Hooks y scripts

| Pieza | Evento | Qué hace | Clasificación |
|---|---|---|---|
| `cargar-ciclo.sh` | `SessionStart` | Lee `.crew/estado.md`, recuerda apuesta y día, avisa si la colina lleva días quieta | **KEEP** — funciona, se ha visto en esta sesión |
| `recordar-cierre.sh` | `Stop` | Verifica coherencia del incremento | **KEEP** |

Son la única parte del sistema que **actúa sola**. Todo lo demás espera a ser invocado.

---

## 4. Los cinco problemas reales

### P1 · No hay orquestación — y el que hay, no puede ejecutarse

`scrum-master` lleva una tabla de derivación de 17 filas (*"si el siguiente paso es X →
deriva a Y"*). Es un **router persona**.

Dos problemas, y el segundo es duro:

1. `agent-skills` rechaza el patrón explícitamente: *"Do not build a 'router' persona that
   decides which other persona to call; that's the job of slash commands and intent
   mapping."*
2. **Restricción de plataforma: un subagente no puede lanzar otro subagente.** Así que
   `scrum-master`, invocado como agente, **no puede convocar a nadie**. Solo puede
   escribir el nombre de quien habría que llamar, para que lo llame a mano la persona
   operadora.

El enrutado existe como texto y no como mecanismo.

### P2 · El ratio invertido — 18 opiniones, 3 procedimientos

Un agente da criterio. Una skill da un resultado repetible con criterios de salida. Hoy
el sistema sabe **opinar** sobre casi todo y **hacer** casi nada de forma repetible.

Consecuencia medible: una fase de arquitectura real produjo un paquete sustancial de
diseño y varios ADRs sin
que ninguna skill de Business Crew definiera cómo se escribe un ADR, qué gates pasa un
diseño, ni cuándo un diseño está terminado.

### P3 · Cero salidas verificables

Ni un agente, ni una skill, ni un comando declara *"esto está terminado cuando…"*. La
palabra "gate" no aparece en ningún archivo del repositorio. La auditoría anterior listó
"gates" como fortaleza; **verificado: no existen como artefacto**.

### P4 · Cero evaluación

18 descripciones que empiezan casi todas por *"Úsalo para…"* y comparten vocabulario
(*"Sirve para cualquier tipo de producto"* aparece en 8). Nadie ha medido si colisionan.

Es exactamente el fallo que el Tier 2 de `agent-skills` detecta de forma **determinista y
gratuita**: si dos descripciones se parecen por encima del 75 %, el enrutado es una
moneda al aire.

### P5 · El aprendizaje no se acumula

`/ship` hace retro. La retro se queda en `.crew/`, que es **por proyecto y está fuera de
git**. Nada asciende una lección a patrón, ni un patrón a skill. El repositorio no ha
aprendido nada desde el commit inicial: **2 commits, ambos con el mismo mensaje**.

---

## 5. Duplicaciones verificadas

| # | Qué | Evidencia | Acción |
|---|---|---|---|
| 1 | `director-arte` ↔ `design-direction` | El agente dice *"Trabaja con la skill […] ahí está la rúbrica, el brief de cinco decisiones y la tabla de enrutado"* y a continuación **reproduce las tres** en sus 83 líneas | **MERGE**: el *cómo* a la skill, el *quién* al agente |
| 2 | `scrum-master` ↔ `/crew` | `commands/crew.md` abre con *"Eres el Scrum Master convocando al equipo"* | **MERGE** hacia el comando: el orquestador es el comando, no la persona |
| 3 | `scrum-master` ↔ `/bet` `/hill` `/ship` | Los cuatro leen `shape-up-cycle` y `.crew/estado.md` | **KEEP** — reparto legítimo por momento del ciclo |
| 4 | `coo-graham` ↔ `dev-dhh` | Ambos opinan sobre automatizar. Frontera declarada por fase | **KEEP** |
| 5 | Hueco de datos ↔ `saas-toolkit` | `saas-multitenant-architecture` ya cubre aislamiento e IDOR; `schema-reviewer` cubre antipatrones de esquema | **La auditoría anterior sobreestimó este hueco.** Ver `data-capability.md` |

---

## 6. Clasificación resumida

| Estado | Cuántos | Cuáles |
|---|--:|---|
| **KEEP** | 14 agentes · 3 skills · 3 comandos · 2 hooks · 2 scripts | La mayoría del repo es buen material |
| **IMPROVE** | 2 agentes (`director-arte`, `scrum-master`) · 1 comando (`/crew`) · las 3 skills (añadir verificación) | — |
| **MERGE** | 2 duplicaciones (§5.1, §5.2) | — |
| **DEPRECATE-CANDIDATE** | 2 agentes (`ceo-bezos`, `analista-thompson`) | Con criterio medible, no por opinión — ver `agent-audit.md` §4 |
| **DELETE** | **0** | No se propone borrar nada |
| **MISSING** | orquestación · gates · artefactos · evals · ciclo de aprendizaje · capacidad de automatización · capacidad de ciclo de vida del dato | Ver `capability-map.md` |

**Nada se borra en esta fase.** El repositorio no tiene un problema de exceso: tiene un
problema de capas que faltan.
