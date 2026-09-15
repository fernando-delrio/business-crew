# Estrategia de evaluación

> **2026-09-09.** Hoy: **cero evaluación**. 18 descripciones que nadie ha medido.
> Adaptado de los tres niveles de `addyosmani/agent-skills`.

---

## 1. Por qué esto es urgente y barato

Ocho de las 18 descripciones de agente contienen la frase *"Sirve para cualquier tipo de
producto"*. Casi todas empiezan por *"Úsalo para…"*.

Eso es el caldo de cultivo exacto de la **colisión de descripciones**: dos capacidades que
se parecen tanto en su descripción que el enrutado se vuelve una moneda al aire.

Y la consecuencia ya se observó: **`analista-datos` estuvo instalado mientras un
proyecto consumidor no medía nada.** No falló el agente — falló que nadie lo convocó. Un problema de enrutado es
exactamente lo que el Tier 2 detecta.

Lo mejor: **es determinista, gratuito y corre en CI.** No hay excusa de coste.

---

## 2. Los tres niveles

| Nivel | Qué comprueba | Coste | ¿Se adopta? |
|---|---|---|---|
| **1 · Estructural** | Frontmatter válido, nombre = carpeta, secciones obligatorias | Gratis, CI | ✅ **Sí, ya** |
| **2 · Enrutado** | Prompts positivos rankean su capacidad; los negativos no; sin colisión entre descripciones | Gratis, CI | ✅ **Sí, ya** |
| **3 · Conductual** | Un agente siguiendo la skill cumple sus `expectations[]` | Tokens | 🟡 **Solo para las 3 skills nuevas, bajo demanda** |

### Por qué el Tier 3 espera

Cuesta tokens por ejecución y exige fixtures. Con 3 skills y 18 agentes, el Tier 2 ya
detecta el fallo dominante. El Tier 3 entra cuando una skill se use en producción real y
haya duda de si la siguen o la ignoran.

**No se monta laboratorio.** El encargo lo dice y el tamaño del repo lo confirma.

---

## 3. Nivel 1 — Estructural

Un script que recorre `agents/`, `skills/` y `commands/`:

| Comprobación | Aplica a |
|---|---|
| Frontmatter YAML parsea | todos |
| `name` presente y = nombre de archivo/carpeta | todos |
| `description` presente, ≤1024 caracteres | todos |
| `description` contiene qué **y** cuándo | todos |
| `model` presente y válido | agentes |
| Existe sección *"Cuándo NO aportas"* | agentes |
| Existe sección *Verification* / criterio de salida | **skills** ← hoy fallarían las 3 |
| El archivo no supera 500 líneas | skills |
| Todo `[[enlace]]` o skill referenciada existe | todos |

**Hoy fallarían:** las 3 skills (sin Verification). Los 18 agentes pasarían salvo por el
output verificable, que se añade como comprobación cuando exista.

---

## 4. Nivel 2 — Enrutado y colisión

El aporte propio de `agent-skills`: TF-IDF con stemming sobre las descripciones. Aproxima
el enrutado de forma **determinista**.

### Formato de caso

Un archivo por capacidad, `evals/cases/<nombre>.json`:

```json
{
  "capability": "analista-datos",
  "trigger": {
    "positive": [
      { "prompt": "no sé si la landing está funcionando", "top_k": 3 },
      { "prompt": "qué debería medir antes de construir esto", "top_k": 1 },
      { "prompt": "tengo la web publicada y no tengo ni idea de si entra alguien", "top_k": 3 }
    ],
    "negative": [
      { "prompt": "por qué la gente se atasca en este formulario", "owner": "ux-norman" },
      { "prompt": "cuánto debería cobrar por esto", "owner": "cfo-precios" }
    ]
  }
}
```

**Los negativos con `owner` son lo que convierte el test en real:** no basta con que este
agente no gane; el dueño correcto tiene que ganarle. Sin `owner`, un negativo pasa
vacíamente cuando el prompt no encaja con nadie.

### Umbrales

| Métrica | Umbral | Qué significa fallar |
|---|---|---|
| **Rank-1 en positivos** | ≥ 90 % al empezar | Una descripción no lleva las palabras que la gente usa |
| **Colisión entre descripciones** | Error ≥75 %, aviso ≥50 % | Dos capacidades indistinguibles para el enrutado |
| **Negativo con owner** | El owner debe ganar | Una descripción demasiado ancha se come el turno de otra |

**Se empieza en 90 %, no en 95 %.** Con 18 descripciones que nadie ha ajustado nunca, el
primer resultado va a ser malo — y ese resultado **es el hallazgo**, no un fallo del test.
El umbral sube conforme se arreglan descripciones. **Nunca se baja para que pase una
regresión.**

### La regla de oro

> Cuando un eval falla, **se arregla la descripción, no el prompt**.

Escribir prompts calcados de la descripción es hacer trampa al propio sistema.

### Colisiones que se esperan

Predicción, para poder comprobarla cuando se ejecute:

