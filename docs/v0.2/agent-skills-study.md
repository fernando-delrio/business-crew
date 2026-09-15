# Estudio de `addyosmani/agent-skills`

> **2026-09-09.** Acceso conseguido vía API de GitHub (commit `6ca0cd7`).
> Se extraen **principios**, no archivos. No se copia, no se vendoriza, no se importa nada.

---

## 1. Qué es, y en qué se diferencia

| | `agent-skills` | `business-crew` |
|---|---|---|
| Dominio | Ingeniería de software | Negocio + producto + ingeniería |
| **Skills** | **25** | **3** |
| **Personas / agentes** | **4** | **18** |
| Comandos | varios, multi-harness | 4 |
| Evals | **3 niveles, en CI** | **0** |
| Docs | 16 archivos, incl. `skill-anatomy.md` | 0 |
| Público objetivo | Comunidad, muchos colaboradores | Un operador solo |
| Harnesses | Claude, Codex, Gemini, OpenCode, Cursor… | Claude Code |

**El dato que más informa: el ratio está invertido.** 25/4 frente a 3/18.

Y no es casualidad: `agent-skills` optimiza para que **el trabajo se haga igual cada vez**;
Business Crew optimiza para que **alguien te dé una opinión que no tenías**. Los dos son
legítimos. El problema es que Business Crew se quedó solo con el segundo.

---

## 2. La diferencia de contexto — antes de copiar nada

| Ellos | Nosotros |
|---|---|
| Decenas de colaboradores | Una persona |
| Muchos harnesses | Uno |
| Dominio acotado (código) | Dominio ancho (negocio → código) |
| Comunidad que vota con PRs | Nadie que vote |
| Sus skills se instalan sueltas | Nuestro plugin se instala entero |

**Consecuencia directa:** todo lo que resuelve *coordinación entre colaboradores* o
*portabilidad entre harnesses* no nos aplica. Todo lo que resuelve *que una capacidad se
dispare cuando debe* nos aplica más que a ellos, porque nosotros no tenemos a nadie que lo
note cuando falla.

---

## 3. La tabla

