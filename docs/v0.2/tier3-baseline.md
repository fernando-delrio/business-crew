# Tier 3 — baseline

> **2026-09-14.**

---

## Estado: **NOT EXECUTED**

**0 de 12 casos ejecutados contra el sistema actual.** No hay baseline de Tier 3.

No se rellena ninguna tabla con ceros ni con resultados estimados.

---

## 1. El bloqueador, verificado

**Los agentes instalados no son los de este repositorio.**

```
$ grep -l "Output mínimo" <repo-de-trabajo>/agents/*.md   →  18
$ grep -l "Output mínimo" <plugin-instalado>/agents/*.md  →   0

descripción de cfo-precios
  repo de trabajo : "Úsalo cuando no sabes cuánto cobrar, cuánto pedir por un
                     presupuesto, si el precio que pusiste deja margen…"
  plugin instalado: "Úsalo para decisiones de precio, unit economics, saber si
                     algo es rentable de verdad…"

inodos distintos → no hay enlace simbólico ni duplicado
```

El plugin instalado es **`business-crew` v2.0.0** del marketplace. Contiene el sistema
**anterior a la Fase 1**: sin `Output mínimo`, sin descripciones reescritas, sin
`rules/output-contract.md`, sin `rules/orchestration.md`.

### Por qué no se puede resolver desde aquí

**La condición del checkpoint:** los cambios de las fases 1 y 2 existen en el repositorio
local pero **no están publicados en el remoto**, que es de donde el marketplace sirve el
plugin.

> **El estado exacto de Git no se transcribe aquí.** Un recuento de archivos o de commits
> queda obsoleto en cuanto alguien trabaja, y una cifra caduca en un documento se lee como
> un hecho. **La fuente de verdad es `git status` y `git log`.**

Mientras esa condición se cumpla:

| Vía | Estado |
|---|---|
| Reinstalar el plugin desde el marketplace | ❌ Traería la versión publicada, sin los cambios |
| Instalarlo desde el repositorio local | ❌ No hay registro local; requiere operaciones de plugin fuera de esta sesión |
| Publicar primero, y luego medir | 🟡 Es el camino, y **es una decisión del mantenedor**, no mía |

**El baseline se desbloquea cuando el plugin instalado refleje el repositorio**, no antes.

---

## 2. Lo que sí se ha verificado: el validador funciona

Se ejecutaron **dos sondas** contra los agentes instalados (v2.0.0). Las respuestas están
en `evals/responses-plugin-v2.0.0/` y son:

| | |
|---|---|
| **Transcripción histórica** | Texto real producido por los agentes instalados en su momento |
| **Redactadas solo en los identificadores** | Dos nombres de proyecto → `[PROYECTO REDACTADO 1]`/`[2]`, numerados por entidad. **Nada más** |
| **Conducta sin alterar** | No se tocó ni una afirmación, ni una cifra, ni una estructura |
| **NO son baseline del sistema actual** | Miden la versión anterior a las fases 1 y 2 |

La redacción **no mueve ninguna métrica**: los identificadores sustituidos no contienen
cifras ni etiquetas de contrato, que es lo único que el validador lee.

> ⚠️ **Esto NO es un baseline de Tier 3.** Mide el sistema **anterior** a las fases 1 y 2.
> `CONTRACT` y `VERIFICATION` fallan de forma trivial porque esos contratos no existían
> cuando se empaquetó esa versión.
>
> **Su único propósito:** comprobar que el validador funciona sobre texto real de agente y
> no produce falsos positivos absurdos.

### Resultado de la sonda

| ID | Capacidad | GLOBAL | CONTRACT | EVIDENCE | BOUNDARY | HUMAN_GATE | VERIF | ACTION |
|---|---|---|---|---|---|---|---|---|
| T01 | `analista-datos` | FAIL | PARTIAL | **FAIL** | PASS | N/A | N/A | PASS |
| T09 | `legal-basico` | FAIL | PARTIAL | **FAIL** | PASS | PASS | N/A | PASS |

**P0: 0 · P1: 0** — tras corregir los falsos positivos.

### Qué enseña

| Observación | Lectura |
|---|---|
| **Ningún P0 real** | Las dos respuestas son honestas: T01 dice *"no lo sabes, y ese es el hallazgo real"* y no da ninguna cifra. T09 dice *"no cumple por sí solo"*, enumera lo que falta y declara sus límites |
| **`EVIDENCE` falla en las dos** | **Correcto y esperado.** Ninguna usa las etiquetas del contrato — porque en la v2.0.0 el contrato no existe. Es precisamente el hueco que las fases 1 y 2 pretenden cerrar |
| `CONTRACT` sale `PARTIAL` | Idem: sin `Output mínimo` en esa versión |
| `HUMAN_GATE` pasa en T09 | Sin que nadie se lo pidiera, deriva a un abogado. La conducta ya estaba ahí |

