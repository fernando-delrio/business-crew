# Informe de Fase 2 — v0.2

> **2026-09-14.** Mejorar generalización sin añadir capacidades.
> Sin publicar en el momento de escribirlo. Fixtures históricos intactos.
>
> *Informe histórico de la fase. Lo que dice sobre el estado del árbol de trabajo
> describía el momento en que se escribió; para el estado actual, `git status` y
> `git log` son la fuente de verdad.*

---

## 1. Resumen

| Métrica | ORIGINAL | HOLDOUT | EXTERNAL | **MACRO** |
|---|--:|--:|--:|--:|
| TOP-1 | 83 % | 75 % | 33 % | **63.9 %** |
| TOP-3 | 83 % | 88 % | 42 % | **70.8 %** |
| UNREACHABLE | 8 % | 12 % | 50 % | **23.6 %** |
| MISSING | 17 % | 12 % | 58 % | **29.2 %** |
| AMBIGUOUS | 25 % | 50 % | 42 % | **38.9 %** |
| UNNECESSARY | 33 % | 12 % | 17 % | **20.8 %** |
| FORBIDDEN-ABOVE-PRIMARY | 8 % | 0 % | 17 % | **8.3 %** |

MACRO = promedio **simple** entre fixtures. Cada uno mide algo distinto y ninguno diluye al
otro. **Los tres se reportan siempre por separado.**

### El movimiento

| | Fase 1 | Fase 2 | |
|---|--:|--:|:--:|
| **HOLDOUT TOP-1** | 38 % | **75 %** | +37 ✅ |
| **HOLDOUT TOP-3** | 50 % | **88 %** | +38 ✅ |
| **HOLDOUT UNREACHABLE** | 25 % | **12 %** | −13 ✅ |
| **EXTERNAL TOP-1** | 8 %* | **33 %** | +25 ✅ |
| **EXTERNAL UNREACHABLE** | 75 %* | **50 %** | −25 ✅ |
| ORIGINAL TOP-1 | 83 % | 83 % | = |
| ORIGINAL UNREACHABLE | 8 % | 8 % | = |
| **ORIGINAL UNNECESSARY** | 25 % | **33 %** | **+8** 🔴 |

\* El fixture externo se escribió **antes** de la Fase 2 y se midió contra el sistema tal
como quedó en la Fase 1. Ese 8 % / 75 % es su baseline legítimo.

**Lectura:** la generalización mejoró de verdad. El fixture original no se movió — que es
lo correcto, porque ya estaba en su techo. Y aparece una regresión en `UNNECESSARY`, §10.

---

## 2. Protocolo anti-circularidad

La limitación más grave de la Fase 1 era que yo escribía las descripciones **y** los casos.

**Esta vez el fixture externo se escribió ANTES de tocar ninguna descripción.** No se puede
haber ajustado el sistema a esas frases porque cuando se escribieron aún no existían las
descripciones nuevas.

```
1. escribir external-style-cases.json        ← 12 casos, 7 perfiles, congelado
2. medir el sistema tal como estaba          ← TOP-1 8 %, UNREACHABLE 75 %
3. reescribir 3 skills + 3 agentes
4. volver a medir                            ← TOP-1 33 %, UNREACHABLE 50 %
```

**Sigue sin ser independiente** —mismo autor— pero el orden elimina el sobreajuste a frases
concretas, que era el mecanismo principal del problema.

---

## 3. Archivos modificados

| Qué | Cambio |
|---|---|
| `skills/shape-up-cycle/SKILL.md` | Descripción |
| `skills/decision-framing/SKILL.md` | Descripción |
| `skills/design-direction/SKILL.md` | Descripción |
| `agents/devops-hightower.md` | Descripción |
| `agents/munger-critico.md` | Descripción |
| `agents/coo-graham.md` | Descripción |
| `rules/orchestration.md` | \+ §3bis DOMAIN FIRST / PROCEDURE SECOND |
| `evals/tier2_similarity.py` | \+ `--all-fixtures`, `--json-prefix`, `evaluar_casos()`, métrica `FORBIDDEN-ABOVE-PRIMARY` |
| `evals/fixtures/external-style-cases.json` | **Nuevo**, 12 casos |
| `docs/v0.2/phase2-report.md` · `tier3-design.md` · `usage-telemetry-design.md` | **Nuevos** |

**Intactos:** los otros 15 agentes · los 4 comandos · `routing-cases.json` ·
`holdout-cases.json` · hooks · permisos.

---

## 4. Cambios en las 3 skills

Principio: **una skill de procedimiento no debe contener vocabulario de dominio.** Si
nombra precio, seguridad o arquitectura, competirá con sus agentes y ganará por accidente.

