# Baseline Tier 2 — colisión y genericidad

> **2026-09-09.** Medición, no opinión. Reproducible con
> `python evals/tier2_similarity.py`.
> **Nada del repositorio se ha modificado.** Este es el estado **antes** de v0.2.

---

> ⚠️ **Este documento es el registro del BASELINE — el estado ANTES de la Fase 1.**
> Sus números se conservan intactos a propósito: son el punto de comparación.
> Los resultados posteriores están en [`phase1-report.md`](phase1-report.md).
>
> **Resumen del cambio:** UNREACHABLE 50 % → 8 % · TOP-1 25 % → 83 % · comodines 24 → 0 ·
> avisos ≥0.50 1 → 0. Con una regresión (UNNECESSARY 8 % → 25 %) y un aviso de
> circularidad: un holdout con vocabulario distinto da **38 %** de TOP-1, no 83 %.


## 1. Anti-bloat gate sobre `evals/`

Se comprueba antes de crear el directorio, como exige el propio protocolo.

| Pregunta | Respuesta |
|---|---|
| ¿Resuelve un problema observado? | ✅ Sí. `analista-datos` existía y nunca se convocó. No había forma de saber si era un caso aislado |
| ¿Existe ya algo que lo resuelva? | ❌ Cero evaluación en el repo |
| ¿Puede ser una sección de otro archivo? | ❌ Contiene **código ejecutable** y **fixtures**. No cabe en un `.md` |
| ¿Se usará en ≥2 casos? | ✅ 25 unidades × 2 espacios + 12 casos de enrutado. Y se reejecuta en cada cambio de agente o skill |
| ¿Tiene owner? | ✅ Se ejecuta en el cool-down |
| ¿Tiene criterio de eliminación? | ✅ Si en 2 ciclos ningún fallo produce un cambio real en una descripción |

**Supera el gate.** Se crea `evals/` con contenido real: un script, un fixture y un volcado.

---

## 2. Metodología

### 2.1 Qué texto entra

Comparar archivos enteros mide el **estilo de la plantilla**, no la capacidad: los 18
agentes comparten encabezados, tono y estructura, así que todos se parecerían a todos.

| Campo | Fuente | Por qué entra |
|---|---|---|
| `name` | frontmatter o nombre de archivo | Forma parte del enrutado |
| `description` | frontmatter (+ `argument-hint` en comandos) | **Es lo que el harness usa para enrutar** |
| `mission` | primer párrafo tras el frontmatter | Declara la responsabilidad |
| `boundaries` | *"Cuándo NO aportas"* / *"Tus límites"* | Declara ownership por exclusión |

| Excluido | Por qué |
|---|---|
| *"Contexto — siempre antes de responder"* | Boilerplate: está en los 18. Ruido puro |
| *"Ajuste por tipo de producto"* | Estructura repetida en 15 de 18 |
| Tablas, bloques de código, ejemplos | Miden el vocabulario del ejemplo, no el de la capacidad |
| Sintaxis markdown | Ruido |

### 2.2 Dos espacios, y por qué la diferencia es el hallazgo

```
desc  = name + description                          ← lo que decide el enrutado HOY
full  = name + description + mission + boundaries   ← la huella semántica real
```

| Patrón | Significa | Coste de arreglo |
|---|---|---|
| `desc` alto + `full` bajo | Capacidades distintas con descripciones que chocan | **Barato** — reescribir una descripción |
| `desc` alto + `full` alto | Se solapan de verdad | **Caro** — fusionar o redefinir |
| `desc` bajo + `full` alto | Contenido solapado que el enrutado no ve | Revisión manual |

### 2.3 Técnica

TF-IDF con `tf` sublineal (`1+log`), `idf` suavizado, normalización L2, similitud coseno.
Español: sin tildes, minúsculas, lista de palabras vacías, stemmer de sufijos conservador
(nunca deja menos de 4 caracteres).

**Se conservan a propósito `no`, `nunca` y `sin`**: en las secciones de frontera son
portadoras de significado (*"Cuándo **NO** aportas"*).

