# Contrato del orquestador

> **2026-09-09.** El formato común de toda ejecución y la disciplina de evidencia.
> Destino propuesto: `rules/orchestration.md` (una sola regla, siempre activa).

---

## 1. Por qué existe

Hoy cada agente responde en su formato. No hay forma de saber, leyendo una respuesta, qué
está demostrado y qué es una opinión razonable.

Es un riesgo concreto, y ya ocurrido en un proyecto real: la bitácora afirmaba *"el camino de n8n, por
fin probado […] en el test se intercepta la petición"*. **Ese test no existía.** Una
inferencia razonable se escribió como hecho, y guió decisiones durante varios días.

El contrato existe para que eso no pueda pasar en silencio.

---

## 2. Clasificación de afirmaciones

Toda conclusión que salga de un workflow se marca con **una** de estas cuatro:

| Marca | Significa | Exige | Ejemplo real |
|---|---|---|---|
| **FACT** | Verificado. Con la evidencia al lado | Comando ejecutado, archivo leído, URL comprobada, cita textual | *"Los despliegues responden 200 — comprobado con `curl`"* |
| **INFERENCE** | Se deduce de evidencia, no está demostrado | Decir **de qué** se deduce | *"Los bundles pesan lo mismo → llevan la misma configuración"* |
| **RECOMMENDATION** | Curso de acción propuesto | Alternativa descartada + motivo | *"Retirar el webhook en vez de levantar el orquestador"* |
| **UNKNOWN** | Dato necesario que falta | **Quién** lo consigue y **cómo** | *"Si el plan del proveedor incluye eventos personalizados — panel del proveedor, la persona responsable"* |

### Las tres reglas que la hacen funcionar

1. **Un UNKNOWN nunca se rellena con una INFERENCE para poder seguir.** Si falta un dato
   que cambia la conclusión, el workflow **se detiene y lo pide**. Es lo que ya hacen bien
   varios agentes (*"pide el mínimo necesario"*, `analista-thompson`).
2. **Una INFERENCE presentada como FACT es un defecto del sistema**, no un matiz de estilo.
3. **Toda RECOMMENDATION lleva su descartada.** Una recomendación sin alternativa es una
   preferencia disfrazada — es la misma regla de `decision-framing`, elevada a contrato.

### Las tres marcas añadidas — y por qué solo tres

El encargo permite añadir `ASSUMPTION`, `RISK` y `DECISION` *"si realmente mejoran el
sistema"*. Las tres pasan el corte, con una condición cada una:

| Marca | Se justifica porque | Condición |
|---|---|---|
| **ASSUMPTION** | Es un UNKNOWN sobre el que **se decide igual**. Sin marca, se vuelve invisible y nadie lo revisa | Lleva **qué cambia si es falsa** |
| **RISK** | Es el output de `munger-critico` y necesita formato estable | Lleva probabilidad × daño **y** mitigación ejecutable esta semana |
| **DECISION** | Es lo que se mira dentro de seis meses. Sin registro, se re-decide | Lleva **reversibilidad** (tipo 1 / tipo 2, de `ceo-bezos`) |

**No se añade nada más.** `OPINION`, `NOTE`, `IDEA` u `OBSERVATION` no cambiarían ninguna
decisión: son las marcas que convierten un contrato en burocracia.

---

## 3. Formato de ejecución

El encargo propone 13 secciones. **Trece secciones para responder "¿qué color pongo?" es
burocracia**, así que el formato tiene dos tamaños con la misma estructura.

### Formato completo — decisiones estratégicas, irreversibles o con gasto