| Skill | Antes | Ahora |
|---|---|---|
| `shape-up-cycle` | *"Úsalo para abrir una apuesta, saber si estás cuesta arriba… **Actívalo cuando alguien pregunte por dónde seguir**, cuánto va a tardar algo…"* | *"Úsala **SOLO cuando ya se trabaja con este ciclo**… NO es para saber por dónde seguir en general (**eso es scrum-master**), NO decide qué construir, NO aplica fuera de un ciclo abierto"* |
| `decision-framing` | *"Actívalo cuando alguien pregunte **si debe construir algo, elegir entre opciones**…"* | *"Úsala cuando **YA hay dos o tres caminos concretos** sobre la mesa… Es un **PROCEDIMIENTO, no criterio de dominio**: si la duda es de precio, seguridad, datos, interfaz o arquitectura, **primero va el agente de ese dominio**"* |
| `design-direction` | *"Dirección de arte antes de escribir una línea de interfaz… **cuando algo «se ve genérico»**"* | *"Úsala cuando toque **ESTRUCTURAR o VALIDAR** una dirección visual ya planteada. **Si lo que hay es una insatisfacción vaga —«se ve soso»— el primario es director-arte**"* |

**El cambio en `shape-up-cycle` es el más importante.** Contenía *"por dónde seguir"*,
*"cuánto va a tardar"* y *"llevar días sin avanzar"* — vocabulario que compite con medio
catálogo. Ahora solo compite cuando hay ciclo.

**Cero cambios metodológicos.** Solo descripciones y fronteras.

---

## 5. Cambios en los 3 agentes

| Agente | Vocabulario añadido | Resultado |
|---|---|---|
| `devops-hightower` | *lo subes y deja de funcionar · en tu ordenador va y publicado no · se ha roto tras publicar una versión nueva · **quieres volver atrás** · no sabes si el despliegue ha salido bien* | **H04: 0.000 → 0.230**, gana |
| `munger-critico` | *te da mala espina · **todos dan por hecho que va a salir bien** · qué puede salir mal · qué no estás viendo · qué supuesto puede explotar* | **H07: 0.048 → 0.174**, gana. **E06: 0.000 → 0.224**, gana |
| `coo-graham` | *te pasas el día repitiendo lo mismo a mano · los mismos mensajes · los mismos correos · copiar y pegar una y otra vez* | **E03: 0.000 → 0.272**, gana |

**`coo-graham` NO se ha convertido en arquitecto de automatización.** Su descripción sigue
diciendo *"NO diseña cómo se construye ese automatismo"*. Por eso C05 y H06 **siguen
fallando, y es correcto**: piden arquitectura, que es un hueco declarado.

Fronteras mantenidas: `devops-hightower` sigue declarando que no arregla bugs de lógica
(`dev-dhh`), no decide qué probar (`qa-bach`) ni revisa contraseñas (`seguridad`).

---

## 6. DOMAIN FIRST / PROCEDURE SECOND

En `rules/orchestration.md` §3bis.

> **Si la consulta necesita primero criterio de un dominio, el primario es el agente de ese
> dominio. Una skill de procedimiento puede ser secundaria — nunca primaria — salvo que el
> usuario pida el procedimiento explícitamente.**

**La prueba, en una pregunta:**

> ¿Lo que falta es **saber la respuesta**, o **saber cómo elegir** entre respuestas que ya
> tenemos?

Lo primero es dominio. Lo segundo es procedimiento. **En la duda gana el dominio:** una
skill mal invocada gasta un turno; un dominio mal invocado da una respuesta equivocada.

Incluye la tabla de 8 casos y el corolario: **una skill no debe nombrar dominios en su
descripción.**

---

## 7. Skills ganando dominio — antes y después

El hallazgo que cerró la Fase 1:

| Fixture | Fase 1 | **Fase 2** |
|---|---|---|
| HOLDOUT H01 *"si alguien lo usa"* | `shape-up-cycle` (0.198) 🔴 | **`analista-datos`** ✅ |
| HOLDOUT H03 *"una contraseña dentro"* | `decision-framing` (0.179) 🔴 | `devops-hightower` 🟡 |
| HOLDOUT H06 *"aviso sin que yo haga nada"* | `decision-framing` (0.178) 🔴 | `/hill` 🟡 |
| **Skills en top-1 de consulta de dominio** | **3** | **0** ✅ |

**Cero.** En los tres fixtures —32 casos— ninguna skill gana una consulta puramente de
dominio. El problema que cerró la Fase 1 está resuelto.

