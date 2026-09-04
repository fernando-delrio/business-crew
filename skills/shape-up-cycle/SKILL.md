---
name: shape-up-cycle
description: Ciclo de trabajo real para quien programa solo o en equipo muy pequeño, basado en Shape Up (Basecamp) en lugar de Scrum. Úsalo para abrir una apuesta (alcance ↔ appetite), saber si estás cuesta arriba o cuesta abajo, detectar atascos, y cerrar un ciclo. Actívalo cuando alguien pregunte por dónde seguir, cuánto va a tardar algo, si sigue puliendo o lanza, o cuando lleve días sin avanzar visiblemente.
---

# El ciclo — Shape Up, no Scrum

Scrum se diseñó para equipos de 5-9 personas con ceremonias que necesitan varias personas
para tener sentido. Aplicado a un operador solo, produce teatro: un "daily standup" contigo
mismo no informa a nadie, y una "estimación en puntos" sin equipo con quien calibrar es un
número inventado.

Shape Up encaja porque resuelve los tres problemas reales de trabajar solo: **no saber
cuándo parar**, **no detectar que llevas días atascado**, y **una lista de ideas infinita
que solo genera culpa**.

---

## 1. Appetite — el cambio mental que lo sostiene todo

**Una estimación pregunta "¿cuánto tardará esto?". Un appetite dice "cuánto tiempo merece
la pena gastar en esto".**

La diferencia no es semántica: invierte qué variable es fija.

| | Variable fija | Variable que se ajusta |
|---|---|---|
| Estimación | El alcance | El tiempo (y siempre se pasa) |
| **Appetite** | **El tiempo** | **El alcance** |

Con appetite ya no fallas plazos, porque el plazo no se negocia: se negocia qué entra dentro.

**Appetites válidos para un operador solo:**

| Appetite | Duración | Para qué |
|---|---|---|
| **Pequeño** | 2-3 días | Un arreglo, una mejora acotada, una página |
| **Medio** | 1-2 semanas | Una feature completa de punta a punta |
| **Grande** | 4-6 semanas | Un módulo entero. Poco frecuente trabajando solo |

Si algo no cabe en 6 semanas, no es un ciclo: es un proyecto sin definir y hay que
volver a darle forma. **Nunca abras un ciclo sin appetite declarado.** Un ciclo sin
tiempo declarado es exactamente el "sigo puliendo" con otro nombre.

---

## 2. Dar forma antes de apostar

Antes de empezar, el trabajo tiene que estar **shaped**: ni tan abstracto que no se
sepa qué hacer, ni tan detallado que no quede margen para resolver problemas mientras
se construye.

Un trabajo bien formado tiene cuatro cosas:

1. **El problema** — en una frase, desde el usuario. No "añadir exportación a CSV" sino
   "el jefe de taller tiene que copiar los datos a mano cada viernes".
2. **El appetite** — cuánto tiempo vale.
3. **Los elementos** — a grandes rasgos qué piezas hay. Suficiente para saber que es
   posible, no tanto como para haberlo diseñado ya.
4. **Los rabbit holes** — los agujeros conocidos donde te vas a perder, señalados
   explícitamente, con la decisión ya tomada de cómo los evitas.
5. **El no-go** — qué queda fuera. Explícito, escrito. Es lo que impide que el alcance crezca solo.

**Si no puedes escribir los rabbit holes, no está formado.** Significa que aún no has
pensado dónde está la dificultad, y la vas a descubrir en el día 8 del ciclo.

---

## 3. El hill chart — la herramienta contra el atasco invisible

Esta es la parte que más aporta a quien trabaja solo, porque **nadie más va a notar que
llevas cuatro días girando en círculos.**

Olvida el porcentaje completado. La única pregunta es: **¿estás subiendo o bajando?**

```
                    ▲  cima: ya no quedan incógnitas
                 ／     ＼
     CUESTA   ／            ＼   CUESTA
     ARRIBA ／                 ＼  ABAJO
       ／                        ＼
   incógnitas                   ejecución
   "no sé cómo"                 "solo es hacerlo"
```

**Cuesta arriba = descubrir.** No sabes todavía cómo se resuelve. Aquí preguntar
"¿qué porcentaje llevas?" no tiene sentido: no sabes lo que no sabes.

Las tres etapas de la subida:
1. *"He pensado en esto"*
2. *"He validado mi enfoque"* — con algo construido, no imaginado
3. *"He llegado lo bastante lejos como para creer que no hay más incógnitas"*

**Cuesta abajo = ejecutar.** Ves todos los pasos que quedan y puedes estimar de verdad.
Aquí sí vale un porcentaje.

### La regla del punto que no se mueve

> **"Un punto que no se mueve es, en la práctica, una mano levantada: algo va mal aquí."**

Si dos días seguidos sigues en el mismo sitio de la colina, **eso es la señal**. No hace
falta que admitas que estás atascado: el punto quieto lo dice por ti.

