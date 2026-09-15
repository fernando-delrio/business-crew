# Capa de inteligencia

> **2026-09-09.** Cómo Business Crew acumula criterio sin convertirse en un vertedero.

---

## 1. El problema

El repositorio tiene **dos commits, ambos con el mismo mensaje**. No ha aprendido nada
desde que se creó.

Y sin embargo ha habido aprendizaje real: una auditoría produjo hallazgos que valen
para cualquier proyecto futuro —el placeholder que se comporta como valor real, el
`instanceof Error` que no distingue el origen, la documentación que afirma tests que no
existen—. **Todo eso quedó en el registro de errores del repositorio privado de ese
proyecto.**

El conocimiento genérico está atrapado en un producto concreto. Cuando la persona operadora
empiece otro proyecto, no viaja.

**Y el riesgo opuesto es igual de real:** volcar aquí todo lo que sale de una conversación
convierte el repo en un vertedero que nadie lee. Un archivo que nadie lee es peor que no
tenerlo: ocupa contexto y da falsa sensación de sistema.

---

## 2. Las ocho clases, y dónde vive cada una

La decisión más importante de este documento es **qué NO entra aquí**.

| Clase | Qué es | Dónde vive | ¿En business-crew? |
|---|---|---|---|
| **PROJECT FACTS** | Estado del proyecto: qué existe, qué falla | Su repositorio privado | ❌ Es del producto |
| **CLIENT FACTS** | Qué dijo un cliente concreto | Fuente privada del proyecto — **fuera de git** | ❌ **Nunca.** Personas reales identificables, y este repo es público |
| **MARKET EVIDENCE** | Lo que cobran los competidores de un sector concreto | Inteligencia privada del proyecto | ❌ Inteligencia comercial concreta |
| **DECISIONS** | Por qué se eligió X | ADR en el repo del producto | ❌ El registro; ✅ el **formato** |
| **PATTERNS** | *"Un placeholder en un campo opcional se comporta como un valor real"* | **`intelligence/patterns.md`** | ✅ **Sí** |
| **ANTI-PATTERNS** | *"Escribir «verificado» sobre algo que no se puede ejecutar"* | **`intelligence/patterns.md`** | ✅ **Sí** |
| **LESSONS** | El relato de un fallo concreto con su fecha | El registro de errores del proyecto | ❌ Es del producto |
| **EXPERIMENT RESULTS** | *"Se probó X y pasó Y"* | `.crew/` mientras el ciclo vive | ❌ salvo que se generalice |

### La regla, en una frase

> **En business-crew entra lo que valdría igual en otro proyecto, con otro cliente y en
> otro sector. Todo lo demás se queda donde ocurrió.**

Y una segunda, no negociable, porque el repositorio es **público con licencia MIT**:

> **Ningún dato de una persona real entra aquí. Nunca.** Ni nombre, ni negocio, ni
> teléfono, ni cita textual que permita identificar a alguien.

---

## 3. El ciclo de ascenso

```
RAW EVIDENCE          algo pasó — un bug, una conversación, una decisión
   │                  vive en .crew/ o en el repo del producto
   │  ← FILTRO 1: ¿es un hecho o una impresión?
   ▼
VERIFIED INSIGHT      hecho con evidencia: el comando, el archivo, la cita
   │                  sigue viviendo donde ocurrió
   │  ← FILTRO 2: ¿ha pasado en ≥2 contextos distintos?
   ▼
PATTERN               intelligence/patterns.md · 3-8 líneas
   │                  nombre · qué lo dispara · qué hacer · dónde se vio
   │  ← FILTRO 3: ¿tiene procedimiento repetible y gate?
   ▼
CANDIDATE SKILL       intelligence/candidates.md · una línea y un contador
   │  ← FILTRO 4: evaluación (evaluation-strategy.md)
   ▼
ACTIVE SKILL          skills/<nombre>/SKILL.md
```

### Los cuatro filtros

| Filtro | Pregunta | Rechaza |
|---|---|---|
| **1 · Evidencia** | ¿Se puede señalar el comando, el archivo o la cita? | Impresiones. *"Me pareció que…"* |
| **2 · Repetición** | ¿En **dos contextos distintos**? | Anécdotas. Un caso es un caso |
| **3 · Procedimiento** | ¿Hay pasos y criterio de salida? | Consejos. Un consejo es una frase en un agente |
| **4 · Evaluación** | ¿Se dispara cuando debe y no cuando no? | Skills que nadie invoca |