| # | Patrón | Fuente | Valor aquí | Decisión | Por qué |
|--:|---|---|:--:|---|---|
| 1 | **Tres capas: skill = cómo · persona = quién · comando = cuándo** | `AGENTS.md` | 🟢 Alto | **ADOPTAR** | Nombra exactamente nuestro problema: 18 "quién" y casi ningún "cómo" |
| 2 | **Las personas no invocan personas. El comando orquesta** | `AGENTS.md` | 🟢 Alto | **ADOPTAR** | `scrum-master` es un router persona, y además **no puede ejecutarse**: un subagente no lanza otro subagente |
| 3 | **Fan-out paralelo + merge, único patrón multi-persona** | `AGENTS.md` (`/ship`) | 🟢 Alto | **ADOPTAR** | Da forma a `/release` y pone techo a `/crew` |
| 4 | **Anatomía de skill** (Overview · When to Use · Process · Rationalizations · Red Flags · **Verification**) | `docs/skill-anatomy.md` | 🟢 Alto | **ADOPTAR** | Nuestras 3 skills no declaran cuándo terminan. Es el hueco de "cero salidas verificables" |
| 5 | **Tabla de racionalizaciones** | idem | 🟢 Alto | **ADOPTAR** | Lo más distintivo del formato. Encaja con nuestros no-go y rabbit holes |
| 6 | **Evals Tier 1 — estructural** | `evals/README.md` | 🟢 Alto | **ADOPTAR** | Gratis y determinista |
| 7 | **Evals Tier 2 — enrutado y colisión de descripciones** | idem | 🟢 **Muy alto** | **ADOPTAR** | 8 descripciones dicen *"Sirve para cualquier tipo de producto"*. Gratis, determinista, detecta nuestro fallo dominante |
| 8 | **Negativos con `owner`** | idem | 🟢 Alto | **ADOPTAR** | Convierte un negativo vacuo en un test de enrutado real |
| 9 | **"Arregla la descripción, no el prompt"** | idem | 🟢 Alto | **ADOPTAR** | Impide hacerse trampas |
| 10 | **Nunca bajar el umbral para que pase una regresión** | idem | 🟢 Alto | **ADOPTAR** | Disciplina, coste cero |
| 11 | **Mapa intención → capacidad** | `AGENTS.md` | 🟢 Alto | **ADOPTAR** | Sustituye la tabla de `scrum-master`, que no puede ejecutarse |
| 12 | **Pre-flight antes de proponer una skill** | `CONTRIBUTING.md` | 🟢 Alto | **ADAPTAR** | Su versión busca PRs abiertos; la nuestra busca skills instaladas fuera (`saas-toolkit`) |
| 13 | **Divulgación progresiva · ≤500 líneas** | `skill-anatomy.md` | 🟡 Medio | **ADAPTAR** | Nuestro tope: **300** para skills nuevas. Somos más pequeños |
| 14 | **`references/` en la raíz para lo compartido** | idem | 🟡 Medio | **ADAPTAR** | Ellos tienen 25 skills compartiendo checklists. Con 3-5, lo compartido son los **gates**, y viven en `docs/` + `rules/` |
| 15 | **`scripts/` solo si hay algo ejecutable** | idem | 🟢 Alto | **ADOPTAR** | *"No crees un `scripts/` vacío para imitar a otras skills"* |
| 16 | **Prefiere ejecutar un script a incrustar código** | idem | 🟡 Medio | **ADAPTAR** | Cierto para contexto. Nuestro dominio es más de criterio que de ejecución |
| 17 | **Referenciar otras skills, nunca duplicarlas** | idem | 🟢 Alto | **ADOPTAR** | Es literalmente el bug `director-arte` ↔ `design-direction` |
| 18 | **Mapeo de ciclo de vida** (DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP) | `AGENTS.md` | 🟡 Medio | **ADAPTAR** | El nuestro empieza antes: DISCOVER → DESIGN → BUILD → RELEASE. El suyo asume que ya sabes qué construir |
| 19 | **Sección anti-racionalización en el nivel del repo** | `AGENTS.md` | 🟡 Medio | **ADAPTAR** | Útil, pero su versión ("siempre invoca una skill") produciría ceremonia sobre decisiones de una tarde |
| 20 | **Evals Tier 3 — conductual con `expectations[]`** | `evals/README.md` | 🟡 Medio | **ADAPTAR** | Cuesta tokens. Solo bajo demanda, para skills nuevas |
| 21 | **Casos de presión** (prisa, coste hundido, autoridad) | idem | 🟢 Alto | **ADOPTAR** | Nuestro `shape-up-cycle` es una skill de disciplina: es justo donde sirve |
| 22 | **Un archivo de eval por skill, obligatorio al añadirla** | idem | 🟢 Alto | **ADOPTAR** | Acopla crear con evaluar. Sin él, los evals nunca se escriben |
| 23 | Soporte multi-harness (`.codex-plugin`, `.gemini`, `.opencode`) | raíz | 🔴 Nulo | **RECHAZAR** | Un solo harness. Sería mantenimiento puro |
| 24 | 16 documentos de setup por herramienta | `docs/` | 🔴 Nulo | **RECHAZAR** | Idem |
| 25 | Plantillas de issue y flujo de PRs comunitario | `.github/` | 🔴 Bajo | **RECHAZAR** | Ya existen dos plantillas. Un colaborador |
| 26 | **25 skills de ingeniería** (TDD, debugging, code review…) | `skills/` | 🔴 Nulo aquí | **RECHAZAR** | Ya están instaladas `superpowers` y `saas-toolkit`. Importarlas sería triplicar el solape |
| 27 | Runner de evals en Node con TF-IDF | `scripts/` | 🟡 Medio | **ADAPTAR** | La **idea** sí; el código no. Nuestra versión: un `.mjs` sin dependencias, sobre 21 descripciones, no 25 skills |
| 28 | `AGENTS.md` con instrucciones para agentes del propio repo | raíz | 🟡 Medio | **ADAPTAR** | Business Crew no lo tiene. Cabría, pero primero hay que tener qué decir |