```markdown
## OBJECTIVE
Una frase. Qué se quiere conseguir, no qué se quiere hacer.

## CONTEXT
Proyecto, fase, ciclo activo. Sale de .crew/estado.md y del CLAUDE.md del proyecto.

## CONSTRAINTS
Appetite, no-go del ciclo, presupuesto, plazo, barreras técnicas.

## EVIDENCE
FACT: ... (con su comprobación)
FACT: ...

## UNKNOWNS
UNKNOWN: ... → quién lo consigue, cómo, y si bloquea
ASSUMPTION: ... → qué cambia si es falsa

## PLAN
2-5 pasos. Si son más de cinco, no es un plan: es un proyecto.

## CAPABILITIES REQUIRED
Máximo 3. Con el porqué de cada una. (Ver minimum-necessary-crew)

## EXECUTION
Lo que se hizo, con su salida real.

## QUALITY GATES
Cada gate aplicable: PASA / FALLA / NO APLICA, con evidencia.

## RISKS
RISK: ... (prob × daño) → mitigación de esta semana

## DECISIONS REQUIRED
Lo que necesita autoridad humana. Con opciones y recomendación.

## OUTPUTS
Artefactos producidos, con su ruta.

## NEXT ACTION
Una. La siguiente. No una lista.
```

### Formato corto — todo lo demás

```markdown
OBJECTIVE · EVIDENCE · UNKNOWNS · PLAN · OUTPUT · NEXT ACTION
```

**Regla de elección, para que no se decida por pereza:**

| Usa el completo si | Usa el corto si |
|---|---|
| La decisión es irreversible o cara de deshacer | Es reversible en una tarde |
| Hay gasto, datos personales o compromiso con un tercero | No |
| Se convocan ≥2 capacidades | 0 o 1 |
| Produce un artefacto que otros van a leer | Es una respuesta de conversación |

---

## 4. El bucle completo

```
INTENT            lo que pide la persona operadora, en sus palabras
   ↓
ORCHESTRATION     un comando (nunca un agente) mapea intención → workflow
   ↓
CONTEXT+EVIDENCE  .crew/estado.md · CLAUDE.md · PORTFOLIO.md · el repo
   ↓              ── aquí se marcan FACT / INFERENCE / UNKNOWN
CAPABILITIES      máximo 3, justificadas. Fan-out paralelo si son varias
   ↓
WORKFLOW          los pasos del workflow elegido
   ↓
QUALITY GATES     PASA / FALLA / NO APLICA, con evidencia
   ↓
HUMAN APPROVAL    solo lo que la política de autoridad exige
   ↓
EXECUTION         Claude Code hace el trabajo
   ↓
VERIFICATION      tests · build · comprobación real. No "debería funcionar"
   ↓
LEARNING          ¿esto es un patrón? → intelligence-lifecycle
```

### Dónde se rompe hoy

| Eslabón | Estado |
|---|---|
| INTENT | ✅ Lo escribe la persona operadora |
| ORCHESTRATION | 🔴 **No existe.** `/crew` sintetiza, no orquesta; `scrum-master` no puede convocar |
| CONTEXT+EVIDENCE | 🟡 Cada agente lo hace por su cuenta, sin marcar nada |
| CAPABILITIES | 🔴 Sin política. `/crew` puede convocar a los que quiera |
| WORKFLOW | 🔴 **No existe ninguno** |
| QUALITY GATES | 🔴 La palabra no aparece en el repo |
| HUMAN APPROVAL | 🟢 Barrera dura en `settings.json` |
| EXECUTION | ✅ Claude Code |
| VERIFICATION | 🟡 Depende de que alguien se acuerde |
| LEARNING | 🔴 Retro en `.crew/`, fuera de git, sin promoción |

**Seis rojos de diez.** Y los seis están en la mitad de arriba: el sistema sabe ejecutar y
no sabe decidir qué ejecutar ni comprobar que quedó bien.

---

## 5. Qué NO hace el contrato

| No hace | Por qué |
|---|---|
| Obligar a las 13 secciones siempre | Formato corto para lo reversible |
| Marcar cada frase de una conversación | Solo las conclusiones que salen de un workflow |
| Sustituir el criterio de los agentes | Es el sobre, no la carta |
| Exigir plantilla para una pregunta directa | Una pregunta se responde |

**Señal de que esto ha fallado:** si la persona operadora empieza a rellenar secciones para cumplir en
vez de para pensar, el contrato sobra y hay que recortarlo. El propio contrato se evalúa
en [`evaluation-strategy.md`](evaluation-strategy.md) §3.
