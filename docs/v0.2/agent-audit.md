# Auditoría de agentes

> **2026-09-09.** Ficha por agente y política de convocatoria.
> **No se propone borrar ninguno.**

---

## 1. El listón

Un agente se justifica cuando tiene **las seis**: responsabilidad propia · criterio propio
· usa varias skills · participación recurrente · límites claros · inputs/outputs definidos.

| Criterio | Cuántos de los 18 lo cumplen |
|---|--:|
| Responsabilidad propia | 18 |
| Criterio propio | 18 |
| Límites claros (*"Cuándo NO aportas"*) | **18** ← lo mejor del repo |
| Inputs definidos (*"Contexto — siempre antes de responder"*) | 18 |
| **Outputs definidos y verificables** | **0** |
| **Usa varias skills** | **3** (`pm-producto`, `director-arte`, `scrum-master`) |
| **Participación recurrente demostrada** | **desconocida** — no se mide |

**Ningún agente cumple las seis.** Todos fallan en "output verificable", y quince en "usa
varias skills".

Eso no significa que sobren quince agentes. Significa que **el listón se cumple añadiendo
outputs y skills, no quitando personas.** El coste de arreglarlo es una sección por
archivo; el de borrar es perder 1.493 líneas de criterio bien escrito.

---

## 2. Las 18 fichas

`No owns` sale literal de la sección *"Cuándo NO aportas"* de cada archivo, que ya existe.

| # | Agente | Misión | Owns | No owns | Output propuesto | Escala a autoridad humana cuando | Solapa con | Estado |
|--:|---|---|---|---|---|---|---|---|
| 1 | `scrum-master` | Continuidad y siguiente paso | Proteger el ciclo · 2-3 pasos de hoy | Ejecutar · el trabajo de otro rol | Lista de 2-3 pasos + a quién derivar | Hay que abrir o cerrar apuesta | `/crew`, `/bet` | **IMPROVE** |
| 2 | `munger-critico` | Pre-mortem | Riesgos antes de invertir · causa raíz | Decisiones pequeñas y reversibles | 3-5 riesgos por prob.×daño + mitigación de esta semana | Un riesgo es mortal | `qa-bach`, `seguridad` | **KEEP** |
| 3 | `pm-producto` | Alcance mínimo | Qué NO construir · prioridad | Diseño · implementación | PRD de media pantalla | El usuario objetivo no está claro | `ceo-bezos` | **KEEP** |
| 4 | `ceo-bezos` | Prioridad de cartera | Enfoque entre proyectos · tipo 1 vs 2 | Detalle técnico · diseño · precio | Una recomendación con su porqué | Decisión tipo 1 (irreversible) | `pm-producto`, `/bet` | **DEPRECATE-CAND.** |
| 5 | `analista-thompson` | Estructura de mercado | Cadena de valor · ventaja estructural | Comunicar · vender · qué construir | Dónde está el poder + ventaja no copiable | — | `cmo-godin` | **DEPRECATE-CAND.** |
| 6 | `analista-datos` | Qué medir | Métrica única · embudo · instrumentación mínima | Por qué el usuario se atasca · precio | Métrica única + 5 eventos + cómo sacarla con lo que ya hay | Se va a recoger PII | `ux-norman` | **KEEP** ⚠️ infrautilizado |
| 7 | `cfo-precios` | Precio por valor | Unit economics · eje de escalado | Fiscal · contable · legal | Precio + las 4 cifras + qué falta | Toca asesor fiscal real | `ceo-bezos` | **KEEP** |
| 8 | `cmo-godin` | Posicionamiento | Audiencia mínima viable · anti-genérico | SEO técnico · cierre de venta | Mensaje que ningún competidor podría firmar | — | `ventas-ross` | **KEEP** |
| 9 | `ventas-ross` | Proceso repetible | Embudo · primeros diez clientes | Landings · herramientas internas | Proceso ejecutable en solitario | — | `cmo-godin` | **KEEP** |
| 10 | `coo-graham` | Automatizar vs a mano | Regla de volumen · optimización prematura | Cómo automatizar | Decisión con el número de volumen delante | — | `dev-dhh` | **KEEP** |
| 11 | `dev-dhh` | Arquitectura | Simplicidad · complejidad no ganada | Escribir código · revisar líneas · despliegue | Opinión + coste concreto de cada capa | Decisión irreversible → ADR | `devops-hightower` | **KEEP** |
| 12 | `devops-hightower` | Despliegue y entornos | Infra aburrida · infra vs código | Bugs de lógica · secretos | Diagnóstico + los 6 mínimos | Hay gasto o proveedor nuevo | `dev-dhh` | **KEEP** |
| 13 | `qa-bach` | Testing exploratorio | Asunciones no verificadas | Escribir los tests | Charter de exploración | Hallazgo bloqueante | `munger-critico` | **KEEP** |
| 14 | `seguridad` | Fallos comunes y caros | Auth · secretos · datos personales | Auditoría profesional · cumplimiento | Lista corta (≤5) con su arreglo | Datos sensibles o brecha | `legal-basico` | **KEEP** |
| 15 | `legal-basico` | Primera lectura de riesgo | Licencias · cláusulas · textos web | Asesoramiento vinculante · fiscal | Riesgo + **qué preguntar a un abogado** | Cualquier señal de alarma | `seguridad` | **KEEP** |
| 16 | `ux-norman` | Usabilidad | Golfos · modelos mentales · deslices vs errores | Estética · tokens | Diagnóstico + arreglo por golfo | — | `ui-duarte` | **KEEP** |
| 17 | `ui-duarte` | Sistema visual | Tokens · escala · densidad · estados | Usabilidad · features | Sistema de tokens reutilizable | — | `director-arte` | **KEEP** |
| 18 | `director-arte` | Brief antes de construir | Referencias · las 5 decisiones · listón | Maquetar · animar · tokens · features | Brief de 5 decisiones + nota de rúbrica | No hay tono de marca definido | **`design-direction`** | **IMPROVE** |