Sin dependencias, sin red, sin LLM. **Un evaluador que necesita tokens no se ejecuta, y uno
que no se ejecuta no mide nada.**

### 2.4 Umbrales

Tomados de `agent-skills`: **error ≥0.75**, **aviso ≥0.50**. No se han ajustado para que
los resultados encajen con ninguna predicción.

### 2.5 Dos bugs del evaluador, corregidos durante la ejecución

Se documentan porque afectaban a los resultados:

| Bug | Efecto | Corrección |
|---|---|---|
| Se limpiaba el markdown **antes** de partir secciones, borrando los `##` | `boundaries` vacío en las 18 → el espacio `full` era solo name+description | Partir secciones primero |
| Una puntuación de 0.000 rellenaba el top-3 | Marcaba como *"prohibida en top-3"* a capacidades que no competían por nada. Inflaba `UNNECESSARY CAPABILITY` de 8 % a 17 % | Score 0 no es un enrutado: es ausencia |

---

## 3. Corpus

**25 unidades:** 18 agentes · 3 skills · 4 comandos.

**Hallazgo estructural:** 17 de 18 agentes declaran fronteras. **`cfo-precios` no tiene
sección de fronteras** — tiene *"Límites"* sobre asesoramiento fiscal, pero no declara a
quién deriva. Es el único.

---

## 4. Top 12 de colisiones

| # | A | B | DESC | FULL | Tipo | Interpretación |
|--:|---|---|---:|---:|---|---|
| 1 | `director-arte` | `design-direction` | **0.628** ⚠ | 0.431 | agent↔skill | **Aviso.** El agente reimprime su skill |
| 2 | `shape-up-cycle` | `/hill` | 0.374 | 0.327 | skill↔command | Legítimo: el comando ejecuta la skill |
| 3 | `ui-duarte` | `ux-norman` | 0.207 | 0.254 | agent↔agent | **El máximo entre agentes** |
| 4 | `analista-datos` | `pm-producto` | 0.181 | 0.144 | agent↔agent | Bajo |
| 5 | `/bet` | `/ship` | 0.162 | 0.282 | command↔command | Legítimo: extremos del mismo ciclo |
| 6 | `devops-hightower` | `qa-bach` | 0.159 | 0.144 | agent↔agent | Bajo |
| 7 | `shape-up-cycle` | `/bet` | 0.154 | 0.202 | skill↔command | Legítimo |
| 8 | `devops-hightower` | `seguridad` | 0.148 | 0.109 | agent↔agent | Bajo |
| 9 | `cfo-precios` | `ventas-ross` | 0.143 | 0.091 | agent↔agent | Bajo |
| 10 | `dev-dhh` | `devops-hightower` | 0.137 | 0.095 | agent↔agent | Bajo |
| 11 | `/crew` | `/hill` | 0.134 | 0.072 | command↔command | Bajo |
| 12 | `analista-datos` | `scrum-master` | 0.123 | 0.072 | agent↔agent | Bajo |

### Recuento

| | |
|---|--:|
| Colisiones ≥0.75 (error) | **0** |
| Avisos ≥0.50 | **1** |
| Pares evaluados | 300 |

### Media por tipo de par

| Tipo | n | Media | Máx |
|---|--:|--:|--:|
| agent ↔ agent | 153 | **0.045** | 0.207 |
| agent ↔ skill | 54 | 0.034 | **0.628** |
| agent ↔ command | 72 | 0.014 | 0.100 |
| command ↔ command | 6 | 0.077 | 0.162 |
| command ↔ skill | 12 | 0.086 | 0.374 |
| skill ↔ skill | 3 | 0.031 | 0.065 |

---

## 5. El resultado que me obliga a corregir el diagnóstico

En la fase anterior escribí una predicción y me comprometí a revisarla si fallaba:

> *"Predicción comprobable: encontrará colisión alta entre `director-arte` ↔
> `design-direction` y entre `scrum-master` ↔ `/crew`. […] Si no la encuentra, hay que
> revisar el diagnóstico."*

**Falló la mitad, y la parte más general falló entera.**

