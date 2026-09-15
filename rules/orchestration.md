# Orquestación y enrutado

> **Fuente de verdad única del enrutado.** Ningún agente reproduce esta tabla: la
> referencian. Antes vivía dentro de `scrum-master`, donde no podía ejecutarse.

---

## 1. Por qué salió de `scrum-master`

Dos motivos, y el segundo es duro:

1. Un agente que decide qué otro agente llamar es un **router persona**, y el patrón está
   desaconsejado: orquestar es trabajo de un comando, no de una persona.
2. **Un subagente no puede lanzar otro subagente.** Invocado como agente, `scrum-master`
   **no puede convocar a nadie**: solo escribe el nombre para que lo llame una persona.

La tabla era la mejor pieza de enrutado del repositorio y estaba en el archivo equivocado.

---

## 2. Mapa de enrutado

Escrito en **lenguaje del problema**, no en el del experto. La regla que lo explica: quien
ya sabe decir *"unit economics"* ya sabe a quién llamar. El mapa existe para quien **no**
lo sabe.

| Lo que dice una persona con el problema | Primaria | Secundaria opcional | NO enrutar a |
|---|---|---|---|
| *"no sé cuánto cobrar"* · *"cuánto pido por esto"* · *"¿me sale a cuenta?"* | `cfo-precios` | `analista-thompson` | `dev-dhh`, `ui-duarte` |
| *"no sé si entra alguien"* · *"¿esto sirve para algo?"* · *"¿funcionó?"* | `analista-datos` | `cmo-godin` | `dev-dhh`, `devops-hightower` |
| *"quiero meter otra cosa"* · *"me piden tres a la vez"* · *"¿por dónde empiezo el producto?"* | `pm-producto` | `munger-critico` | `ui-duarte` |
| *"esto puede estar expuesto"* · *"hay una clave en el código"* · *"cualquiera podría llamarlo"* | `seguridad` | `devops-hightower` | `cmo-godin`, `cfo-precios` |
| *"cómo despliego esto"* · *"en mi máquina va y publicado no"* · *"se rompió al subirlo"* | `devops-hightower` | `dev-dhh` | `cmo-godin` |
| *"funciona pero la gente se pierde"* · *"no entienden qué hacer"* · *"abandonan a mitad"* | `ux-norman` | `ui-duarte` | `director-arte` |
| *"se ve soso"* · *"parece igual que todas"* · *"no sé qué le falta"* | `director-arte` → skill `design-direction` | `ui-duarte` | `ux-norman` |
| *"qué tamaño de letra"* · *"qué colores"* · *"esto no pega con lo otro"* | `ui-duarte` | `director-arte` | `ux-norman` |
| *"los tests pasan, ¿publico?"* · *"se ha roto otra vez"* · *"qué puede fallar"* | `qa-bach` | `seguridad` | `cmo-godin`, `ventas-ross` |
| *"cómo organizo el código"* · *"¿me estoy complicando?"* · *"dónde meto esto"* | `dev-dhh` | `devops-hightower` | `ui-duarte` |
| *"lo hago a mano, ¿lo automatizo?"* · *"quiero que esto se haga solo"* | `coo-graham` | `dev-dhh` | `cmo-godin`, `ventas-ross` |
| *"no sé qué poner en la web"* · *"suena igual que todos"* · *"a quién le hablo"* | `cmo-godin` | `analista-thompson` | `ui-duarte` |
| *"no tengo clientes"* · *"cómo consigo el primero"* · *"vendo de casualidad"* | `ventas-ross` | `cmo-godin` | `ui-duarte` |
| *"quién más hace esto"* · *"¿hay hueco?"* · *"contra quién compito"* | `analista-thompson` | `cmo-godin` | `dev-dhh`, `qa-bach` |
| *"¿en qué me centro?"* · *"tengo varios frentes"* · *"¿merece la pena a largo plazo?"* | `ceo-bezos` | `pm-producto` | `ui-duarte` |
| *"¿por dónde va a fallar esto?"* · *"antes de meterle semanas"* · *"algo va mal y no sé por qué"* | `munger-critico` | `qa-bach` | — |
| *"voy a firmar"* · *"puedo usar este código"* · *"recojo datos en un formulario"* | `legal-basico` | `seguridad` | `cfo-precios` |
| *"vuelvo tras un tiempo"* · *"por dónde sigo"* · *"llevo días sin avanzar"* | `scrum-master` | — | `ceo-bezos` |
| *"quiero varias opiniones sobre esto"* · *"contrastad esta decisión"* | `/crew` | — | `scrum-master` |
| *"empiezo un ciclo"* · *"qué apuesto estas dos semanas"* | `/bet` | `pm-producto` | — |
| *"¿voy bien?"* · *"actualizo la colina"* | `/hill` | — | — |
| *"cierro el ciclo"* · *"esto ya está, ¿qué hago?"* | `/ship` | `qa-bach` | — |

### Huecos conocidos — capacidad ausente, no enrutado roto

| Lo que dice | Estado |
|---|---|
| *"cómo monto el flujo, con reintentos y qué pasa si falla"* | 🔴 **Nadie lo posee.** `coo-graham` decide *si*, no *cómo*. Candidata `automation-architecture`, sin aprobar |
| *"guardo datos de varios clientes sin que se vean entre ellos"* | 🟡 El dueño está **fuera de este repo**: skill `saas-multitenant-architecture`. Aquí, `dev-dhh` + `seguridad` |
| *"cuánto tiempo guardo esto"* · *"cómo borro los datos de alguien"* | 🔴 **Nadie.** Candidata `data-lifecycle`, sin aprobar |

