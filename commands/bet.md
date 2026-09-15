---
description: Abre un ciclo de trabajo de Shape Up: da forma a la apuesta, fija el appetite y escribe el no-go antes de tocar nada. Solo para EMPEZAR un ciclo nuevo — no decide precios, arquitectura ni diseño.
argument-hint: [qué quieres construir, o vacío para decidirlo entre las opciones]
---

Vas a abrir una apuesta siguiendo el ciclo de la skill `shape-up-cycle`. **Léela primero.**

Tu trabajo aquí no es empezar rápido: es que lo que empiece esté bien formado. Un ciclo
mal formado se descubre el día 8, cuando ya no hay tiempo de arreglarlo.

## Paso 1 — Comprobar si ya hay un ciclo abierto

Mira `.crew/estado.md` en el proyecto actual.

**Si hay un ciclo activo, no abras otro.** Muestra cuál es, cuántos días quedan, y pregunta:
¿esto sustituye a la apuesta actual (y por qué), o se anota para el próximo cool-down?
Abrir un segundo ciclo en paralelo es la forma más rápida de no terminar ninguno.

## Paso 2 — Contexto

Lee `~/.claude/PORTFOLIO.md` y el `CLAUDE.md` del proyecto. Necesitas saber qué es el
producto, de qué tipo, quién lo usa y en qué fase está.

## Paso 3 — Dar forma

**No aceptes la apuesta tal y como te la dan.** Casi siempre llega como solución
("añadir exportación a CSV") cuando lo que hace falta es el problema.

Trabaja estos cinco puntos con el usuario, preguntando lo que falte:

1. **El problema**, en una frase y desde el usuario final. Si no sabe decir a quién le
   pasa y con qué frecuencia, eso es lo primero que hay que averiguar.
2. **Appetite** — pequeño (2-3 días), medio (1-2 semanas) o grande (4-6 semanas).
   Pregúntalo así: *"¿cuánto tiempo merece la pena gastar en esto?"*, nunca *"¿cuánto crees
   que tardarás?"*.
3. **Los elementos** — a grandes rasgos, qué piezas hay. Lo justo para saber que es posible.
4. **Rabbit holes** — dónde te vas a perder. **Si no sabes decir ninguno, la apuesta no está
   formada:** significa que aún no has pensado dónde está la dificultad. Empújale a buscarlos.
5. **No-go** — qué queda fuera, explícito. Sin esto el alcance crece solo durante el ciclo.

## Paso 4 — Contrastar antes de confirmar

Antes de escribir nada, convoca mentalmente a dos roles y di lo que dirían:

- **`munger-critico`** — ¿cómo fracasa esta apuesta? Si el pre-mortem encuentra algo mortal,
  dilo ahora, no en el día 8.
- **`pm-producto`** — ¿es este el alcance mínimo que resuelve el problema, o hay una
  versión más pequeña que ya lo resuelve?

Si alguno levanta una bandera seria, **preséntala antes de abrir el ciclo** y deja que el
usuario decida con esa información.

## Paso 5 — Escribir el estado

Crea o actualiza `.crew/estado.md` con la plantilla de la skill `shape-up-cycle`.
Calcula la fecha de fin a partir del appetite y la fecha de hoy — **fecha absoluta, no
"en dos semanas"**. Deja la colina en `cuesta-arriba-1`.

Si `.crew/` no existe, créalo. Sugiere añadirlo al `.gitignore` **solo si el usuario
trabaja con más gente**; en solitario es mejor versionarlo, porque el historial de apuestas
es memoria del proyecto.

## Paso 6 — Confirmar

```
🎯 Apuesta abierta — <proyecto>

Problema:   <una frase desde el usuario>
Appetite:   <tamaño> · del <fecha> al <fecha>
Colina:     cuesta arriba (1/3) — descubriendo

Fuera:      <no-go, en una línea>
Ojo con:    <el rabbit hole principal>

Primer paso hoy: <acción concreta que cabe en una sesión>
```

Recuérdale la regla que hace que esto funcione: **cuando se agote el appetite, se recorta
y se envía, se cancela, o se vuelve a apostar a conciencia. Nunca "un poco más".**