**Recuento: 14 ADOPTAR · 10 ADAPTAR · 4 RECHAZAR.**

---

## 4. Riesgos de copiarlo

| # | Riesgo | Por qué es real |
|---|---|---|
| 1 | **Importar sus 25 skills** | Ya están instaladas `superpowers` (TDD, debugging, planning) y `saas-toolkit`. Sería triplicar el solape — y el Tier 2 de ellos mismos demostraría la colisión |
| 2 | **Copiar el ratio 25/4 al revés** | Convertir 18 personas en skills destruiría lo mejor del repo. El criterio de `munger-critico` **no es un procedimiento** |
| 3 | **Multi-harness** | Mantenimiento sin beneficio |
| 4 | **Su ceremonia** | *"Si hay un 1 % de que una skill aplique, invócala"* funciona en un dominio donde cada tarea es un cambio de código. Aquí produciría un workflow para elegir un color |
| 5 | **Copiar el nombre `/ship`** | **Ya está ocupado** en Business Crew con otro significado |
| 6 | **Sus evals tal cual** | Están calibrados para 25 skills de un dominio. Los umbrales hay que recalibrarlos |
| 7 | **Confundir escala** | Su `CONTRIBUTING.md` resuelve coordinación entre desconocidos. Aquí hay una persona |

---

## 5. Lo que más cambia el sistema

Tres cosas, en orden:

### 1 · El Tier 2 de evals

Determinista, gratuito, en CI, y detecta exactamente nuestro fallo dominante. **El mejor
retorno por esfuerzo de todo el estudio**, y el único que se puede ejecutar mañana sobre lo
que ya existe sin cambiar nada.

### 2 · La separación quién / cómo / cuándo

Da vocabulario a un diagnóstico que ya teníamos y no sabíamos nombrar. Explica de golpe las
dos duplicaciones (`director-arte`, `scrum-master`) y por qué `workflows/` no debe ser un
directorio.

### 3 · La anatomía de skill con `Verification`

Cierra el hueco de "cero salidas verificables" sobre material que ya está escrito y
probado. Coste: una sección por skill.

---

## 6. Lo que tenemos y ellos no

Para que el estudio no sea una lista de lo que nos falta:

| Nuestro | Por qué importa |
|---|---|
| **Ciclo de trabajo real** (`shape-up-cycle`, `/bet`, `/hill`, `/ship`) | Ellos tienen ciclo de vida de *tarea*; nosotros de *apuesta*, con appetite y circuit breaker. Es más difícil de escribir y resuelve un problema que ellos no tienen |
| **Hooks que actúan solos** | El aviso de *"llevas 2 días sin mover la colina"* no tiene equivalente allí |
| **Criterio de negocio** | Precio, posicionamiento, mercado, legal. Su repo es de ingeniería |
| **"Cuándo NO aportas" en las 18 personas** | Sus 4 personas son más simples. Nuestros límites están mejor escritos |

**No es un repo mejor: es un repo con el problema contrario resuelto.** Ellos tienen
procedimiento sin criterio de negocio; nosotros criterio sin procedimiento.

---

## 7. Lo que no se pudo verificar

Por honestidad sobre el alcance:

| No verificado | Por qué |
|---|---|
| El código de `scripts/run-evals.js` | No se leyó. Se adopta el **diseño** descrito en su `evals/README.md`, no la implementación |
| Sus 25 `SKILL.md` uno a uno | Se leyó la anatomía y el listado. No hacía falta más para extraer principios |
| Si sus umbrales (95 % rank-1, 75 % colisión) son los correctos **para nosotros** | Habría que ejecutarlo. Por eso se propone empezar en 90 % |
| `references/orchestration-patterns.md` | Citado en su `AGENTS.md`, no leído. Podría contener más patrones útiles |

**Licencia:** MIT (verificado). Compatible. Aun así, no se copia ningún archivo — se
adoptan principios, que es lo que el encargo pedía y lo que además no plantea ninguna
cuestión de atribución.