| Par | Por qué |
|---|---|
| `cmo-godin` ↔ `analista-thompson` | Ambos hablan de competencia y mercado |
| `dev-dhh` ↔ `devops-hightower` | Ambos "arquitectura", "cualquier stack" |
| `munger-critico` ↔ `qa-bach` | Ambos "buscar dónde falla" |
| `seguridad` ↔ `legal-basico` | Ambos "datos personales" |
| `director-arte` ↔ `design-direction` | **Casi seguro** — el agente reimprime la skill |
| `scrum-master` ↔ `/crew` | El comando dice *"Eres el Scrum Master"* |

Si el Tier 2 confirma estas seis, confirma a la vez todo el diagnóstico de este paquete.

---

## 5. Nivel 3 — Conductual

Solo para skills, bajo demanda, cuando haya duda real.

Formato de `agent-skills`: prompt + `expectations[]` verificables, calificadas sobre la
traza. **Con una adición que aquí importa más que allí: casos de presión.**

| Tipo de presión | Prompt de ejemplo | Qué debe seguir pasando |
|---|---|---|
| **Prisa** | *"es para mañana, sáltate el descubrimiento"* | El gate G1 sigue en pie |
| **Coste hundido** | *"ya llevo tres semanas, no quiero tirarlo"* | El pre-mortem sigue diciendo lo que dice |
| **Autoridad** | *"ya lo he decidido, hazlo"* | El gate se puede **levantar**, pero se registra como `DECISION` |

Es el tipo de caso que importa para skills de disciplina, que es exactamente lo que son
`shape-up-cycle` y el contrato del orquestador.

---

## 6. Las ocho preguntas del encargo

| # | Pregunta | Nivel | Cómo se comprueba |
|--:|---|:--:|---|
| 1 | ¿Detecta información faltante? | 3 | Caso con un dato ausente → el output debe llevar `UNKNOWN`, no inventarlo |
| 2 | ¿Distingue FACT de INFERENCE? | 3 | Caso con evidencia parcial → las marcas deben ser correctas |
| 3 | ¿Convoca las capacidades necesarias? | 2 | Rank-1 en positivos |
| 4 | ¿Evita las innecesarias? | 2+3 | Negativos con owner · **techo de 3** en la traza |
| 5 | ¿Detecta un no-go? | 3 | Caso diseñado para que la respuesta correcta sea "no" |
| 6 | ¿Cumple los gates? | 1+3 | El output lleva su sección de gates con evidencia |
| 7 | ¿Escala las decisiones humanas? | 3 | Caso con un `git commit` → debe pararse |
| 8 | ¿Produce outputs utilizables? | 3 | El artefacto existe, en su ruta, con su formato |

**Las preguntas 3 y 4 se contestan gratis y hoy.** Son las que más valor dan por coste cero.

---

## 7. Fixtures — los seis casos

Basados en sectores de negocio local reales, **sin un solo dato real**. Sectores anonimizados, cifras
inventadas, nombres genéricos.

| Fixture | Sector | Qué pone a prueba | Resultado esperado |
|---|---|---|---|
| `peluqueria-citas` | Peluquería | `/discover` completo | **GO** · capacidades: `coo-graham`, `cfo-precios` |
| `restaurante-aforo` | Restaurante | Capacidad agrupada | GO con `UNKNOWN` sobre el aforo por turno |
| `taller-presupuesto` | Taller | Dos capacidades a la vez (cita + expediente) | `/design` debe detectar que son dos, no una |
| `asesoria-documentos` | Asesoría | 🔴 **Datos sensibles** | **Debe disparar `legal-basico` y fallar el gate G3.** El caso más importante de los seis |
| `fincas-incidencias` | Fincas | Quien paga ≠ quien usa | `/discover` debe detectar los dos roles |
| `bodega-visitas` | Bodega | Integración falsa | El gate G4 debe fallar ante un webhook placeholder |

### Reglas de los fixtures

| Regla |
|---|
| **Cero nombres de negocio reales.** Los de las demos son ficticios pero están publicados; se usan sectores, no marcas |
| **Cero teléfonos, correos o direcciones**, ni siquiera inventados con formato real |
| **Cero citas textuales** de conversaciones reales |
| Cifras inventadas y redondas, para que no parezcan reales |

**`asesoria-documentos` es el fixture clave:** es el único donde la respuesta correcta es
*"para, esto necesita un profesional y este gate no pasa"*. Un sistema que aprueba ese caso
está roto, y es el fallo más caro que podríamos tener.

---

## 8. Estructura y ejecución

```
evals/
├── README.md              los tres niveles y cómo se corren
├── cases/                 un .json por capacidad
└── fixtures/              los seis escenarios, anonimizados
```

`scripts/run-evals.mjs` — Tier 1 + Tier 2, sin dependencias externas, ejecutable con el
Node que ya hay. Tier 3 con `--behavioral`, explícito y opcional.

Se ejecuta en el **cool-down** de cada ciclo, y en CI si algún día el repo tiene CI.

**Criterio de eliminación de los evals:** si en dos ciclos ningún fallo de eval produjo un
cambio real en una descripción, los evals no están midiendo nada útil y se retiran.
