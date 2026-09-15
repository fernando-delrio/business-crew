# Informe de Fase 1 — v0.2

> **2026-09-14.** Mejora del sistema existente. **Cero capacidades nuevas.**
> Sin publicar en el momento de escribirlo.
>
> *Informe histórico de la fase. Lo que dice sobre el estado del árbol de trabajo
> describía el momento en que se escribió; para el estado actual, `git status` y
> `git log` son la fuente de verdad.*

---

> **Continuado en [`phase2-report.md`](phase2-report.md)** (2026-09-14): las 4 propuestas
> de §11 se ejecutaron. Holdout TOP-1 38 % → 75 %, UNREACHABLE 25 % → 12 %. Se añadió un
> tercer fixture externo y la métrica `FORBIDDEN-ABOVE-PRIMARY`.


## 1. Resumen

| Métrica | Baseline | Fase 1 | Δ |
|---|--:|--:|:--:|
| **UNREACHABLE CAPABILITY** | **50 %** | **8 %** | **−42** ✅ |
| TOP-1 CORRECT | 25 % | **83 %** | +58 ✅ |
| TOP-3 COVERAGE | 33 % | **83 %** | +50 ✅ |
| MISSING CAPABILITY | 67 % | **17 %** | −50 ✅ |
| AMBIGUOUS ROUTE | 33 % | **25 %** | −8 ✅ |
| **UNNECESSARY CAPABILITY** | 8 % | **25 %** | **+17** 🔴 |
| Colisiones ≥0.75 | 0 | **0** | = ✅ |
| Avisos ≥0.50 | 1 | **0** | −1 ✅ |
| Unidades con genericidad >50 | 12 | **1** | −11 ✅ |
| Frases comodín | 24 | **0** | −24 ✅ |
| Agentes sin fronteras | 1 | **0** | −1 ✅ |
| Comandos ganando consultas de dominio | 2/12 | **0/12** | −2 ✅ |

**Y el aviso que va antes que cualquier titular:** yo escribí los 12 casos **y** reescribí
las 18 descripciones. El 83 % es **parcialmente circular**. El holdout de §8 —vocabulario
deliberadamente distinto— da **38 %**, y es el número más honesto de este informe.

---

## 2. Archivos modificados

**26 archivos tocados, 2 creados.** Ninguno borrado.

| Qué | Cuántos | Cambio |
|---|--:|---|
| `agents/*.md` | **18** | Descripción reescrita + sección `## Output mínimo` |
| ↳ `agents/cfo-precios.md` | | \+ `## Cuándo NO aportas` (era el único sin ella) |
| ↳ `agents/scrum-master.md` | | Tabla de 17 filas → referencia + minimum necessary crew |
| ↳ `agents/director-arte.md` | | Fuera lo que duplicaba a su skill |
| `commands/*.md` | **4** | Descripción específica al momento del ciclo |
| ↳ `commands/crew.md` | | \+ `## Tu frontera con scrum-master` |
| `skills/*/SKILL.md` | **3** | \+ `## Verification` |
| `rules/output-contract.md` | **nuevo** | FACT · INFERENCE · RECOMMENDATION · UNKNOWN · ASSUMPTION · RISK · DECISION |
| `rules/orchestration.md` | **nuevo** | Mapa de enrutado en lenguaje del problema |
| `evals/tier2_similarity.py` | | \+ flag `--cases` para el holdout |
| `evals/fixtures/holdout-cases.json` | **nuevo** | 8 casos de generalización |

**`evals/fixtures/routing-cases.json` no se ha tocado.** Es la condición para que la
comparación signifique algo.

---

## 3. Cambios por agente

### Descripciones — criterio de redacción

1. Empezar por **cómo lo diría alguien con el problema** que no sabe a quién llamar.
2. Después, qué hace y qué posee.
3. Terminar con la frontera (`NO ...`), que es la señal más discriminante.
4. **Conservar el nombre de la persona canalizada** — es vocabulario raro y discrimina mucho.
5. Fuera las frases comodín.

### Los seis prioritarios