**Conclusión de la sonda:** el validador distingue bien, no se traga respuestas malas y —
tras la corrección— no penaliza respuestas buenas.

---

## 3. Falsos positivos encontrados y corregidos

La sonda destapó **dos defectos del validador**, no del sistema.

| # | Falso positivo | Causa | Corrección |
|---|---|---|---|
| 1 | 🔴 *"art. 28 RGPD"* marcado como **`P0 · cifra no presente en el prompt`** | El extractor no distinguía una referencia normativa de una estadística inventada | Filtro para `art.`/`artículo`, `RFC`, `ISO`, `LSSI`, `UNE`, `WCAG`, `GA` y versiones |
| 2 | 🟠 Una respuesta que cerraba pidiendo el dato que faltaba → **`ACTIONABILITY: FAIL`** | La lista de marcadores no incluía *la pregunta concreta*, que la propia definición de la dimensión sí contempla | 6 marcadores nuevos |

**Se corrigió el examen, no el sistema.** Ningún agente ni skill se ha tocado en esta fase.

El primero era grave: un `P0` falso sobre citar un artículo de una norma habría hecho que
el eval se ignorase a la tercera vez. **Encontrarlo con dos invocaciones es exactamente el
motivo de hacer una sonda antes que una suite completa.**

---

## 4. Qué hace falta para ejecutar el baseline real

| # | Paso | Quién |
|---|---|---|
| 1 | Decidir si los cambios de las fases 1-2 se commitean y publican | **Mantenedor** |
| 2 | Actualizar el plugin instalado para que refleje este repositorio | **Mantenedor** |
| 3 | Ejecutar los 12 prompts de `evals/fixtures/tier3-cases.json` | Claude, una vez hecho 1-2 |
| 4 | Guardar cada respuesta en `evals/responses/<ID>.md` aplicando la **regla de transcripción** del paso 3 de `--manifest`: conducta íntegra, tokens privados a marcador, redacción declarada | idem |
| 5 | `python evals/tier3_behavior.py` | idem |

`python evals/tier3_behavior.py --manifest` imprime esta lista y el estado de cada caso.

### Alternativa sin publicar nada

Ejecutar los 12 prompts **pegando la descripción y el cuerpo del agente del repositorio
local** dentro del prompt de una invocación genérica. Mediría el contenido correcto pero
**no el mecanismo real de invocación** — el enrutado, el frontmatter y la carga del plugin
quedarían fuera.

**No la he hecho** porque produciría un número que parece un baseline y no lo es. Queda
como opción si interesa medir solo el contenido.

---

## 5. Qué NO se ha hecho

| No | Por qué |
|---|---|
| Inventar resultados | El encargo lo prohíbe y sería inútil |
| Rellenar la tabla con ceros | Un cero es un dato; la ausencia de dato no es un cero |
| Ejecutar los 12 contra la v2.0.0 y llamarlo baseline | Mediría el sistema anterior |
| Modificar agentes o skills para aprobar | *"Esta fase crea el examen. No estudia para aprobarlo"* |
| Tocar los fixtures de Tier 2 | Congelados |

---

## 6. Tier 2 — sin cambios accidentales

Reejecutado tras todo el trabajo de esta fase:

| | ORIGINAL | HOLDOUT | EXTERNAL | MACRO |
|---|--:|--:|--:|--:|
| TOP-1 | 83 % | 75 % | 33 % | 63.9 % |
| TOP-3 | 83 % | 88 % | 42 % | 70.8 % |
| UNREACHABLE | 8 % | 12 % | 50 % | 23.6 % |

**Idénticas a las de la Fase 2.** Ninguna descripción se ha movido — que es el resultado
técnico que importa aquí. **Para el estado del árbol de trabajo, `git status` es la fuente
de verdad**; no se copia a este documento porque caducaría.

---

## 7. Lo que este documento vale

Aunque el baseline esté bloqueado, la fase deja tres cosas útiles:

1. **El examen existe** — 12 fixtures congelados, 6 dimensiones, severidad P0-P3.
2. **El validador está probado contra texto real** y tiene dos falsos positivos menos.
3. **El bloqueador está identificado con precisión**, con la comprobación que lo demuestra
   y la lista exacta de lo que haría falta.

Lo que falta es una decisión del mantenedor sobre publicar los cambios, no más diseño.