| Predicción | Resultado |
|---|---|
| `director-arte` ↔ `design-direction` alta | ✅ 0.628 — la más alta del corpus |
| `scrum-master` ↔ `/crew` alta | ❌ **0.061.** Casi el mínimo posible |
| *"8 de 18 descripciones genéricas → colisión probable"* | ❌ **Cero colisiones ≥0.75.** Media entre agentes: 0.045 |

### Qué aprendo de que fallara

**1. Los 18 agentes están léxicamente mucho más diferenciados de lo que supuse.** Media de
0.045 y máximo de 0.207 entre agentes. La afirmación *"con 18 descripciones que empiezan
por «Úsalo para…» el enrutado es una moneda al aire"* **era falsa** y la retiro.

**2. El TF-IDF explica por qué me equivoqué, y el mecanismo importa.** *"Sirve para
cualquier tipo de producto"* aparece en 8 descripciones, así que su IDF es **bajo**: el
método lo descuenta casi por completo. La frase comodín **no produce colisión** — produce
algo distinto y peor, que aparece en §7.

**3. La duplicación funcional no es lo mismo que la colisión de descripciones.**
`/crew` dice literalmente *"Eres el Scrum Master convocando al equipo"*: la duplicación es
real y está en el **cuerpo**. Sus descripciones apenas comparten *"equipo"*.

> **Corrección al diagnóstico de v0.2:** el Tier 2 mide **colisión de descripciones**. No
> detecta duplicación funcional en el cuerpo. Son dos defectos distintos y hacen falta dos
> métodos. Presentar el Tier 2 como el detector de *"nuestro fallo dominante"* era
> incorrecto: detecta **un** fallo, y no el que yo esperaba.

---

## 6. Hipótesis H1–H5

| # | Par | DESC | FULL | Esperado | Veredicto |
|---|---|---:|---:|---|---|
| **H1** | `director-arte` ↔ `design-direction` | **0.628** | 0.431 | alta | ✅ **CONFIRMADA** |
| **H2** | `scrum-master` ↔ `/crew` | 0.061 | 0.164 | alta | ❌ **RECHAZADA** |
| **H3a** | `munger-critico` ↔ `qa-bach` | 0.083 | 0.080 | próximas pero diferenciadas | ✅ CONFIRMADA |
| **H3b** | `munger-critico` ↔ `seguridad` | 0.022 | 0.104 | idem | ✅ CONFIRMADA |
| **H3c** | `qa-bach` ↔ `seguridad` | 0.021 | 0.050 | idem | ✅ CONFIRMADA |
| **H4** | `dev-dhh` ↔ `devops-hightower` | 0.137 | 0.095 | baja | ✅ CONFIRMADA |
| **H5** | `ux-norman` ↔ `ui-duarte` | 0.207 | 0.254 | baja | ✅ CONFIRMADA |

**Sin tocar umbrales.** Notas por hipótesis:

- **H1 — confirmada, con matiz.** 0.628 es un **aviso**, no un error: no llega a 0.75. El
  hallazgo cualitativo es más fuerte que el número: `desc` (0.628) > `full` (0.431), es
  decir, **se parecen más en la descripción que en la sustancia**. Eso es la firma exacta
  de un *bug de descripción*, no de un solapamiento real — el agente reimprime la rúbrica
  de la skill en su descripción, pero sus misiones y fronteras sí difieren.
- **H2 — rechazada.** 0.061. Ver §5. La duplicación existe, en el cuerpo, y este método no
  la ve. `full` (0.164) > `desc` (0.061) apunta en esa dirección, pero no llega a ser
  evidencia.
- **H3 — confirmadas las tres.** Los tres agentes que *"buscan dónde falla"* están
  claramente diferenciados en descripción. Sus fronteras funcionan.
- **H4 y H5 — confirmadas.** `ux-norman` ↔ `ui-duarte` es el máximo entre agentes (0.207) y
  aun así está muy por debajo del aviso. Sus secciones *"Cuándo NO aportas"* se citan
  mutuamente, y funciona.

---

