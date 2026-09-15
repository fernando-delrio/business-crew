# Diseño de workflows

> **2026-09-09.** El encargo propone ocho. **Se proponen tres**, y se explica cada recorte.

---

## 1. El recorte

| # | Propuesto en el encargo | Decisión | Motivo |
|--:|---|---|---|
| 1 | DISCOVER | ✅ **`/discover`** | Se necesita hoy: ciclo de descubrimiento abierto sin guion |
| 2 | VALIDATE | 🔀 **Fusionado en `/discover`** | Con cero clientes, descubrir y validar son **la misma conversación**. Separarlos crea dos workflows que se invocan juntos siempre |
| 3 | DESIGN SOLUTION | ✅ **`/design`** | Se necesita cuando un cliente diga que sí |
| 4 | BUILD | ❌ **No se crea** | Ya existe y funciona: `superpowers:writing-plans`, `executing-plans`, `test-driven-development`, más el `CLAUDE.md` del proyecto. Duplicarlo sería competir con lo instalado |
| 5 | SHIP | ✅ **`/release`** ⚠️ renombrado | `/ship` **ya existe** y significa *cerrar el ciclo de Shape Up*. Colisión real |
| 6 | OPERATE | ⏸️ **Aplazado** | Cero clientes, cero incidentes, cero sistemas en operación. Disparador: el primer incidente real |
| 7 | LEARN | 🔀 **Fusionado en `/ship` + skill de promoción** | `/ship` ya hace retro. Lo que falta no es un workflow, es el protocolo de ascenso a skill |
| 8 | CLIENT DELIVERY | ⏸️ **Aplazado** | Es la concatenación de los otros tres más contrato y traspaso. Con cero clientes sería un guion de una obra que nadie ha representado |

**Ocho → tres nuevos.** Los cinco recortes no son pereza: cuatro se resuelven con algo que
ya existe, y dos no tienen ningún caso observado.

---

## 2. La regla de orquestación

Tomada de `agent-skills` y adaptada:

> **El orquestador es un comando. Los agentes no se invocan entre sí.**
> Un agente puede leer una skill. Un comando puede convocar agentes.
> El único patrón multi-agente permitido es **fan-out paralelo + síntesis**.

Esto no es preferencia estética: **un subagente no puede lanzar otro subagente**. Cualquier
diseño que dependa de cadenas de agentes no se puede ejecutar.

---

## 3. `/discover` — de un negocio a una decisión de go/no-go

**Cuándo:** antes de proponer nada a un negocio. **Es el workflow que hace falta esta
semana.**

```
INTENT: "voy a hablar con <negocio>"
   ↓
1 · PREPARAR
    · Sector y qué se sabe ya (fuente privada del proyecto)
    · Qué paga hoy por resolverlo (la comparativa de alternativas del sector)
    · La demo de SU sector, no la landing genérica
    · 7 preguntas del sector, no una presentación
   ↓
2 · ESCUCHAR  ← fuera del ordenador. Claude no participa
    · Cómo lo hace hoy, paso a paso
    · Qué le interrumpe un día normal
    · Si pudiera quitarse una sola cosa, cuál
    · Siempre, al final: ¿a quién más del gremio le pasa?
   ↓
3 · REGISTRAR   → fuente privada del proyecto (fuera de git: son personas reales)
    FACT:  lo que dijo, con sus palabras
    INFERENCE: lo que se deduce
    UNKNOWN: lo que no se preguntó
   ↓
4 · ANALIZAR    → capacidades: máximo 2
    · coo-graham → ¿esto se automatiza o se hace a mano?
    · cfo-precios → ¿el precio encaja con lo que ya paga?
   ↓
5 · DECIDIR
    GO      → /design
    NO-GO   → se anota el motivo y se cierra. Un no-go es un resultado válido
    UNKNOWN → qué falta y cómo se consigue
   ↓
GATE: DISCOVERY GATE
```

**Output:** ficha de conversación + decisión go/no-go con su motivo.

**Lo que este workflow impide, y es su razón de ser:** ir a enseñar lo que uno sabe hacer
en vez de escuchar qué le duele al otro. Es un rabbit hole recurrente, y el
paso 2 lo bloquea por construcción — la web no se abre hasta que el otro ha descrito su
problema.

---

## 4. `/design` — de un problema validado a una propuesta

**Cuándo:** después de un GO. Nunca antes.