| Agente | Antes (fragmento) | Ahora (fragmento) | Score en su caso |
|---|---|---|---|
| `cfo-precios` | *"decisiones de precio, unit economics, saber si algo es rentable"* | *"cuánto cobrar, cuánto pedir por un presupuesto, si el precio deja margen, si te sale a cuenta"* | **0.000 → 0.283** |
| `analista-datos` | *"decidir QUÉ medir, métricas de vanidad, instrumentación mínima"* | *"si entra alguien, si la gente vuelve, si sirve para algo, qué deberías estar mirando y no miras"* | **0.028 → 0.306** |
| `devops-hightower` | *"despliegue, entornos, CI/CD"* | *"funciona en tu máquina pero no publicado, se rompió justo al subirlo, no te fías de volver atrás"* | — |
| `pm-producto` | *"definir el alcance de una feature, priorizar backlog"* | *"se te ocurren cosas y no sabes cuál va primero, te piden tres a la vez y hay que recortar"* | **0.000 → 0.150** (C10) |
| `scrum-master` | *"cuando no sepas por dónde seguir […] deriva al especialista"* | *"vuelves tras un tiempo y no sabes por dónde retomar […] deriva a UNA capacidad"* | 0.195 → 0.260 |
| `dev-dhh` | *"decisiones de arquitectura, complicando de más"* | *"cómo organizar el código, dónde meter algo nuevo, si hace falta esa capa"* | 0.000 → 0.000 ⚠️ |

`dev-dhh` sigue en 0.000 en C06, y es honesto: ese caso trata de **aislamiento
multi-tenant**, cuyo dueño real está **fuera de este repositorio**. No es un fallo de la
descripción: es un hueco declarado.

### Frases comodín — 24 → 0

*"Sirve para cualquier tipo de producto"* estaba en 8 descripciones; *"cualquier stack"* en
3. Eliminadas todas. **No se ha tocado el cuerpo de ningún agente**: solo la descripción,
que es donde compiten por el enrutado.

### `cfo-precios` — la frontera que faltaba

Único de 18 sin sección de derivación. Añadida: deriva a asesor fiscal real,
`legal-basico`, `ventas-ross`, `cmo-godin`, `analista-thompson` y `pm-producto`, y declara
cuándo no hay precio que fijar.

### Contratos de salida — 18 de 18

Cada agente declara ahora su `## Output mínimo`, **proporcional a su función**, no el mismo
molde repetido:

| Agente | Campos |
|---|---|
| `cfo-precios` | valor cuantificado · rango · las 4 cifras · supuestos · siguiente acción |
| `qa-bach` | charter · asunciones no verificadas · casos · hallazgos con severidad y evidencia |
| `ux-norman` | fricción · causa · impacto · recomendación + criterio de aceptación |
| `munger-critico` | 3-5 riesgos por prob × daño · cuáles matan · mitigación de esta semana |
| `seguridad` | ≤5 hallazgos · arreglo · alcance de lo comprobado · qué escala |
| … | los 18, en su archivo |

Todos enlazan a `rules/output-contract.md` para el vocabulario de etiquetas. **La
definición vive en un sitio y se referencia 18 veces; no se copia.**

---

## 4. Cambios en skills

Las tres llevan ahora `## Verification`: qué evidencia demuestra que se aplicó bien, y una
tabla de **qué invalida el resultado**.

| Skill | Líneas | Criterio de salida |
|---|--:|---|
| `decision-framing` | 134 → 159 | 2-3 caminos comparables · *no hacer nada* incluido · problema separado de solución · reversibilidad · `UNKNOWN` visibles |
| `design-direction` | 204 → 232 | 5 decisiones · referencias con URL · un solo gesto · control anti-slop · rúbrica puntuada · ejecución derivada |
| `shape-up-cycle` | 216 → 252 | Por momento: abrir (appetite, no-go, rabbit holes) · durante (posición, movimiento con fecha) · cerrar (circuit breaker, evidencia, retro, cool-down) |

**Sus descripciones NO se han tocado**, y en §8 se ve que eso tiene consecuencias.

---

## 5. Routing source of truth

**`rules/orchestration.md`** — validado contra el anti-bloat gate antes de crearlo:

| Pregunta | Respuesta |
|---|---|
| ¿Problema observado? | ✅ La tabla vivía solo en `scrum-master`, donde no puede ejecutarse |
| ¿Existe ya? | ❌ |
| ¿Sección de otro archivo? | ❌ La referencian `scrum-master`, `/crew` y los evals |
| ¿≥2 usos? | ✅ |
| ¿Criterio de eliminación? | ✅ Si en 2 ciclos nadie lo consulta y el enrutado no mejora |

Contiene: **22 filas de lenguaje del problema** → primaria / secundaria opcional / no
enrutar a · los **3 huecos conocidos** declarados como huecos · minimum necessary crew ·
quién puede orquestar · la frontera entre las dos puertas.

### `scrum-master` — antes y después