---

## 3. Los dos que hay que arreglar

### 3.1 `scrum-master` — el router que no puede enrutar

**Dos hechos verificables:**

1. `agent-skills` prohíbe el patrón: *"Do not build a 'router' persona that decides which
   other persona to call; that's the job of slash commands and intent mapping."*
2. **Un subagente no puede lanzar otro subagente.** Invocado como agente, `scrum-master`
   **no puede convocar a nadie**: solo escribe el nombre para que lo llame la persona operadora.

Su tabla de derivación de 17 filas es la mejor pieza de enrutado del repositorio **y está
en el archivo equivocado**.

**Propuesta:** la tabla sube al mapa de intención del orquestador
(`rules/orchestration.md`), donde sí puede ejecutarse desde un comando. `scrum-master`
conserva lo que es suyo y nadie más hace: proteger el ciclo, detectar parálisis de pulido,
detectar trabajo invisible, detectar el proyecto zombi y dar **2-3 pasos de hoy**.

Pasa de router a **guardián del ciclo**: un rol más pequeño y realmente ejecutable.

### 3.2 `director-arte` — el envoltorio que reimprime su skill

Dice *"Trabaja con la skill `design-direction`. Léela antes de responder. Ahí está la
rúbrica completa, el brief de cinco decisiones y la tabla de enrutado"* — y a continuación
**reproduce las tres**.

Único punto del repo donde el contenido de una skill se repite dentro de un agente. Si la
rúbrica cambia, hay dos sitios que tocar y uno se olvidará.

| Se queda en `director-arte` (el quién) | Vuelve a `design-direction` (el cómo) |
|---|---|
| *"¿Cuáles son las dos o tres referencias, con URL?"* | Las 5 decisiones del brief, desarrolladas |
| Detectar la huella del diseño generado sin dirección | La rúbrica Awwwards 40/30/20/10 |
| Defender la contención (un gesto, no dos) | La tabla de enrutado a skills de ejecución |
| Ajuste por tipo de producto | — |