```
1 · ENCUADRAR       decision-framing · 2-3 caminos, incluido no construir nada
2 · ALCANCE         pm-producto → el único problema que justifica que alguien pague
3 · FAN-OUT         ← paralelo, según qué toque el problema:
        arquitectura   → dev-dhh
        automatización → skill automation-architecture
        datos          → skill data-lifecycle + saas-multitenant-architecture
        interfaz       → director-arte → design-direction
        seguridad      → seguridad
        legal          → legal-basico  (obligatorio si hay datos de terceros)
4 · SÍNTESIS        una propuesta, no cinco informes pegados
5 · PRE-MORTEM      munger-critico → cómo fracasa esto en seis meses
6 · COSTE           cfo-precios → precio y coste de operarlo al mes
7 · ADR             toda decisión irreversible se escribe. Plantilla en templates/
   ↓
GATES: ARCHITECTURE · DATA · AUTOMATION · SECURITY · BUSINESS
   ↓
DECISIONS REQUIRED → la persona aprueba o recorta
```

**Output:** propuesta + ADRs + lista de decisiones para la persona.

**El paso 5 va después del 4 a propósito.** Un pre-mortem sobre una propuesta a medio
cocer produce riesgos de manual; sobre una propuesta cerrada, produce los reales.

---

## 5. `/release` — de terminado a publicado

**Cuándo:** antes de que algo llegue a un usuario real.
**Nombre:** `/release`, no `/ship`. La colisión está documentada en
[`current-state-audit.md`](current-state-audit.md) §3.3.

```
1 · VERIFICACIÓN TÉCNICA     ← lo que el proyecto ya tenga
      typecheck · lint · tests · build. Con la salida real pegada
   ↓
2 · FAN-OUT PARALELO         ← el único patrón multi-agente permitido
      qa-bach        → qué falla que nadie ha probado
      seguridad      → secretos, auth, datos personales
      analista-datos → ¿cómo sabremos si esto funcionó?
   ↓
3 · SÍNTESIS                 un veredicto, no tres informes
   ↓
4 · GATES                    QUALITY · SECURITY · UX · BUSINESS
   ↓
5 · HUMAN GATE               la persona. commit / push / deploy
   ↓
6 · VERIFICACIÓN POST        ← distinguir IMPLEMENTADO de VERIFICADO EN PRODUCCIÓN
```

**El paso 6 existe por un fallo real:** una instrumentación de analítica compilaba, pasaba
tests y construía — y eso no demuestra que registre un solo evento en producción. Que algo compile
no es que funcione.

**Output:** informe de release + lista de pendientes de verificación manual.

---

## 6. Cómo se enruta la intención

Sustituye a la tabla de `scrum-master`, que no puede ejecutarse. Vive en
`rules/orchestration.md`.

| Lo que dice quien lo usa | Va a |
|---|---|
| *"voy a hablar con X"* · *"me ha escrito un negocio"* | `/discover` |
| *"quiere que le haga X"* · *"cómo montaría esto"* | `/design` |
| *"vamos a construirlo"* | `superpowers:writing-plans` → `executing-plans` |
| *"esto ya está"* · *"lo subo"* | `/release` |
| *"¿por dónde sigo?"* | `scrum-master` (1 capacidad) |
| *"¿abro una apuesta?"* | `/bet` |
| *"¿voy bien?"* · *"llevo días atascado"* | `/hill` |
| *"cierro el ciclo"* | `/ship` |
| *"¿qué opináis de X?"* | `/crew` — **con techo de 3** |
| Pregunta de un dominio concreto | Ese agente, uno. Sin workflow |
| Decisión reversible de una tarde | **Nadie.** Que decida y siga |

**La última fila es la más importante y la que más se incumple.**

---

## 7. Anti-bloat: por qué tres y no ocho

| Pregunta del gate | `/discover` | `/design` | `/release` | OPERATE | CLIENT DELIVERY |
|---|:--:|:--:|:--:|:--:|:--:|
| ¿Problema observado hoy? | ✅ descubrimiento sin guion | ✅ la fase que viene | ✅ analítica sin verificar | ❌ cero incidentes | ❌ cero clientes |
| ¿Existe ya algo que lo resuelva? | ❌ | ❌ | ❌ | 🟡 `devops-hightower` | ❌ |
| ¿Se usará en ≥2 casos? | ✅ cada conversación | ✅ cada cliente | ✅ cada release | ? | ? |
| ¿Tiene gate verificable? | ✅ | ✅ | ✅ | ? | ? |
| ¿Tiene criterio para eliminarlo? | ✅ | ✅ | ✅ | — | — |
| **Se crea** | **SÍ** | **SÍ** | **SÍ** | **NO** | **NO** |

### Criterio de eliminación de los tres nuevos

Escrito ahora, que no hay apego:

| Workflow | Se retira si |
|---|---|
| `/discover` | Tras un ciclo entero de conversaciones, ninguna se registró usándolo |
| `/design` | Tras 2 propuestas, se saltó las dos veces |
| `/release` | Tras 3 releases, no detectó nada que los tests no detectaran ya |

**Un workflow que nadie usa es peor que ninguno:** ocupa contexto, sale en las listas y da
la falsa sensación de que el proceso existe.