## 7. Genericidad — aquí sí está el problema

Tres señales combinadas: frases comodín (20 %), similitud media con todas las demás (50 %),
e IDF medio invertido (30 %). Escala 0–100.

| Unidad | GEN | Sim.med | IDF.med | Comodines |
|---|--:|--:|--:|---|
| `devops-hightower` | **75.1** | 0.056 | 2.76 | *cualquier tipo de producto · cualquier stack* |
| `pm-producto` | **71.5** | 0.053 | 2.88 | *cualquier tipo de producto* |
| `scrum-master` | **71.1** | 0.054 | 2.97 | *cualquier tipo de producto* |
| `dev-dhh` | **70.5** | 0.052 | 2.87 | *cualquier tipo de producto · cualquier stack* |
| `analista-datos` | 63.9 | 0.046 | 2.96 | *cualquier tipo de producto* |
| `qa-bach` | 62.7 | 0.045 | 3.01 | *cualquier tipo de producto* |
| `ux-norman` | 60.9 | 0.044 | 3.08 | *cualquier tipo de producto* |
| `ui-duarte` | 54.9 | 0.038 | 3.16 | *cualquier tipo de producto* |
| `director-arte` | 53.1 | 0.056 | 2.96 | — |
| `coo-graham` · `cmo-godin` | ~51 | 0.033 | 3.13 | *cualquier tipo de producto* |
| `shape-up-cycle` | 50.7 | 0.055 | 3.14 | — |
| `seguridad` | 47.6 | 0.030 | 3.19 | *cualquier stack* |
| … | | | | |
| `legal-basico` | 18.9 | 0.021 | 3.33 | — |
| `analista-thompson` | **14.6** | 0.016 | 3.33 | — |

**Diez unidades por encima de 50.** Las cuatro primeras superan 70.

### El mecanismo, que no es el que yo suponía

La frase comodín **no hace que dos agentes colisionen entre sí**. Hace algo peor:

> **Gasta el presupuesto de la descripción en palabras que no distinguen nada.**

Una descripción tiene entre 20 y 35 palabras útiles. Si cinco se van en *"Sirve para
cualquier tipo de producto"*, quedan menos para las palabras que un usuario diría de
verdad. El resultado no es que el agente compita con otro: es que **no compite con nadie**,
porque no contiene el vocabulario de la consulta.

Eso es exactamente lo que mide §8, y es lo que le pasó a `analista-datos`.

---

## 8. Casos de enrutado — 12 escenarios

Consultas escritas parafraseando cómo habla un usuario, **nunca copiadas de las
descripciones** (esa es la regla de `agent-skills`: copiarlas sería hacer trampa).

| Caso | Esperado | Score esperado | Top-1 real | ¿OK? |
|---|---|--:|---|:--:|
| C01 *"no sé si entra alguien en la web"* | `analista-datos` | 0.028 | `scrum-master` (0.207) | ❌ |
| C02 *"el enlace del formulario está a la vista"* | `seguridad` | **0.000** | `/bet` (0.247) | ❌ |
| C03 *"no sé cuánto pedir"* | `cfo-precios` | **0.000** | `/hill` (0.251) | ❌ |
| C04 *"añadir algo que nadie ha pedido"* | `pm-producto` | 0.348 | `pm-producto` | ✅ |
| C05 *"montar el flujo que avisa y reintenta"* | `coo-graham` | **0.000** | `seguridad` (0.172) | ❌ |
| C06 *"datos de varios clientes sin que se vean"* | `dev-dhh` | **0.000** | `seguridad` (0.271) | ❌ |
| C07 *"funciona pero la gente se atasca"* | `ux-norman` | 0.184 | `ux-norman` | ✅ |
| C08 *"tests pasan, ¿publico?"* | `qa-bach` | **0.000** | `ventas-ross` (0.190) | ❌ |
| C09 *"quién más hace esto en mi zona"* | `analista-thompson` | 0.129 | `cfo-precios` (0.161) | ~3 |
| C10 *"mensajería, reservas y llamadas a la vez"* | `pm-producto` | **0.000** | `scrum-master` (0.220) | ❌ |
| C11 *"vuelvo tras dos semanas"* | `scrum-master` | 0.195 | `scrum-master` | ✅ |
| C12 *"se ve soso, igual que cualquier otra"* | `director-arte` | 0.041 | `legal-basico` (0.191) | ❌ |