**Qué hacer con un punto quieto:**
- ¿Sigues cuesta arriba? La incógnita es más grande de lo que parecía. Recorta alcance
  o cambia de enfoque. **No sigas empujando el mismo muro.**
- ¿Estás cuesta abajo y no avanza? Entonces no estabas cuesta abajo. Vuelve a subir:
  quedaba una incógnita que no habías visto.

**El error clásico:** creerse cuesta abajo cuando aún estás arriba. Se reconoce porque
"solo falta un detalle" lleva tres días siendo el mismo detalle.

---

## 4. Circuit breaker — la regla que cura el pulido infinito

> **Los proyectos que no llegan en su ciclo se cancelan por defecto, en vez de extenderse
> por defecto.**

No es un castigo: es gestión de riesgo. Extender por defecto convierte cada proyecto en
un pozo sin fondo, porque siempre parece que falta poco.

Cuando se agota el appetite y no está terminado, hay **tres salidas y ninguna es "seguir
un poco más sin pensarlo"**:

1. **Recortar y enviar** — casi siempre la correcta. ¿Qué versión más pequeña resuelve
   igualmente el problema del usuario?
2. **Cancelar** — el problema resultó menos valioso, o la solución más cara de lo que valía.
   Cancelar no es fracasar: es información comprada con tiempo.
3. **Volver a apostar explícitamente** — un ciclo nuevo, decidido a conciencia, no por inercia.
   Solo si sigue siendo lo más valioso que puedes hacer **comparado con todo lo demás.**

**La diferencia entre 3 y "seguir": la 3 se decide comparando con las alternativas.
Seguir es no decidir.**

---

## 5. Cool-down — el paréntesis obligatorio

Después de cada ciclo, **2-3 días sin apuesta**. Sin objetivo grande. Para bugs sueltos,
mantenimiento, deuda técnica pequeña, probar cosas, y decidir la siguiente apuesta con
la cabeza fría.

Trabajando solo se salta siempre, y es un error: la siguiente apuesta decidida el mismo
día que acabas la anterior se decide por inercia, no por criterio. **El cool-down es lo
que impide que el portfolio se decida solo.**

---

## 6. Sin backlog

Shape Up no tiene backlog, y esto es deliberado.

> Las ideas buenas sobreviven. Si algo importa de verdad, volverá a aparecer solo cuando
> vuelvas a mirar. Si no vuelve, no importaba.

Un backlog de 40 ideas no es un activo: es una lista de deudas emocionales que revisas
sin actuar. En su lugar, en cada cool-down se decide **desde cero** qué es lo más valioso
ahora, con la información de hoy.

Lo que sí se guarda: **problemas observados de usuarios reales**. Eso no es backlog, es
evidencia — y no caduca igual.

---

## 7. Estado del ciclo — `.crew/estado.md`

El ciclo vive en un fichero del proyecto para que sobreviva entre sesiones. Ese fichero
es lo que hace que al abrir el proyecto mañana sepas dónde estabas.

Estructura mínima:

```markdown
# Ciclo activo

**Apuesta:** <qué se construye, en una frase desde el usuario>
**Appetite:** <pequeño 2-3d | medio 1-2sem | grande 4-6sem>
**Empezó:** <fecha absoluta>
**Termina:** <fecha absoluta — calculada, no negociable>

**Colina:** <cuesta-arriba-1 | cuesta-arriba-2 | cuesta-arriba-3 | cima | cuesta-abajo | enviado>
**Último movimiento:** <fecha> — <qué cambió>

**Fuera de alcance (no-go):**
- <lo que NO entra en este ciclo>

**Rabbit holes identificados:**
- <dónde te vas a perder y cómo lo evitas>

**Decisiones tomadas:**
- <fecha> — <decisión> — <por qué>
```

**Al terminar un ciclo se archiva, no se borra.** El historial de apuestas es la memoria
del proyecto: qué se intentó, qué se canceló y por qué.

---

## Cómo lo aplicas

- **Alguien pregunta "¿por dónde sigo?"** → ¿hay ciclo activo? Si lo hay, la respuesta ya
  está decidida: sigue la apuesta. Si no, toca decidir apuesta (`/bet`).
- **Alguien pregunta "¿cuánto tardaré?"** → dale la vuelta: ¿cuánto tiempo merece la pena?
- **Alguien lleva días sin avance visible** → hill chart. Localiza si sigue cuesta arriba.
- **Se agotó el appetite** → circuit breaker. Las tres salidas. Nunca "un poco más".
- **Aparece una idea nueva a mitad de ciclo** → no entra. Se anota y se decide en el
  próximo cool-down. Proteger el ciclo es el trabajo.

## Lo que este ciclo NO es

No es Scrum con otros nombres. Si te descubres haciendo daily standups contigo mismo,
estimando en puntos o manteniendo un backlog priorizado, has vuelto a Scrum sin darte cuenta.

**Fuente:** [Shape Up, Ryan Singer (Basecamp)](https://basecamp.com/shapeup) — lectura
gratuita. Los capítulos que más rinden trabajando solo son el 13 (hill charts) y el 8
(betting table).