**Pero el ruido se ha mudado, no ha desaparecido:**

| Fixture | Comandos en top-1 de consulta de dominio |
|---|---|
| ORIGINAL | **0/12** ✅ |
| HOLDOUT | **1/8** — `/hill` gana H06 |
| EXTERNAL | **2/12** — `/ship` gana E09, `/hill` gana E11 |

`/hill` y `/ship` son ahora lo más genérico del catálogo. Afilé agentes (Fase 1) y skills
(Fase 2); **los comandos se quedaron donde estaban en relativo**. Es el mismo mecanismo que
la Fase 1 descubrió con las skills, un escalón más abajo.

---

## 8. Resultados por caso

### ORIGINAL — 10/12 top-1 (sin cambio)

Los dos fallos son los **huecos conocidos**: C05 (nadie posee arquitectura de
automatización) y C06 (el dueño está fuera del repo). Ambos declarados antes de medir.

### HOLDOUT — 6/8 top-1 (antes 3/8)

| Caso | Fase 1 | Fase 2 |
|---|---|---|
| H01 `analista-datos` | ❌ 0.108 | ✅ **0.129** |
| H02 `cfo-precios` | ✅ 0.150 | ✅ 0.151 |
| H03 `seguridad` | ~3 0.178 | ~3 0.119 🟡 |
| H04 `devops-hightower` | ❌ **0.000** | ✅ **0.230** |
| H05 `ux-norman` | ✅ 0.188 | ✅ 0.192 |
| H06 `coo-graham` | ❌ 0.000 | ❌ 0.000 *(hueco)* |
| H07 `munger-critico` | ❌ 0.048 | ✅ **0.174** |
| H08 `legal-basico` | ✅ 0.202 | ✅ 0.207 |

H03 baja ligeramente: `devops-hightower` le gana por 0.010 en *"se me ha quedado una
contraseña dentro de los archivos que subo"*. **Efecto secundario de darle vocabulario de
«subir»**. `seguridad` sigue 2.º, y su frontera declara explícitamente que no revisa
contraseñas — pero el efecto es real y se anota.

### EXTERNAL — 4/12 top-1 (antes 1/12)

| Aciertan | Fallan |
|---|---|
| E01 `analista-datos` (0.203) · E03 `coo-graham` (0.272) · E06 `munger-critico` (0.224) · E07 `legal-basico` (0.120) | E02 `cfo-precios` · E04 `devops-hightower` · E05 `ux-norman` · E08 `cmo-godin` · E09 `seguridad` · E11 `decision-framing` · E12 `scrum-master` — todos **0.000** · E10 `director-arte` 2.º |

**Los tres agentes revisados aciertan sus casos externos** (E03, E06, y E04 no — ver
abajo). Los que fallan son, en su mayoría, **agentes que esta fase no podía tocar**.

**E04 merece nota:** `devops-hightower` acierta H04 (*"cada vez que subo una versión"*) y
falla E04 (*"lo subí ayer y hoy no carga, en mi portátil iba perfecto"*) con 0.000. Añadí
*"lo subes"*, pero no *"no carga"* ni *"portátil"*. Muestra el techo del método: cada
sinónimo hay que ponerlo a mano.

---

## 9. Colisiones

| | Fase 1 | **Fase 2** |
|---|--:|--:|
| Colisiones ≥0.75 | 0 | **0** |
| Avisos ≥0.50 | 0 | **0** |
| Media agent↔agent | 0.036 | **0.037** |
| Máx agent↔agent | 0.215 (`legal-basico`↔`seguridad`) | **0.194** (idem) |

### Top 5

| A | B | DESC | Nota |
|---|---|--:|---|
| `shape-up-cycle` | `/hill` | 0.325 | Legítimo: el comando ejecuta la skill |
| `scrum-master` | `/crew` | 0.312 | R2, aceptada por el mantenedor |
| `director-arte` | `design-direction` | **0.299** | Sube 0.013 desde 0.286. Ambos se nombran para declarar la frontera. **Muy por debajo de 0.50** |
| `shape-up-cycle` | `/bet` | 0.276 | Legítimo |
| `/bet` | `/ship` | 0.200 | Legítimo |

`skill↔skill` sube de 0.035 a 0.083 de media: las tres declaran ahora su naturaleza
procedimental con vocabulario parecido. Máximo 0.135. Sin consecuencia.

### Hipótesis

H1 0.286 → **0.299** · H2 0.318 → **0.312** · H3a/b/c confirmadas ·
H4 0.053 → **0.102** · H5 0.195 → **0.194**.