### Métricas baseline

| Métrica | Valor | |
|---|--:|---|
| **TOP-1 CORRECT** | **3/12 = 25 %** | La capacidad correcta gana |
| **TOP-3 COVERAGE** | **4/12 = 33 %** | Aparece entre las tres primeras |
| **UNNECESSARY CAPABILITY** | 1/12 = 8 % | Una prohibida entre las candidatas reales |
| **MISSING CAPABILITY** | 8/12 = 67 % | La esperada, fuera del top-3 |
| **AMBIGUOUS ROUTE** | 4/12 = 33 % | Margen <0.05 o líder <0.15 |
| **UNREACHABLE CAPABILITY** | **6/12 = 50 %** | **Score 0: cero vocabulario en común** |
| NO ROUTE AT ALL | 0/12 = 0 % | Siempre hay alguna candidata |

> **La métrica que importa es `UNREACHABLE`, no `TOP-1`.**
>
> `TOP-1 = 25 %` mide mi ranking léxico y **no debe leerse como "el sistema real acierta
> una de cada cuatro"**: el harness usa selección semántica, no TF-IDF.
>
> `UNREACHABLE = 50 %` mide una propiedad de las descripciones: **en la mitad de los
> escenarios, la capacidad correcta no comparte ni una palabra** con la forma natural de
> plantear el problema. Eso es cierto independientemente del método de ranking.

**Seis capacidades inalcanzables:** `seguridad`, `cfo-precios`, `coo-graham`, `dev-dhh`,
`qa-bach`, `pm-producto` (en C10).

**Y `cfo-precios` con 0.000 en *"no sé cuánto pedir por esto"* es el resultado más claro de
todos**: es su consulta insignia, no hay ninguna ambigüedad sobre quién debería ganar, y su
descripción no contiene ninguna de esas palabras. Habla de *"pricing basado en valor"*,
*"unit economics"* y *"rentable"*. Nadie que no sepa ya a quién llamar usaría esas palabras.

---

## 9. Limitaciones

Lo que este eval **no** demuestra:

| # | Limitación |
|---|---|
| 1 | **Es léxico, no semántico.** *"cobrar"* y *"pedir"* son sinónimos y para el método no se parecen en nada |
| 2 | **No es el enrutador real.** El harness usa un modelo. Estos números miden las **descripciones**, no el sistema en producción |
| 3 | **`TOP-1 = 25 %` no es la precisión del sistema.** Es el suelo de un método deliberadamente tonto |
| 4 | **12 casos son pocos.** Cada uno vale 8 puntos porcentuales |
| 5 | **Las consultas las escribí yo**, no salen de usuarios reales |
| 6 | **Los `expected_primary` son mi criterio.** C05 y C06 son discutibles: el dueño real está fuera del repo |
| 7 | **El stemmer es casero.** Conservador a propósito, pero puede fusionar o separar mal |
| 8 | **No detecta duplicación funcional en el cuerpo** — es lo que H2 demostró |
| 9 | **Corpus pequeño (25).** Los IDF son inestables: una palabra en 2 documentos pesa mucho |

**Para qué sirve, entonces:** como **línea base reproducible**. El mismo script, el mismo
corpus y los mismos 12 casos, ejecutados después de la Fase 1, dicen si las descripciones
mejoraron. **Las comparaciones relativas son válidas aunque los valores absolutos sean un
suelo.**

---

## 10. Reproducir

```bash
python evals/tier2_similarity.py                              # informe
python evals/tier2_similarity.py --json evals/results.json    # + volcado
python evals/tier2_similarity.py --top 30                     # más pares
```

Sin dependencias. Determinista: misma entrada, misma salida.
Volcado de esta ejecución: `evals/results-baseline.json`.
