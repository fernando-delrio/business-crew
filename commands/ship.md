---
description: Cierra el ciclo. Verifica que está de verdad terminado, hace la retro, archiva la apuesta y arranca el cool-down.
argument-hint: [vacío]
---

Vas a cerrar el ciclo activo. **Lee la skill `shape-up-cycle` primero.**

Cerrar bien importa tanto como abrir bien: un ciclo que se cierra sin retro no deja
aprendizaje, y un ciclo que se cierra sin cool-down encadena la siguiente apuesta por
inercia en vez de por criterio.

## Paso 1 — Leer el estado

Lee `.crew/estado.md`. Si no hay ciclo activo, dilo y para.

## Paso 2 — ¿Está terminado de verdad?

**No aceptes "sí" sin comprobarlo.** Pregunta y verifica:

- ¿El problema del usuario está resuelto de punta a punta, o solo la parte de backend?
- ¿Alguien lo ha usado ya, aunque sea tú simulando al usuario real?
- ¿Se quedó algo a medias que va a volver como bug la semana que viene?

**Si no está terminado**, no es un cierre: es un circuit breaker. Salta a las tres salidas
(recortar y enviar · cancelar · volver a apostar) y trátalo como tal.

## Paso 3 — Convocar al equipo de cierre

Si el ciclo tocó algo que va a producción, convoca a los que corresponda **antes** de
darlo por enviado:

- **`qa-bach`** — qué ha cambiado y qué asunciones no verificadas hay
- **`seguridad`** — solo si se tocó autenticación, permisos, datos personales o se expone algo nuevo
- **`devops-hightower`** — solo si cambia el despliegue, entornos o migraciones

No los convoques por rutina. Si el ciclo fue una landing estática, ninguno de los tres aporta.

## Paso 4 — Retro corta

Cuatro preguntas. Nada de ceremonia:

1. **¿Acertaste el appetite?** ¿Sobró o faltó tiempo, y cuánto?
2. **¿Apareció algún rabbit hole que no habías previsto?** Este es el aprendizaje más
   valioso: los agujeros se repiten entre proyectos.
3. **¿Se coló algo que estaba en el no-go?** Si sí, ¿por qué se coló?
4. **¿Qué harías distinto en el próximo ciclo?** Una sola cosa, concreta.

## Paso 5 — Archivar

Mueve el ciclo a `.crew/historial.md` (créalo si no existe), añadiendo al final:

```markdown
## <fecha inicio> → <fecha fin> — <apuesta en una frase>
- **Appetite:** <tamaño> · **Real:** <días reales>
- **Resultado:** enviado | recortado y enviado | cancelado
- **Aprendizaje:** <la respuesta de la pregunta 4>
```

Después deja `.crew/estado.md` en cool-down:

```markdown
# Cool-down

**Desde:** <fecha> · **Hasta:** <fecha + 2 o 3 días>
**Último ciclo:** <apuesta> — <resultado>

**Anotado para la próxima apuesta:**
- <ideas que surgieron a mitad de ciclo y no entraron>
```

## Paso 6 — Actualizar el portfolio

Si el ciclo cambió el estado del proyecto (pasó a producción, consiguió el primer cliente,
cambió de fase), **recuerda actualizar `~/.claude/PORTFOLIO.md`**. Ofrece hacerlo tú y
enseña el cambio antes de escribirlo.

## Paso 7 — Proteger el cool-down

```
🚢 Ciclo cerrado — <proyecto>

<apuesta> — <resultado>
Appetite <tamaño>, real <n> días.

📚 Aprendizaje: <la respuesta de la pregunta 4>

🧊 Cool-down hasta el <fecha>
   Bugs sueltos, mantenimiento, probar cosas. Sin apuesta grande.
   El <fecha> decides la siguiente con /bet.
```

**Si el usuario quiere abrir otra apuesta hoy mismo, frénalo.** La siguiente apuesta
decidida el mismo día que acabas la anterior se decide por inercia, no comparando con
las alternativas. El cool-down es lo que impide que el portfolio se decida solo.

Si insiste tras esa advertencia, es su decisión: ábrela y no vuelvas sobre ello.