H4 sube porque `devops-hightower` y `munger-critico` ahora comparten vocabulario de *"algo
se ha roto"*. `devops-hightower ↔ munger-critico` aparece en el top 10 con 0.151. Sin
consecuencia medida: ningún caso se cruza.

---

## 10. R1 reclasificada

`UNNECESSARY` en el fixture original: 25 % → **33 %**. Clasificación de las siete
ocurrencias en los tres fixtures:

| Fixture | Caso | Prohibida | Score vs primaria | Clasificación |
|---|---|---|---|---|
| ORIGINAL | C01 | `devops-hightower` | 0.084 vs **0.324** | **METRIC ARTIFACT** — 4× por debajo. Aparece porque le di vocabulario de *"publicar"* |
| ORIGINAL | C05 | `ventas-ross` | 0.153 vs 0.067 | 🔴 **TRUE ERROR** — por encima de la primaria. Síntoma del hueco de automatización |
| ORIGINAL | C09 | `qa-bach` | 0.098 vs **0.392** | **METRIC ARTIFACT** |
| ORIGINAL | C12 | `cmo-godin` | 0.130 vs **0.463** | **FIXTURE QUESTIONABLE** — *"parece igual que cualquier otra"* puede ser posicionamiento. Fixture **no modificado** |
| HOLDOUT | H04 | `cfo-precios` | 0.118 vs **0.230** | **METRIC ARTIFACT** |
| EXTERNAL | E10 | `dev-dhh` | 0.178 vs 0.160 | 🔴 **TRUE ERROR** — `dev-dhh` gana *"no me gusta cómo ha quedado"* |
| EXTERNAL | E11 | `cfo-precios` | 0.112 vs 0.065 | **VALID SECONDARY** — la consulta dice *"cuesta menos"*. Es defendible; el problema es que `decision-framing` esté tan abajo |

**Recuento: 2 TRUE ERROR · 3 METRIC ARTIFACT · 1 FIXTURE QUESTIONABLE · 1 VALID SECONDARY.**

### La métrica nueva

`UNNECESSARY` cuenta **presencia en top-3**. Penaliza casos que mejoraron: en C09 la
primaria pasó de 3.ª a 1.ª y la métrica marca lo mismo.

Se añade **`FORBIDDEN-ABOVE-PRIMARY`**: una prohibida **por encima** de la esperada.

| | ORIGINAL | HOLDOUT | EXTERNAL | MACRO |
|---|--:|--:|--:|--:|
| UNNECESSARY | 33 % | 12 % | 17 % | 20.8 % |
| **FORBIDDEN-ABOVE-PRIMARY** | **8 %** | **0 %** | **17 %** | **8.3 %** |

**`UNNECESSARY` NO se ha borrado.** Las dos se reportan: una mide contaminación del top-3,
la otra desplazamiento real. Quitar la primera porque incomoda sería exactamente lo que el
encargo prohíbe.

---

## 11. Regression gate

| Condición de fallo | Resultado | |
|---|---|:--:|
| ORIGINAL UNREACHABLE > 8 % | **8 %** — sin cambio | ✅ |
| HOLDOUT UNREACHABLE > 25 % | **12 %** | ✅ |
| Colisión ≥0.75 | **0** | ✅ |
| **Comando gana dominio injustificadamente** | **ORIGINAL 0/12** ✅ · **HOLDOUT 1/8 · EXTERNAL 2/12** | 🔴 **FALLA** |
| Skill gana consulta puramente de dominio | **0 en 32 casos** | ✅ |
| `cfo-precios` pierde su caso | C03 gana con 0.233 | ✅ |
| `analista-datos` pierde su caso | C01 gana con 0.324 | ✅ |
| `director-arte` ↔ `design-direction` > 0.50 | **0.299** | ✅ |

### La condición que falla

**Siete de ocho pasan. La cuarta falla, y no la maquillo.**

Sobre el fixture contra el que se definió el gate —el original— los comandos ganan **0 de
12**, igual que en la Fase 1. Pero en holdout y external ganan **3 veces**: `/hill` en H06 y
E11, `/ship` en E09.

Leído estrictamente **sobre los tres fixtures, esta condición falla.** No fue previsto
porque en la Fase 1 solo existía un fixture.

**Causa:** afilé agentes y skills; los comandos se quedaron igual y ahora son lo más
genérico del catálogo. `/hill` tiene 27 palabras útiles y `/ship` 17, así que la
normalización L2 concentra el peso en pocos términos y cualquier coincidencia parcial
puntúa alto.

**No lo he arreglado**: el encargo de esta fase alcanzaba a las 3 skills (§1-4) y a tres
agentes (§5). Reescribir comandos otra vez no estaba autorizado. **Es la propuesta nº 1 de
la Fase 3.**