`director-arte` bajaría de 83 a ~45 líneas y dejaría de mentir sobre dónde está la verdad.

---

## 4. Los dos candidatos a retirada — con criterio, no con opinión

**No se retiran ahora.** Se marcan con criterio medible.

| Agente | Por qué es candidato | Criterio de retirada | Qué lo salva |
|---|---|---|---|
| `ceo-bezos` | Prioriza **entre proyectos**. Hay un proyecto activo y la prioridad ya la decide `/bet` con appetite | **Sin invocar en 2 ciclos completos** → se archiva | Que la cartera vuelva a tener 2+ proyectos vivos |
| `analista-thompson` | Estructura de mercado: se usa una vez por mercado, y el del proyecto activo ya está analizado | Mismo criterio | Entrar en un vertical nuevo |

**Cómo se mide, ya que hoy no se mide nada:** el registro de invocaciones es parte de la
capa de inteligencia ([`intelligence-lifecycle.md`](intelligence-lifecycle.md) §5). Sin
ese registro este criterio no se puede aplicar — y ese es justo el motivo de que hoy no se
pueda decidir con datos si sobra alguien.

**Lo que NO justifica retirar un agente:** usarse poco pero acertar cuando se usa.
`legal-basico` se usará dos veces al año y una de ellas evitará un problema caro.

---

## 5. MINIMUM NECESSARY CREW

El problema no es tener 18 agentes: es convocar a ocho para una decisión de una tarde.

| Regla | Valor |
|---|---|
| **Techo por defecto** | **3 capacidades por decisión.** Más exige justificarlo por escrito |
| **Suelo** | 1. Si basta una, se llama a una. No hay quórum mínimo |
| **Cero** | Si la persona operadora ya sabe qué hacer, no se convoca a nadie |
| **Sin router persona** | El orquestador es un **comando**, nunca un agente |
| **Un solo patrón multi-agente** | **Fan-out paralelo + síntesis**. Nunca cadenas de agentes llamándose |
| **Antes de convocar** | Si falta un dato de entrada, se pide el dato. No se convoca a nadie para que adivine |

### Cuántos, por tipo de decisión

| Decisión | Capacidades | Ejemplo |
|---|--:|---|
| Reversible, de una tarde | **0** | Color de un botón, copy de una sección |
| Táctica, un dominio | **1** | *"¿qué mido en esta landing?"* → `analista-datos` |
| Táctica con tensión entre dos dominios | **2** | *"¿automatizo esto?"* → `coo-graham` + `dev-dhh` |
| Estratégica o irreversible | **3** | Precio: `cfo-precios` + `analista-thompson` + `munger-critico` |
| Verificación antes de publicar | **3 en paralelo + síntesis** | `qa-bach` + `seguridad` + `analista-datos` |
| Con dinero, datos personales o compromiso legal | **+`legal-basico` obligatorio** | — |

**Regla de coste:** convocar tres agentes `opus` para ordenar dos secciones cuesta más que
la decisión. La complejidad de la convocatoria debe ser proporcional a la **irreversibilidad
del error**. Ver [`model-routing.md`](model-routing.md).

---

## 6. Cifras

| | Ahora | Propuesto |
|---|--:|--:|
| Agentes | **18** | **18** |
| Con output verificable declarado | 0 | **18** |
| A mejorar | — | 2 |
| A fusionar | — | 2 duplicaciones, sin borrar archivos |
| Candidatos a retirada con criterio | — | 2 |
| A borrar | — | **0** |
| Agentes nuevos | — | **0** |

**Cero agentes nuevos.** Los dos huecos reales se cubren con skills, no con personas:
[`automation-capability.md`](automation-capability.md) §5 y
[`data-capability.md`](data-capability.md) §4.