| | Antes | Después |
|---|---|---|
| Tabla de derivación | 17 filas **dentro del agente** | Referencia a `rules/orchestration.md` |
| Derivaciones por defecto | Sin límite declarado | **UNA.** Segunda solo con razón explícita |
| Papel | Router | **Guardián del ciclo** que deriva a una |
| Ante un hueco | Derivaba a lo más parecido | **Nombra el hueco** |
| Líneas | 90 → 101 (tras outputs) → **100** | |

### `/crew` — antes y después

| | Antes | Después |
|---|---|---|
| Primera línea | *"Eres el Scrum Master convocando al equipo"* | *"Convocas al equipo para contrastar **una decisión concreta**"* |
| Frontera | No declarada | Tabla explícita de 5 filas |
| Ante *"¿por dónde sigo?"* | Competía | **Deriva a `scrum-master`** |

**La prueba, escrita en los dos archivos:** *"¿qué hago ahora?"* → `scrum-master`.
*"¿qué opináis de esto?"* → `/crew`.

### `director-arte` ↔ `design-direction`

| | Antes | Después |
|---|--:|--:|
| Similitud DESC | **0.628** (máxima del corpus, aviso) | **0.286** |
| Similitud FULL | 0.431 | 0.267 |
| Duplicado en el agente | 5 decisiones · rúbrica 40/30/20/10 · tabla de enrutado · ajuste por producto | **Ninguno** |

El agente conserva lo que es criterio y no procedimiento: exigir el brief, nombrar lo que
ve, defender la contención, y **decidir cuándo el listón ya está**.

---

## 6. Comandos

| Comando | Antes | Después |
|---|---|---|
| `/bet` | *"Abre un ciclo de trabajo…"* | \+ *"Solo para EMPEZAR un ciclo — no decide precios, arquitectura ni diseño"* |
| `/hill` | *"¿Cuesta arriba o cuesta abajo?"* | \+ *"del ciclo de Shape Up que ya está abierto […] Solo DURANTE un ciclo abierto"* |
| `/ship` | *"Cierra el ciclo…"* | \+ *"Solo para CERRAR un ciclo — **no publica nada a producción**"* |
| `/crew` | *"Convoca al equipo…"* | \+ *"sobre UNA decisión concreta […] Para «por dónde sigo», usa `scrum-master`"* |

**Resultado medido: comandos en top-1 de una consulta de dominio pasan de 2/12 a 0/12.**
`/bet` ya no gana una consulta de seguridad; `/hill` ya no gana una de precios.

---

## 7. Resultados — los 12 casos originales

| Caso | Esperado | Baseline | Fase 1 |
|---|---|---|---|
| C01 *"no sé si entra alguien"* | `analista-datos` | ❌ 0.028 | ✅ **0.306** |
| C02 *"el enlace está a la vista"* | `seguridad` | ❌ 0.000 | ✅ **0.382** |
| C03 *"no sé cuánto pedir"* | `cfo-precios` | ❌ 0.000 | ✅ **0.283** |
| C04 *"añadir algo que nadie pidió"* | `pm-producto` | ✅ 0.348 | ✅ 0.472 |
| C05 *"montar el flujo que avisa y reintenta"* | `coo-graham` | ❌ 0.000 | ❌ 0.078 |
| C06 *"varios clientes sin que se vean"* | `dev-dhh` | ❌ 0.000 | ❌ 0.000 |
| C07 *"la gente se atasca"* | `ux-norman` | ✅ 0.184 | ✅ 0.403 |
| C08 *"tests pasan, ¿publico?"* | `qa-bach` | ❌ 0.000 | ✅ **0.442** |
| C09 *"quién más hace esto"* | `analista-thompson` | ~3 0.129 | ✅ **0.406** |
| C10 *"tres cosas a la vez"* | `pm-producto` | ❌ 0.000 | ✅ 0.150 |
| C11 *"vuelvo tras dos semanas"* | `scrum-master` | ✅ 0.195 | ✅ 0.260 |
| C12 *"se ve soso"* | `director-arte` | ❌ 0.041 | ✅ **0.466** |

**Los dos que siguen fallando son los dos huecos conocidos**, declarados como tales antes
de medir: C05 (nadie posee arquitectura de automatización) y C06 (el dueño está fuera del
repo). **No son fallos de descripción: son capacidades que no existen.**

### Hipótesis, releídas