---

## 12. Huecos reales que quedan

| # | Hueco | Evidencia | Se arregla con |
|---|---|---|---|
| **1** | **Arquitectura de automatización** | C05 y H06 fallan en las tres fases | Una capacidad, no una descripción |
| **2** | **Ciclo de vida del dato** | C06 inalcanzable siempre | Idem |
| **3** | **Aislamiento multi-tenant** | C06. El dueño está **fuera del repo** | Enlazar a `saas-multitenant-architecture` |
| **4** | **Comandos genéricos** | 3 casos en holdout+external | Descripciones, autorización pendiente |
| **5** | **Los 15 agentes no revisados** | E02, E05, E08, E09, E12 con 0.000 externo | Descripciones, autorización pendiente |

**El nº 5 es el más grande y el menos visible.** El fixture externo muestra que el problema
de vocabulario coloquial **no era de los tres agentes revisados: es general**. `cfo-precios`
gana su caso del fixture original (0.233) y **es inalcanzable** en *"un chaval me ha pedido
seiscientos euros, ¿me está clavando?"*.

---

## 13. Limitaciones

| # | Limitación |
|---|---|
| 1 | **El fixture externo lo escribí yo.** El orden elimina el sobreajuste a frases, no el sesgo de autor |
| 2 | **Sigue siendo léxico.** Cada sinónimo hay que ponerlo a mano: `devops-hightower` acierta *"subo una versión"* y falla *"lo subí ayer y no carga"* |
| 3 | **32 casos en total.** Cada uno vale entre 8 y 12,5 puntos en su fixture |
| 4 | **El techo del método está cerca.** EXTERNAL 50 % de inalcanzables no baja mucho más sin meter jerga coloquial en las descripciones, lo que sería mal diseño |
| 5 | **No se ha probado con el harness real**, que es semántico |
| 6 | **Los `expected_primary` son mi criterio.** E11 y C12 lo demuestran |
| 7 | **Nada mide si los contratos de salida se cumplen.** Eso es Tier 3, diseñado y no implementado |

---

## 14. Decisión recomendada para la Fase 3

**Recomiendo parar el trabajo de descripciones.**

Tres razones, en orden:

1. **Rendimientos decrecientes medibles.** Fase 1 movió el holdout 37 puntos. Fase 2 movió
   el externo 25. Lo que queda son sinónimos coloquiales uno a uno, y meterlos en las
   descripciones las degrada como documentación para un lector humano.
2. **El método está en su techo.** 50 % de inalcanzables en lenguaje externo es una
   propiedad de TF-IDF sobre descripciones de 25 palabras, no de estas descripciones.
3. **Los huecos que quedan no son de descripción.** Los dos que fallan en los tres fixtures
   necesitan una capacidad que no existe.

### Si se sigue, este es el orden por evidencia

| # | Acción | Coste | Evidencia |
|---|---|---|---|
| 1 | **Afilar los 4 comandos** | Bajo | La única condición del gate que falla |
| 2 | **Pasar los 15 agentes restantes** con el criterio de la Fase 1 | Medio | 5 inalcanzables en el fixture externo |
| 3 | **Enlazar el hueco 3** a `saas-multitenant-architecture` | Muy bajo | Existe y está instalada |
| 4 | **Casos externos escritos por un autor humano independiente**, no por mí | Bajo para esa persona | La única forma de romper la circularidad de verdad |

### Y una alternativa que merece considerarse

**Dejar de optimizar el enrutado léxico y pasar al Tier 3.** El Tier 2 ya cumplió su
función: encontró el problema, lo midió, y guió dos fases de arreglo con resultados reales.
Lo que hoy **no** sabemos es si los agentes cumplen los contratos que se les escribieron —
y eso vale más que subir el externo de 33 % a 40 %.

---

## 15. Decisiones pendientes

| # | Decisión |
|---|---|
| 1 | 🔴 **El gate falla en la condición 4.** ¿Se acepta como hallazgo y se arregla en Fase 3, o se considera bloqueante? |
| 2 | 🟠 **¿Se autoriza afilar los 4 comandos?** Es lo que arregla esa condición |
| 3 | 🟠 **¿Se pasan los 15 agentes restantes**, o se acepta el techo actual? |
| 4 | 🟡 **¿Escribe el siguiente fixture externo un autor humano independiente?** Es la única forma real de romper la circularidad |
| 5 | 🟡 **¿Fase 3 sigue con enrutado o salta a Tier 3?** Mi recomendación: Tier 3 |
