# Análisis de enrutado — baseline

> **2026-09-09.** Cobertura de la tabla actual y detección de
> **CAPABILITY EXISTS / NO RELIABLE ROUTE**.
> Datos de `evals/tier2_similarity.py`. **Nada modificado.**

---

> ⚠️ **Este documento es el registro del BASELINE — el estado ANTES de la Fase 1.**
> Sus números se conservan intactos a propósito: son el punto de comparación.
> Los resultados posteriores están en [`phase1-report.md`](phase1-report.md).
>
> **Resumen del cambio:** UNREACHABLE 50 % → 8 % · TOP-1 25 % → 83 % · comodines 24 → 0 ·
> avisos ≥0.50 1 → 0. Con una regresión (UNNECESSARY 8 % → 25 %) y un aviso de
> circularidad: un holdout con vocabulario distinto da **38 %** de TOP-1, no 83 %.


## 1. La distinción que ordena todo

Un enrutado puede fallar de dos formas, y se arreglan distinto:

| Fallo | Síntoma | Método que lo detecta |
|---|---|---|
| **Colisión** | Dos capacidades compiten por la misma consulta | Tier 2 · similitud de descripciones |
| **Inalcanzabilidad** | La capacidad correcta no compite por nada | Tier 2 · casos de enrutado |

**El baseline dice que el problema de Business Crew es el segundo, no el primero:**
cero colisiones ≥0.75, pero **50 % de capacidades inalcanzables**.

Ese es el hallazgo central y contradice lo que yo había supuesto.

---

## 2. Cobertura de la tabla de `scrum-master`

17 filas. **17 de 18 agentes aparecen**; el ausente es `scrum-master`, que es el propio
router — correcto.

**Cobertura nominal: 94 %.** Y aun así el enrutado falla. Eso significa que **el problema
no es la cobertura de la tabla**.

| Agente | En tabla | Trigger declarado | Calidad | Score en su caso |
|---|:--:|---|---|--:|
| `ceo-bezos` | ✅ | *Decidir entre proyectos, visión* | 🟢 Específico | — |
| `munger-critico` | ✅ | *Buscar dónde va a fallar esto* | 🟢 Específico | — |
| `pm-producto` | ✅ | *Definir qué construir y qué no* | 🟢 Específico | **0.348** ✅ |
| `cfo-precios` | ✅ | *Precio, márgenes, rentabilidad* | 🟡 Vocabulario de experto | **0.000** 🔴 |
| `coo-graham` | ✅ | *Automatizar vs hacerlo a mano* | 🟡 Presupone el marco | **0.000** 🔴 |
| `ux-norman` | ✅ | *Un flujo confunde al usuario* | 🟢 Específico | **0.184** ✅ |
| `ui-duarte` | ✅ | *Color, tipografía, jerarquía, tokens* | 🟢 Específico | — |
| `director-arte` | ✅ | *Antes de construir cualquier interfaz* | 🟡 Temporal, no sintomático | **0.041** 🔴 |
| `analista-datos` | ✅ | *Qué medir, si algo funcionó* | 🟡 Presupone saber que se mide | **0.028** 🔴 |
| `dev-dhh` | ✅ | *Cómo estructurar el código* | 🟡 Amplio | **0.000** 🔴 |
| `qa-bach` | ✅ | *Qué probar antes de desplegar* | 🟡 Vocabulario de experto | **0.000** 🔴 |
| `devops-hightower` | ✅ | *Despliegue, entornos, CI* | 🟡 Vocabulario de experto | — |
| `seguridad` | ✅ | *Exponer algo público, datos de clientes* | 🟡 Abstracto | **0.000** 🔴 |
| `cmo-godin` | ✅ | *Mensaje, posicionamiento, marca* | 🟢 Específico | — |
| `ventas-ross` | ✅ | *Conseguir los primeros clientes* | 🟢 Específico | — |
| `analista-thompson` | ✅ | *Competencia, hueco de mercado* | 🟢 Específico | 0.129 ~3 |
| `legal-basico` | ✅ | *Licencias, contratos, condiciones* | 🟢 Específico | — |
| `scrum-master` | — | *(es el router)* | — | **0.195** ✅ |

### El patrón

Los triggers están escritos **en el idioma del experto, no en el del que tiene el
problema**.

