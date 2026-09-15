---
name: decision-framing
description: Úsala cuando YA hay dos o tres caminos concretos sobre la mesa y lo que cuesta es compararlos: separar el problema de la solución que viene envuelta dentro, ponerlos en los mismos ejes y saber si la elección es reversible o no. Es un PROCEDIMIENTO, no criterio de dominio: si la duda es de precio, seguridad, datos, interfaz o arquitectura, primero va el agente de ese dominio y esta skill ayuda después a estructurar la elección.
---

# Cómo se plantea una decisión

Casi todas las malas decisiones de producto no se toman mal: **se plantean mal.** Llegan
ya con la respuesta dentro, en forma de sí/no, y entonces lo único que queda por hacer es
justificarla.

---

## 1. "Compare and contrast", no "whether or not"

Este es el cambio que más mejora las decisiones, y está documentado en el trabajo de
Teresa Torres sobre descubrimiento continuo:

> **Una mente humana compara mejor de lo que evalúa.** Ante una sola opción, buscamos
> razones para justificarla. Ante tres, las comparamos de verdad.

| Planteamiento | Qué produce |
|---|---|
| ❌ *"¿Construyo el chat integrado?"* | Sí/no. Y como ya lo has pensado, saldrá que sí |
| ✅ *"El cliente no se entera de los avisos. Tres formas de resolverlo: chat, email automático, aviso en la app. Comparadas por coste, tiempo y riesgo."* | Una decisión real |

**Regla dura: nunca respondas sí/no a una pregunta de producto.** Reformula a dos o tres
caminos comparados, o pide el dato que falta para poder compararlos.

La excepción son las decisiones triviales y reversibles. Aplicar esto al color de un botón
es burocracia; aplicarlo a un mes de trabajo es lo que evita tirarlo.

---

## 2. Separa el problema de la solución

Una petición casi nunca llega como problema. Llega como solución:

> *"Necesito exportación a CSV"* ← esto es una solución
> *"El jefe de taller copia los datos a mano cada viernes y tarda dos horas"* ← esto es el problema

**Sube un nivel antes de decidir.** La pregunta es siempre: *¿qué problema resuelve esto,
y a quién le pasa?*

Cuando llegas al problema real, casi siempre aparecen soluciones que nadie había considerado
—y suelen ser más baratas. Quizá no hacía falta exportar: hacía falta un informe automático
por correo los viernes.

**Si no se puede nombrar el problema, no hay decisión que tomar.** Hay que ir a averiguarlo.

---

## 3. Genera antes de comparar

Antes de comparar caminos hay que tenerlos. Dos reglas:

1. **Genera en solitario primero, compara después.** Discutir mientras se generan opciones
   hace que la primera idea ancle todas las demás.
2. **Genera solo sobre el problema elegido**, no sobre todos los problemas a la vez.
   Abrir el abanico entero produce una lista inmanejable y ninguna decisión.

**Mínimo tres caminos**, y que uno sea deliberadamente incómodo:

- **El obvio** — lo que ya habías pensado
- **El barato** — la décima parte de esfuerzo. ¿Resuelve el 80%?
- **El radical** — no construir nada. Cambiar un texto, un proceso manual, quitar la función
  que causa el problema

**El camino "no construir nada" gana más veces de las que nadie espera.** Ponlo siempre
en la mesa: si no está, no se elige.

---

## 4. Clasifica por reversibilidad antes de gastar tiempo pensando

Cuánto esfuerzo merece la decisión depende de si se puede deshacer:

| Tipo | Qué es | Cómo se decide |
|---|---|---|
| **Tipo 1 — irreversible** | Modelo de datos multi-tenant, nombre de marca, pasarela sobre la que construyes la facturación, ceder propiedad intelectual | Despacio. Compara a fondo. Consulta |
| **Tipo 2 — reversible** | Copy, precio de lanzamiento, color primario, orden del onboarding, nombre de un endpoint interno | **Rápido.** Decide y ajusta con datos |

**El error caro es tratar una tipo 2 como tipo 1.** Es la causa número uno de parálisis en
quien trabaja solo: semanas dándole vueltas a algo que se cambia en una tarde.

Cuando lo detectes, dilo tal cual: *"esto lo cambias en una tarde. Decide y sigue."*

---

## 5. La tabla de comparación

Cuando presentes caminos, preséntalos así. **Nunca en prosa**: la prosa esconde que un
camino es peor, la tabla lo enseña.

```
Problema: <una frase, desde el usuario>

| Camino | Qué implica | Tiempo | Riesgo | Qué se pierde |
|---|---|---|---|---|
| A. <obvio>   | | | | |
| B. <barato>  | | | | |
| C. <radical / no construir> | | | | |

Recomendación: <uno> — porque <razón en una línea>
Reversible: <sí / no>
Lo que cambiaría mi recomendación: <el dato que falta>
```

Esa última línea es la más importante y la que casi nadie escribe. **Hace explícito qué
información convertiría esto en una decisión distinta**, y muchas veces conseguir ese dato
cuesta menos que construir cualquiera de los caminos.

---

## 6. Recomienda: no dejes la decisión en el aire

Comparar no es escurrir el bulto. **Después de la tabla, moja.** Presentar tres opciones
sin recomendación devuelve el problema entero a quien preguntó, y eso no es ayudar.

La forma correcta: **una recomendación clara, su porqué en una línea, y qué la cambiaría.**

---

## Señales de que la decisión está mal planteada

- La pregunta admite sí/no → falta reformular
- La petición nombra una solución, no un problema → sube un nivel
- Solo hay un camino sobre la mesa → falta generar
- No está el camino "no construir nada" → falta el más barato de todos
- Nadie sabe si es reversible → se está gastando esfuerzo a ciegas
- Se lleva días decidiendo algo que se cambia en una tarde → es tipo 2, decide ya

**Fuente:** [Opportunity Solution Tree — Teresa Torres](https://www.productplan.com/glossary/opportunity-solution-tree) ·
["Compare and contrast" frente a "whether or not"](https://getperspective.ai/blog/opportunity-solution-tree-2026-practical-guide-continuous-discovery)

## Verification

La skill se ha aplicado bien si se cumple todo esto. Si falta algo, la decisión no está
planteada: está justificada.

- [ ] **Hay dos o tres caminos comparados**, no un sí/no. Uno de ellos es *no hacer nada*
- [ ] **Los caminos son comparables**: se describen con los mismos ejes, no uno en detalle
      y los otros como espantapájaros
- [ ] **El problema está separado de la solución propuesta** — se puede enunciar sin
      nombrar ninguna de las opciones
- [ ] **La reversibilidad está declarada**: tipo 1 (cara de deshacer) o tipo 2
- [ ] **Los `UNKNOWN` están visibles**, con quién los consigue y si bloquean
- [ ] **Si un dato que falta cambiaría la elección**, se ha parado a pedirlo en vez de
      suponerlo

### Qué invalida el resultado

| Señal | Qué pasó |
|---|---|
| Una sola opción con razones a favor | Se justificó una decisión ya tomada |
| Las alternativas son obviamente peores | Espantapájaros: la comparación es decorativa |
| Falta *no hacer nada* | La opción más barata no se evaluó |
| Una decisión tipo 2 tratada como tipo 1 | Parálisis: se puede cambiar en una tarde |
| Un `UNKNOWN` rellenado con una suposición para poder seguir | La conclusión descansa sobre aire |