**El filtro 2 es el que más rechaza, y es el importante.** Es la línea entre *"esto me pasó"*
y *"esto pasa".

**Excepción documentada:** un fallo con consecuencia grave y causa clara puede ascender con
**un solo caso**, marcándolo como tal. El placeholder de `.invalid` que rompió un formulario
en producción no necesita una segunda víctima para ser un patrón.

---

## 4. Qué aspecto tiene un patrón

Corto por diseño. Si no cabe en ocho líneas, probablemente sea una skill.

```markdown
### Un placeholder se comporta como un valor real

**Dispara:** un campo opcional que puede contener un valor de ejemplo
(`.invalid`, `localhost`, `<TU_URL>`) y se comprueba con `if (campo)`.

**Qué hacer:** la comprobación no es "¿hay valor?" sino "¿este valor sirve?".
Y esa función corre también en producción, no solo en el test — el test solo
protege de lo que ya está en el repositorio.

**Visto en:** un proyecto consumidor, en un despliegue real — formulario roto en producción.
**Estado:** patrón · 1 caso, consecuencia grave.
```

Sin nombre de cliente, sin teléfono, sin nada que identifique a nadie. **Ese ejemplo es
publicable en un repo MIT tal cual está.** Ese es el listón.

---

## 5. El registro de uso — lo que hoy hace imposible decidir

Hay dos preguntas de este paquete de documentos que **no se pueden contestar** porque nada
se mide:

- *"¿`ceo-bezos` se usa?"* → desconocido
- *"¿un patrón ha aparecido en dos contextos?"* → desconocido

Sin registro, retirar un agente es una opinión y ascender un patrón es una corazonada.

### La versión mínima que pasa el anti-bloat gate

**No** un sistema de telemetría. Una línea por invocación, a mano o desde el hook de
`Stop`, en `.crew/` (por proyecto, fuera de git):

```
2026-09-09 · design · dev-dhh, seguridad · ADR-004 · util
2026-09-09 · discover · coo-graham · ficha · util
2026-09-12 · crew · ceo-bezos · — · no aportó
```

Cuatro campos: fecha · workflow · capacidades · resultado. Suficiente para contestar las
dos preguntas dentro de dos ciclos.

**Criterio de eliminación:** si al cabo de dos ciclos nadie lo ha rellenado, se retira y se
acepta que las decisiones sobre agentes se toman por criterio y no por datos. Un registro
que no se rellena es peor que ninguno: da falsa sensación de medición.

---

## 6. Estructura propuesta

```
intelligence/
├── patterns.md        patrones y anti-patrones. Genéricos. Publicables
└── candidates.md      candidatas a skill, con su contador de casos
```

**Dos archivos. No más.**

| Descartado | Por qué |
|---|---|
| Un archivo por patrón | Con seis patrones, seis archivos son más ruido que índice |
| `decisions/` | Los ADR viven en el repo del producto. Aquí solo la plantilla |
| `lessons/` | Es el registro de errores del producto. Aquí solo lo generalizado |
| `experiments/` | Cero experimentos registrados. Cuando haya dos, se crea |

### Reglas de cada archivo

| Archivo | Permitido | Prohibido |
|---|---|---|
| `patterns.md` | Patrones genéricos, anónimos, con su disparador y su acción | Nombres de clientes · teléfonos · citas identificables · nombres de negocio reales · cualquier PII |
| `candidates.md` | Nombre, problema, contador de casos, estado | Lo mismo |

---

## 7. Higiene — para que no se convierta en vertedero

| Regla | Motivo |
|---|---|
| **`patterns.md` ≤ 300 líneas.** Al llegar, se poda antes de añadir | Un archivo que no se lee entero no se lee |
| **Un patrón sin usar en 6 meses se retira.** Se anota que se retiró | Si no ha aplicado en seis meses, no era un patrón |
| **Un patrón que asciende a skill se borra de aquí** y se enlaza | Duplicación — el error de `director-arte` |
| **Ninguna conversación entra directamente.** Pasa los cuatro filtros o no entra | Es la regla que impide el vertedero |
| **Revisión en el cool-down**, no continua | El cool-down de Shape Up ya existe y es el momento natural |

### La regla que lo resume

> **Una conversación de Claude no se convierte en conocimiento permanente.**
> Un hecho verificado que se repite en dos sitios, sí.
