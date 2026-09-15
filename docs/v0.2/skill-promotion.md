# Protocolo de promoción a skill

> **2026-09-09.** Cómo un aprendizaje se convierte en skill — y, sobre todo, cómo **no**.

---

## 1. El riesgo que este protocolo evita

`skillization` prematura: convertir en skill cada cosa que salió bien una vez.

El síntoma es conocido y medible: un catálogo que crece, descripciones que se parecen cada
vez más, enrutado que empieza a fallar, y un agente que carga tres skills para hacer lo que
hacía con una frase.

`agent-skills` lo dice en su propio flujo de contribución: *"Most new-skill ideas overlap an
existing skill or an open PR; prefer extending an existing skill over adding a
near-duplicate."* Con 25 skills ya les pasa. Con 3, a Business Crew le pasaría antes.

---

## 2. Los requisitos

Los del encargo, con el criterio de verificación al lado. **Los ocho, o no asciende.**

| # | Requisito | Cómo se comprueba | Rechaza |
|---|---|---|---|
| 1 | **Problema repetido** | Aparece en `intelligence/patterns.md` con su contador | Una anécdota |
| 2 | **≥2 contextos** | Dos proyectos, dos clientes o dos sectores distintos | La misma situación vista dos veces |
| 3 | **Procedimiento** | Pasos numerados y ordenados | Un consejo. Un consejo cabe en un agente |
| 4 | **Inputs** | Qué hace falta antes de empezar | *"Depende"* |
| 5 | **Outputs** | El artefacto que produce | *"Una respuesta"* |
| 6 | **Failure modes** | Qué sale mal y cómo se nota | Skills que solo describen el camino feliz |
| 7 | **Quality gate** | Criterio de salida comprobable | *"Cuando esté bien"* |
| 8 | **Evaluación** | Caso de eval que pasa — ver [`evaluation-strategy.md`](evaluation-strategy.md) | Sin eval no se activa |

### La excepción, y su límite

El requisito 2 se puede saltar **una vez** cuando hay **un solo caso con consecuencia
grave y causa clara**. Se marca `1 caso · consecuencia grave` y se revisa en el siguiente
cool-down.

El límite: **no más de una skill activa bajo excepción a la vez.** Si hay una y aparece
otra candidata en las mismas condiciones, primero se confirma la primera.

---

## 3. El camino

```
1 · CANDIDATA        alguien propone. Entra en intelligence/candidates.md
                     una línea: problema · contexto · quién lo propuso
      ↓
2 · PRE-FLIGHT       ← el filtro que más rechaza
      · ¿Ya existe una skill que lo cubre?        → extenderla
      · ¿Lo cubre algo instalado fuera?            → enlazarlo, no reescribirlo
      · ¿Cabe como sección de una skill existente? → sección
      · ¿Es criterio en vez de procedimiento?      → va a un agente
      ↓ solo si las cuatro son NO
3 · ESPERAR EL 2º CASO   se anota y se espera. No se escribe nada todavía
      ↓
4 · ESCRIBIR         anatomía de agent-skills. ≤300 líneas
      ↓
5 · EVALUAR          Tier 1 (estructura) + Tier 2 (enrutado y colisión)
      ↓
6 · ACTIVAR          skills/<nombre>/SKILL.md · se borra de candidates.md
      ↓
7 · REVISAR          en cada cool-down: ¿se ha usado?
```

**El paso 3 es el corazón del protocolo.** Una candidata puede estar meses esperando su
segundo caso, y eso es un éxito del sistema, no un atasco.

---

## 4. El pre-flight, con ejemplos reales

| Candidata | Resultado |
|---|---|
| *"Skill de modelado de datos"* | ❌ **RECHAZADA** en pre-flight: `schema-reviewer` y `saas-multitenant-architecture` ya lo cubren. Se reformuló a `data-lifecycle`, que empieza donde ellas acaban |
| *"Skill de arquitectura de automatización"* | ✅ **PASA** el pre-flight: nada lo cubre. Pero espera al primer caso real construido |
| *"Skill de entrevista de descubrimiento"* | ✅ **PASA**, y con 10 casos por delante en dos semanas |
| *"Skill de cómo escribir un ADR"* | ❌ **RECHAZADA**: es una **plantilla**, no un procedimiento. Va a `templates/adr.md` |
| *"Skill de revisar bundles"* | ❌ **RECHAZADA**: un caso, y muy específico de una herramienta. Se queda como patrón |

Cinco candidatas, **tres rechazadas**. Si el protocolo no rechaza la mayoría, no está
funcionando.

---

## 5. Qué NO es una skill

La clasificación del encargo, aplicada:

| Si lo que falta es… | No es una skill. Es… |
|---|---|
| Criterio para juzgar un caso ambiguo | **AGENT** |
| Una restricción siempre activa | **RULE** |
| Un formato de salida | **TEMPLATE** |
| Una lista de comprobación de salida | **GATE** |
| Un hecho o una tabla de referencia | **KNOWLEDGE** (`intelligence/patterns.md`) |
| Coordinar varias capacidades | **WORKFLOW** |
| Algo que debe pasar sin que nadie lo pida | **HOOK** |
| Algo determinista que puede ejecutar una máquina | **SCRIPT** |

**Una skill es la única de las ocho que responde a "¿cómo se hace esto, paso a paso, y
cómo sé que está terminado?"**

---

## 6. Retirada

Una skill que no se usa cuesta: ocupa contexto, aparece en el enrutado y compite con la
correcta.

| Criterio | Acción |
|---|---|
| Sin invocar en 2 ciclos completos | Se revisa en el cool-down |
| Sin invocar en 4 ciclos | Se retira |
| Su Tier 2 colisiona ≥75 % con otra | **Se fusionan.** No coexisten dos descripciones casi iguales |
| Lo que cubre pasa a estar cubierto fuera | Se retira y se enlaza |
| Su gate nunca ha fallado en ningún uso | 🟡 Sospechoso: o el gate es trivial o nadie lo comprueba |

**Retirar no es borrar la primera vez.** Se marca `DEPRECATED` un ciclo, y si nadie la
reclama, se borra. Un ciclo es dos semanas: suficiente para notar la falta, poco para
acumular.

---

## 7. Las tres skills actuales

| Skill | ¿Pasaría el protocolo hoy? | Qué le falta |
|---|:--:|---|
| `shape-up-cycle` | ✅ | Sección de **Verification** |
| `decision-framing` | ✅ | **Verification** + tabla de racionalizaciones |
| `design-direction` | ✅ | **Verification** + recuperar lo que `director-arte` le duplica |

**Las tres pasan por contenido y las tres fallan por formato:** ninguna declara cuándo su
proceso está terminado.

**Lo primero no es escribir skills nuevas: es cerrar las tres que ya existen.** Cierra el
hueco de "cero salidas verificables" sobre material ya probado, y el coste es una sección
por archivo.
