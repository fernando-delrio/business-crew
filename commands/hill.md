---
description: ¿Cuesta arriba o cuesta abajo? Actualiza tu posición en la colina y detecta si llevas días atascado sin darte cuenta.
argument-hint: [qué has avanzado, o vacío para que te pregunte]
---

Vas a actualizar el hill chart del ciclo activo. **Lee la skill `shape-up-cycle` primero**,
en concreto la sección 3.

Trabajando solo, nadie nota que llevas cuatro días girando en círculos. Este comando existe
para eso.

## Paso 1 — Leer el estado

Lee `.crew/estado.md`. Si no hay ciclo activo, dilo y ofrece `/bet`. No inventes uno.

Fíjate en dos cosas: la posición actual en la colina y **la fecha del último movimiento.**

## Paso 2 — La pregunta correcta

Nunca preguntes "¿qué porcentaje llevas?". Pregunta:

> **¿Todavía estás descubriendo cómo se hace, o ya sabes exactamente lo que queda?**

Y para situarlo con precisión:

| Posición | Significa |
|---|---|
| `cuesta-arriba-1` | *"He pensado en esto"* — tienes un plan, sin validar |
| `cuesta-arriba-2` | *"He validado mi enfoque"* — has construido algo que demuestra que funciona |
| `cuesta-arriba-3` | *"No creo que queden incógnitas"* — lo bastante lejos como para verlo entero |
| `cima` | Ves todos los pasos que faltan |
| `cuesta-abajo` | Solo es ejecutar. Aquí sí vale un porcentaje |

**Validar cuesta arriba significa haber construido algo, no haberlo pensado.** Si dice que
ha validado el enfoque pero no hay nada funcionando, sigue en `cuesta-arriba-1`. Sé estricto
aquí: es el autoengaño más común y el más caro.

## Paso 3 — Detectar el punto quieto

Compara con el último movimiento registrado.

**Si la posición no ha cambiado en 2 días o más, eso es una mano levantada.** Dilo
explícitamente, sin suavizarlo, y diagnostica:

**Sigue cuesta arriba y no se mueve** → la incógnita es mayor de lo que parecía.
No sirve empujar el mismo muro. Ofrece tres salidas concretas:
- Recortar el alcance para que la incógnita desaparezca
- Cambiar de enfoque por completo
- Resolver solo la parte fácil y ver si con eso ya basta

**Dice estar cuesta abajo pero no avanza** → entonces no estaba cuesta abajo.
Quedaba una incógnita sin ver. **Devuélvelo a la subida** y localiza cuál es.
La señal delatora: *"solo falta un detalle"* lleva tres días siendo el mismo detalle.

## Paso 4 — Comprobar el appetite

Calcula los días consumidos y los que quedan.

- **Consumido >50% y todavía cuesta arriba** → avisa ya. Es el momento de recortar,
  mientras aún hay tiempo de hacerlo con cabeza. Si esperas al final, la única salida
  que quedará es cancelar.
- **Appetite agotado** → circuit breaker. Presenta las tres salidas de la skill
  (recortar y enviar · cancelar · volver a apostar a conciencia). **No ofrezcas "seguir
  un poco más": eso no es una opción, es no decidir.**

## Paso 5 — Escribir y responder

Actualiza `.crew/estado.md` con la nueva posición y la fecha de hoy como último movimiento.
Registra en "Decisiones tomadas" cualquier recorte o cambio de enfoque acordado.

```
⛰️  <Proyecto> — día <n> de <total>

        ▲
     ／    ＼          Estás en: <posición>
  ／          ＼       <qué significa, en una línea>
／               ＼

<Si el punto no se mueve: la alerta, sin suavizar>
<Si el appetite aprieta: el aviso y las salidas>

Siguiente paso: <acción concreta de hoy>
```

Sé breve y honesto. El valor de este comando es decir lo que nadie más te va a decir.