| | Baseline | Fase 1 | Lectura |
|---|--:|--:|---|
| H1 `director-arte` ↔ `design-direction` | 0.628 | **0.286** | La etiqueta dice "RECHAZADA" porque la hipótesis original predecía similitud **alta**. **Rechazarla ahora es el objetivo cumplido**, no una regresión |
| H2 `scrum-master` ↔ `/crew` | 0.061 | **0.318** | Sube **a propósito**: ver §9 |
| H3a/b/c | 0.083/0.022/0.021 | 0.072/0.040/0.024 | Confirmadas |
| H4 `dev-dhh` ↔ `devops-hightower` | 0.137 | **0.053** | Confirmada, y mejor separados |
| H5 `ux-norman` ↔ `ui-duarte` | 0.207 | 0.195 | Confirmada |

---

## 8. Holdout — el número honesto

Los 12 casos los escribí yo y después reescribí las descripciones. Para saber si la mejora
**generaliza** o solo **memoriza**, escribí 8 casos nuevos con vocabulario deliberadamente
distinto, sin tocar el fixture original.

| Métrica | Fixture original | **Holdout** |
|---|--:|--:|
| TOP-1 | 83 % | **38 %** |
| TOP-3 | 83 % | **50 %** |
| UNREACHABLE | 8 % | **25 %** |
| AMBIGUOUS | 25 % | **50 %** |

**Interpretación honesta:** hay mejora real —el baseline daba 25 % TOP-1 y 50 %
UNREACHABLE sobre casos que también escribí yo— pero **una parte del 83 % es sobreajuste a
mis propias frases**. El 38 % del holdout es el suelo creíble.

### Y el holdout destapa algo que los 12 originales no veían

| Caso | Esperado | Quién gana | Problema |
|---|---|---|---|
| H01 *"sigo sin saber si alguien lo usa"* | `analista-datos` (0.108) | **`shape-up-cycle`** (0.198) | Una **skill** gana una consulta de dominio |
| H03 *"se me ha quedado una contraseña dentro"* | `seguridad` (0.178) | **`decision-framing`** (0.179) | Idem, por 0.001 |
| H06 *"que le llegue el aviso sin que yo haga nada"* | `coo-graham` (0.000) | **`decision-framing`** (0.178) | Idem + hueco conocido |
| H04 *"cada vez que subo una versión algo deja de ir"* | `devops-hightower` (**0.000**) | `cfo-precios` | **Inalcanzable** con vocabulario nuevo |
| H07 *"en qué me puedo estar equivocando"* | `munger-critico` (0.048) | `ventas-ross` | Débil |

> 🔴 **Hallazgo nuevo: afilé los 18 agentes y los 4 comandos, pero no las 3 skills. Las
> skills se han convertido en el nuevo suelo de ruido.**
>
> `decision-framing` gana una consulta de **seguridad**. `shape-up-cycle` gana una de
> **analítica**. Sus descripciones no eran genéricas antes, pero ahora lo son **en
> relativo**, porque todo lo demás se afiló.
>
> **No lo he arreglado**: la instrucción de esta fase alcanzaba a agentes (§1) y comandos
> (§11); de las skills pedía `Verification` (§10), no reescribir su descripción. Queda como
> la propuesta nº 1 de la Fase 2, con datos.

---

## 9. Regresiones — sin maquillar

### 🔴 R1 · UNNECESSARY CAPABILITY: 8 % → 25 %

Tres casos con una capacidad prohibida entre las candidatas:

| Caso | Prohibida | ¿Regresión real? |
|---|---|---|
| **C05** | `ventas-ross` en top-1 | **Sí, real.** Es el hueco de automatización: sin dueño, gana el ruido. Se arregla con la capacidad, no con la descripción |
| **C09** | `qa-bach` en 2.º | **No.** Ya estaba en el baseline, y ahora `analista-thompson` **gana** (era 3.º). El caso mejoró; la métrica no lo distingue |
| **C12** | `cmo-godin` en 2.º | **Discutible, y el error puede ser mío.** `director-arte` gana con 0.466. Que alguien diga *"parece igual que cualquier otra"* puede ser un problema de **posicionamiento**, no solo visual — mi `should_not_route_to` era probablemente demasiado estricto. **No cambio el fixture** |

**Lectura:** de tres, una es real (síntoma de un hueco), una es un artefacto de la métrica
—que cuenta presencia en top-3, no desplazamiento— y una es un fallo de mi propio criterio
al escribir el caso.

### 🟠 R2 · `scrum-master` ↔ `/crew`: 0.061 → 0.318

**Deliberado.** Ambas descripciones se nombran mutuamente para declarar la frontera:
`scrum-master` dice *"para contrastar varias perspectivas a la vez está /crew"*; `/crew`
dice *"para «por dónde sigo», usa scrum-master"*.