| Trigger de la tabla | Cómo lo diría de verdad alguien con el problema |
|---|---|
| *"Precio, márgenes, rentabilidad"* | *"no sé cuánto pedir por esto"* |
| *"Qué probar antes de desplegar"* | *"los tests pasan, ¿lo publico ya?"* |
| *"Exponer algo público, datos de clientes"* | *"esto está a la vista y cualquiera podría llamarlo"* |
| *"Automatizar vs hacerlo a mano"* | *"quiero montar el flujo que avisa solo"* |
| *"Qué medir, si algo funcionó"* | *"no tengo ni idea de si entra alguien"* |

**Quien ya sabe decir *"unit economics"* ya sabe a quién llamar.** La tabla enruta bien a
quien no la necesita.

---

## 3. Enrutado de las 3 skills

| Skill | Quién la activa | Puntos de entrada | Riesgo |
|---|---|--:|---|
| `shape-up-cycle` | `scrum-master`, `/bet`, `/hill`, `/ship` | **4** | 🟢 Bien enrutada |
| `decision-framing` | `ceo-bezos`, `pm-producto`, `/crew` | **3** | 🟢 Bien enrutada |
| `design-direction` | **`director-arte` y nadie más** | **1** | 🔴 **Punto único de fallo** |

`design-direction` solo es alcanzable a través de `director-arte`. Y `director-arte`
obtiene **0.041** ante su propia consulta insignia (*"se ve soso, parece igual que
cualquier otra web"*), donde gana `legal-basico` con 0.191.

> **La skill mejor escrita sobre dirección de arte es inalcanzable en la práctica**, porque
> su única puerta no se abre. Y encima el agente que la custodia es el que más la duplica
> (H1: 0.628, la similitud más alta del corpus).

---

## 4. CAPABILITY EXISTS / NO RELIABLE ROUTE

Las seis capacidades con score **0.000** ante su escenario:

| Capacidad | Escenario | Quién gana en su lugar | Diagnóstico |
|---|---|---|---|
| `cfo-precios` | *"no sé cuánto pedir ni si me sale a cuenta"* | `/hill` (0.251) | 🔴 **El caso más claro.** Consulta insignia, cero solape |
| `seguridad` | *"el enlace está a la vista y cualquiera podría llamarlo"* | `/bet` (0.247) | 🔴 Descrito sin jerga = invisible |
| `qa-bach` | *"los tests pasan, ¿publico?"* | `ventas-ross` (0.190) | 🔴 *"publicar"* activa al de ventas |
| `dev-dhh` | *"datos de varios clientes sin que se vean"* | `seguridad` (0.271) | 🟡 Discutible: `seguridad` es defendible |
| `coo-graham` | *"montar el flujo que avisa y reintenta"* | `seguridad` (0.172) | 🟡 **Hueco conocido:** nadie posee automatización |
| `pm-producto` | *"mensajería, reservas y llamadas a la vez"* | `scrum-master` (0.220) | 🔴 Gana en C04 (0.348) y desaparece en C10 |

### `analista-datos` — la pregunta directa

> **¿Es realmente difícil de alcanzar?** **Sí, y con número.**

Ante *"tengo la web publicada y no tengo ni idea de si entra alguien ni de si sirve para
algo"* obtiene **0.028** y queda fuera del top-3. Ganan `scrum-master` (0.207),
`pm-producto` (0.120) y `legal-basico` (0.111).

Su descripción dice *"decidir QUÉ medir"*, *"métricas de vanidad"*, *"instrumentación
mínima"*. La consulta dice *"entra alguien"*, *"sirve para algo"*. **Cero palabras en
común.**

Esto explica con datos el episodio ya citado: entregas repetidas sin analítica con el agente
correcto instalado. **No fue descuido: fue que la capacidad no era alcanzable desde el
lenguaje del problema.**

Y no es inalcanzable del todo (0.028 > 0), lo que lo hace peor que un fallo limpio: es
alcanzable en teoría e invisible en la práctica.

---

## 5. Ruido: quién gana cuando no debería

| Capacidad | Veces en top-1 sin ser la esperada | Por qué |
|---|--:|---|
| `scrum-master` | **3** (C01, C10, C11*) | Genericidad 71.1. Su descripción cubre *"no sepas por dónde seguir"*, que encaja con casi cualquier duda |
| `seguridad` | 2 (C05, C06) | *"datos de clientes"* y *"exponer"* son palabras frecuentes |
| `/bet` · `/hill` | 2 (C02, C03) | 🔴 **Comandos ganando consultas de dominio.** Ver abajo |
| `legal-basico` | 1 (C12) | Probable artefacto: *"condiciones"*, *"web"* |
| `ventas-ross` | 1 (C08) | *"publicar"* |

\* En C11 `scrum-master` es la esperada y acierta.

### El hallazgo que no había previsto: los comandos compiten con los agentes

`/bet` gana una consulta de **seguridad** y `/hill` gana una de **precios**. Ninguno tiene
nada que ver.

Ocurre porque las descripciones de comando son **cortas** (11–18 palabras útiles frente a
21–33 de los agentes), así que la normalización L2 concentra todo el peso en pocos
términos. Cualquier coincidencia parcial produce un coseno alto.

**Es en parte un artefacto del método** —y así se anota— pero apunta a algo real: los
comandos y los agentes viven en el mismo espacio de enrutado y **no hay nada que impida a
un comando de ciclo capturar una consulta de dominio**. Es un argumento a favor de separar
el enrutado en dos etapas (primero *tipo de intención*, después *capacidad*).

---

## 6. El techo de 3 capacidades

De la política *minimum necessary crew*: 12 casos con máximo 3 candidatas.

| | |
|---|--:|
| Casos con >3 candidatas reales | **0** |
| Casos con exactamente 3 | 5 |
| Casos con 2 | 3 |
| Casos con 1 | 4 |

**El techo no se viola nunca**, pero por el motivo equivocado: no porque haya disciplina,
sino porque **muy pocas capacidades puntúan por encima de cero**. Un embudo estrecho por
pobreza de vocabulario no es lo mismo que uno estrecho por criterio.

---

## 7. Qué cambiar en la Fase 1 — basado en datos

Ordenado por evidencia, no por intuición. **Nada de esto se ejecuta ahora.**

### 🔴 Prioridad 1 — Reescribir descripciones con el lenguaje del problema

**Evidencia:** `UNREACHABLE = 50 %`. Seis capacidades con score 0 ante su propio escenario.

La regla: **toda descripción debe contener las palabras que usaría alguien que tiene el
problema y no sabe a quién llamar.**

| Capacidad | Vocabulario que falta |
|---|---|
| `cfo-precios` | *cuánto cobrar · cuánto pedir · si sale a cuenta · si compensa · presupuesto* |
| `qa-bach` | *antes de publicar · antes de lanzar · se rompió otra vez · qué puede fallar* |
| `seguridad` | *está a la vista · cualquiera podría · se me ha colado · expuesto* |
| `analista-datos` | *si entra alguien · si sirve para algo · si funcionó · no sé si va bien* |
| `director-arte` | *se ve soso · parece igual que todas · genérico · no sé qué le falta* |
| `coo-graham` | *montar el flujo · hacerlo solo · dejar de hacerlo a mano* |

**Método, tomado de `agent-skills`: se arregla la descripción, no el prompt.**
**Coste:** una línea por archivo. **Sin tocar el cuerpo de ningún agente.**

### 🔴 Prioridad 2 — Quitar las frases comodín

**Evidencia:** 10 unidades con genericidad >50; las 4 primeras >70. *"Sirve para cualquier
tipo de producto"* en 8 descripciones.

No causan colisión —eso lo aprendí al equivocarme— pero **gastan entre el 15 % y el 25 % de
una descripción en palabras que no distinguen nada**, y ese espacio es justo el que
necesita la prioridad 1.

### 🟠 Prioridad 3 — Resolver H1 (`director-arte` ↔ `design-direction`)

**Evidencia:** 0.628, la más alta del corpus, con `desc` > `full` — firma de bug de
descripción. Y `design-direction` tiene **un único punto de entrada**, que además es ese
agente.

### 🟠 Prioridad 4 — `cfo-precios` no declara fronteras

**Evidencia:** único agente de 18 sin sección de derivación. Tiene *"Límites"* sobre
asesoramiento fiscal, pero no dice a quién deriva.

### 🟡 Prioridad 5 — Separar el enrutado de comando y de agente

**Evidencia:** `/bet` gana una consulta de seguridad, `/hill` una de precios.
Parcialmente artefacto del método; merece confirmarse antes de actuar.

### ⚪ Lo que los datos dicen que NO hay que hacer

| No hacer | Por qué |
|---|---|
| **Fusionar agentes por colisión** | **Cero colisiones ≥0.75.** Media entre agentes: 0.045. La hipótesis de que 18 agentes se pisan **queda refutada** |
| **Retirar `ceo-bezos` o `analista-thompson` por genericidad** | Son de los **menos** genéricos (33.9 y **14.6**, el mínimo). Si se retiran algún día, será por uso, nunca por esto |
| **Tocar `dev-dhh` ↔ `devops-hightower` o `ux-norman` ↔ `ui-duarte`** | H4 y H5 confirmadas. Sus fronteras funcionan |
| **Reescribir la tabla de `scrum-master`** | Cobertura del 94 %. El problema son los triggers, no la tabla |

---

## 8. Qué medir después de la Fase 1

Mismo script, mismo corpus, mismos 12 casos:

| Métrica | Baseline | Objetivo Fase 1 |
|---|--:|--:|
| **UNREACHABLE CAPABILITY** | **50 %** | **≤15 %** ← la que importa |
| TOP-3 COVERAGE | 33 % | ≥65 % |
| TOP-1 CORRECT | 25 % | ≥50 % |
| AMBIGUOUS ROUTE | 33 % | ≤25 % |
| Unidades con genericidad >50 | 10 | ≤3 |
| Colisiones ≥0.75 | 0 | **0** (no empeorar) |
| Avisos ≥0.50 | 1 | 0 |
| Agentes sin fronteras | 1 | 0 |

**Y la regla, escrita ahora que no hay presión:** si tras la Fase 1 `UNREACHABLE` no baja,
la hipótesis *"el problema son las descripciones"* queda refutada y hay que buscar en otro
sitio — **no ajustar los umbrales ni reescribir los casos para que salgan mejor.**

---

## 9. Resultado de la Fase 1 — qué se cumplió de §7

> Añadido el **2026-09-14**. Informe completo en [`phase1-report.md`](phase1-report.md).

| Propuesta de §7 | Estado | Evidencia |
|---|:--:|---|
| **P1 · Descripciones con lenguaje del problema** | ✅ Hecho, 18/18 | UNREACHABLE 50 % → **8 %** |
| **P2 · Quitar frases comodín** | ✅ Hecho | 24 → **0**. Genericidad media 44.5 → 31.3; unidades >50: 12 → **1** |
| **P3 · Resolver H1** | ✅ Hecho | 0.628 → **0.286**, sin perder el rol del agente |
| **P4 · `cfo-precios` sin fronteras** | ✅ Hecho | 0 agentes sin sección de derivación |
| **P5 · Separar enrutado de comando y de agente** | ✅ Hecho | Comandos en top-1 de consulta de dominio: 2/12 → **0/12** |

### Lo que §7 dijo que NO había que hacer — y se respetó

Cero agentes fusionados, cero retirados. `dev-dhh` ↔ `devops-hightower` y `ux-norman` ↔
`ui-duarte` siguen separados (H4 y H5 confirmadas). La tabla de `scrum-master` no se
reescribió: **se movió** a `rules/orchestration.md`, donde sí puede ejecutarse.

### Lo que §7 no vio, y el holdout sí

**Las 3 skills son ahora el suelo de ruido.** `decision-framing` gana una consulta de
seguridad; `shape-up-cycle` una de analítica. No eran genéricas antes — lo son **en
relativo**, porque agentes y comandos se afilaron y ellas no.

No estaba en el alcance de la Fase 1 y **no se ha tocado**. Es la propuesta nº 1 de la
Fase 2.

### Objetivos de §8, medidos

| Métrica | Baseline | Objetivo | Fase 1 | |
|---|--:|--:|--:|:--:|
| UNREACHABLE | 50 % | ≤15 % | **8 %** | ✅ |
| TOP-3 | 33 % | ≥65 % | **83 %** | ✅ |
| TOP-1 | 25 % | ≥50 % | **83 %*** | ✅ |
| AMBIGUOUS | 33 % | ≤25 % | **25 %** | ✅ |
| Genericidad >50 | 10** | ≤3 | **1** | ✅ |
| Colisiones ≥0.75 | 0 | 0 | **0** | ✅ |
| Avisos ≥0.50 | 1 | 0 | **0** | ✅ |
| Agentes sin fronteras | 1 | 0 | **0** | ✅ |

\* Parcialmente circular. El holdout con vocabulario distinto da **38 %**.
\*\* §7 contó 10 sobre los agentes; el recuento sobre las 25 unidades es 12.

**Los ocho objetivos se cumplen.** Y la regla que escribí antes de medir —*"si UNREACHABLE
no baja, la hipótesis queda refutada"*— no llegó a activarse: bajó 42 puntos.