**Un hueco se dice, no se rellena con la capacidad más cercana.**

---

## 3. Minimum necessary crew

| Regla | |
|---|---|
| **Por defecto: UNA primaria** | Una capacidad, no un comité |
| **Secundaria solo con razón explícita** | Hay tensión real entre dos dominios, o la primaria lo pide |
| **Techo: 3** | Más exige justificarlo por escrito |
| **Cero** | Si la persona ya sabe qué hacer, no se convoca a nadie |
| **Antes de convocar** | Si falta un dato de entrada, se pide el dato. No se convoca a nadie para que adivine |

### Cuántas, por tipo de decisión

| Decisión | Capacidades |
|---|--:|
| Reversible, de una tarde | **0** |
| Un solo dominio | **1** |
| Tensión real entre dos dominios | **2** |
| Estratégica o difícil de deshacer | **3** |
| Verificación antes de publicar | **3 en paralelo + síntesis** |
| Con dinero, datos personales o compromiso legal | **+`legal-basico`** |

---


## 3bis. DOMAIN FIRST / PROCEDURE SECOND

La regla que decide quién es primario cuando compiten un **agente de dominio** y una
**skill de procedimiento**.

> **Si la consulta necesita primero criterio de un dominio, el primario es el agente de
> ese dominio. Una skill de procedimiento puede ser secundaria — nunca primaria — salvo
> que el usuario pida el procedimiento explícitamente.**

### Por qué

Una skill sabe **cómo se estructura** una decisión. No sabe **cuál es la respuesta
correcta** en precio, seguridad, datos o interfaz. Enrutar a la skill primero produce una
comparación bien formada entre dos opciones que un experto habría descartado las dos.

Y hay evidencia: en el holdout, `decision-framing` ganó una consulta sobre una contraseña
expuesta y otra sobre automatizar un aviso. Ninguna de las dos es un problema de método.

### Cómo se aplica

| Consulta | Primario | Secundario | Por qué |
|---|---|---|---|
| *"¿cobro 400 o 700?"* | `cfo-precios` | `decision-framing` | Hace falta saber qué vale, no cómo se compara |
| *"tenemos dos arquitecturas posibles"* | `dev-dhh` | `decision-framing` | El criterio técnico va primero |
| *"se me ha quedado una contraseña en el código"* | `seguridad` | — | No hay decisión que estructurar: hay algo que arreglar |
| *"no sé si entra alguien en la web"* | `analista-datos` | — | Es un problema de medición |
| *"tengo dos caminos y llevo días dándole vueltas"* | **`decision-framing`** | `pm-producto` | **Aquí sí manda el procedimiento**: las alternativas ya existen y el problema es compararlas |
| *"quiero dar forma a la apuesta de este ciclo"* | **`shape-up-cycle`** | `/bet` | El usuario nombra el procedimiento |
| *"cómo validamos esta dirección visual"* | **`design-direction`** | `director-arte` | Pide estructurar el método |
| *"se ve soso, le falta algo"* | `director-arte` | `design-direction` | Insatisfacción vaga: primero criterio |

### La prueba, en una pregunta

> **¿Lo que falta es saber la respuesta, o saber cómo elegir entre respuestas que ya
> tenemos?**

Lo primero es dominio. Lo segundo es procedimiento. **En la duda, gana el dominio**: una
skill mal invocada gasta un turno; un dominio mal invocado da una respuesta equivocada.

### Corolario para las descripciones de skill

Una skill de procedimiento **no debe contener vocabulario de dominio** en su descripción.
`decision-framing` no dice "precio", "seguridad" ni "arquitectura" — dice cuándo hay
*alternativas que comparar*. Si una skill empieza a nombrar dominios, competirá con sus
agentes y ganará por accidente.

## 4. Quién puede orquestar

| Puede | No puede |
|---|---|
| Un **comando** convoca capacidades | Un **agente** no convoca a otro agente — no es estilo, es una restricción de la plataforma |
| Un agente **lee** una skill | — |
| Un agente **nombra** a quién derivar | — |

**Único patrón multi-agente admitido:** fan-out en paralelo + una síntesis. Nunca cadenas
de agentes llamándose entre sí.

---

## 5. Las dos puertas de entrada

No son equivalentes y conviene no confundirlas:

| | `scrum-master` | `/crew` |
|---|---|---|
| **Para** | Continuidad: por dónde sigo | Contraste: qué opinan varios sobre **una** decisión |
| **Entrada** | El estado del proyecto | Una pregunta concreta |
| **Salida** | 2-3 pasos de hoy + **una** derivación | Posturas de varios roles, sintetizadas |
| **Convoca** | No: deriva | Sí, en paralelo |
| **Protege el ciclo** | Sí, es la mitad de su trabajo | No |
| **Cuándo** | *"vuelvo y no sé por dónde retomar"* | *"esto es caro de deshacer, quiero contraste"* |

**La prueba:** si la pregunta es *"¿qué hago ahora?"* → `scrum-master`. Si es *"¿qué opináis
de esto?"* → `/crew`.

---

## 6. Mantenimiento

- Este archivo es la **única** fuente de enrutado. Un agente que reproduzca la tabla
  introduce una segunda verdad que se desincronizará.
- Al añadir o retirar una capacidad, se actualiza aquí **y** se añade su caso en
  `evals/fixtures/`.
- Se verifica con `python evals/tier2_similarity.py`.
- **Criterio de eliminación:** si en dos ciclos nadie lo consulta y el enrutado no mejora,
  sobra.