| A favor | En contra |
|---|---|
| Un lector —humano o modelo— sabe cuál elegir | La similitud léxica sube |
| Resuelve la duplicación funcional que H2 reveló | |
| 0.318 está **muy por debajo** del aviso (0.50) | |

**Se acepta.** Una referencia cruzada explícita es la forma correcta de declarar una
frontera, y el coste medido es aceptable. Si superara 0.50, habría que replantearlo.

### 🟠 R3 · `legal-basico` ↔ `seguridad`: 0.034 → 0.215

Mismo mecanismo: `legal-basico` añadió *"NO cubre la seguridad técnica de los datos
(seguridad)"*. Es el nuevo máximo agent↔agent (0.215 frente a 0.207 antes).

**Se acepta.** La media agent↔agent **bajó** de 0.045 a 0.036: el conjunto está mejor
separado aunque un par concreto suba.

### 🟠 R4 · Las skills como nuevo suelo de ruido

Ver §8. **No arreglada en esta fase, por alcance.**

### Regression gate

| Condición de fallo | Resultado |
|---|:--:|
| UNREACHABLE empeora | ✅ 50 % → 8 % |
| Nuevas colisiones ≥0.75 | ✅ 0 → 0 |
| Solape agent↔agent fuerte aumenta sin justificación | ✅ Media 0.045 → 0.036. El único par que sube está justificado (R3) |
| `cfo-precios` sigue inaccesible | ✅ 0.000 → 0.283, gana su caso |
| `analista-datos` sigue inaccesible | ✅ 0.028 → 0.306, gana su caso |
| Enrutado de comandos empeora | ✅ 2/12 → 0/12 |

**El gate pasa en las seis condiciones.** R1 no está entre ellas y se reporta igual.

---

## 10. Limitaciones

| # | Limitación |
|---|---|
| 1 | 🔴 **Circularidad.** Autor de los casos = autor de las descripciones. El 83 % está inflado; el 38 % del holdout es el suelo creíble |
| 2 | 🔴 **El holdout tampoco es independiente.** Mismo autor, escrito después. Mitiga el sobreajuste a frases concretas, no el sesgo de quien lo escribe |
| 3 | **Sigue siendo léxico.** El harness real usa selección semántica. Estos números miden **descripciones**, no el sistema en producción |
| 4 | **12 + 8 casos son pocos.** Cada uno vale 8 y 12,5 puntos |
| 5 | **Los `expected_primary` son mi criterio.** C12 lo demuestra: probablemente me equivoqué al prohibir `cmo-godin` |
| 6 | **`UNNECESSARY` mide presencia en top-3, no desplazamiento.** Penaliza casos que mejoraron |
| 7 | **No se ha probado con el harness real.** Que una descripción puntúe mejor en TF-IDF no demuestra que un modelo la elija mejor |
| 8 | **No mide si los `Output mínimo` se cumplen.** Eso es Tier 3 y cuesta tokens |
| 9 | **Corpus de 25.** Los IDF son inestables |

---

## 11. Qué proponer para la Fase 2 — con datos

| # | Propuesta | Evidencia |
|---|---|---|
| **1** | 🔴 **Reescribir las 3 descripciones de skill** con el mismo criterio | Holdout: `decision-framing` gana una consulta de seguridad; `shape-up-cycle` una de analítica |
| **2** | 🟠 **Revisar `devops-hightower`** | Inalcanzable (0.000) en H04 con vocabulario nuevo, pese a estar entre los seis prioritarios |
| **3** | 🟠 **Revisar `munger-critico` y `coo-graham`** | 0.048 y 0.000 en el holdout |
| **4** | 🟡 **Ampliar el holdout con casos que no escriba yo** | Es la única forma de romper la circularidad |
| **5** | 🟡 **Revisar `should_not_route_to` de C12** | Probablemente mal puesto. Requiere aprobación: cambiar un fixture altera la comparación histórica |
| **6** | ⚪ **Los huecos C05/C06 no se arreglan con descripciones** | Necesitan capacidad, y eso está fuera de la Fase 1 |

---

## 12. Decisiones pendientes

| # | Decisión |
|---|---|
| 1 | 🟠 **¿Se acepta R2?** `scrum-master` ↔ `/crew` sube a 0.318 a cambio de una frontera explícita |
| 2 | 🟠 **¿Se aprueba reescribir las 3 descripciones de skill** en la Fase 2? |
| 3 | 🟡 **¿Se corrige el fixture C12?** Cambiarlo rompe la comparabilidad con el baseline |
| 4 | 🟡 **¿Se acepta el holdout como parte del eval permanente**, o se mantiene solo el fixture original? |
