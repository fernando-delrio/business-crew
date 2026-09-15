# Contrato de salida

> Fuente de verdad de cómo se etiqueta una afirmación. **No dupliques estas
> definiciones dentro de un agente o una skill: enlaza aquí.**

---

## Por qué existe

Sin esto no se puede saber, leyendo una respuesta, qué está demostrado y qué es una
opinión razonable.

No es teórico. En un proyecto real, una bitácora afirmaba *"el camino de n8n, por fin
probado […] en el test se intercepta la petición"*. **Ese test no existía.** Una inferencia
razonable se escribió como hecho y estuvo días guiando decisiones.

---

## Las cuatro etiquetas obligatorias

| Etiqueta | Significa | Exige | Ejemplo |
|---|---|---|---|
| **FACT** | Verificado, con la evidencia al lado | El comando ejecutado, el archivo leído, la URL comprobada, la cita textual | *"Los despliegues responden 200 — comprobado con `curl`"* |
| **INFERENCE** | Se deduce de la evidencia, no está demostrado | Decir **de qué** se deduce | *"Los bundles pesan lo mismo → llevan la misma configuración"* |
| **RECOMMENDATION** | Curso de acción propuesto | La alternativa descartada **y su motivo** | *"Retirar el webhook en vez de levantar el orquestador — porque no hay cliente todavía"* |
| **UNKNOWN** | Dato necesario que falta | **Quién** lo consigue y **cómo** | *"Si el plan incluye eventos personalizados — panel del proveedor, lo comprueba la persona responsable"* |

### Las tres reglas que lo hacen funcionar

1. **Un `UNKNOWN` no se rellena con una `INFERENCE` para poder seguir.** Si falta un dato
   que cambia la conclusión, se para y se pide.
2. **Una `INFERENCE` presentada como `FACT` es un defecto**, no un matiz de estilo.
3. **Toda `RECOMMENDATION` lleva su descartada.** Sin alternativa es una preferencia
   disfrazada.

---

## Las tres opcionales

Se usan solo cuando aportan. Cada una tiene una condición.

| Etiqueta | Cuándo | Condición |
|---|---|---|
| **ASSUMPTION** | Es un `UNKNOWN` sobre el que se decide igual | Lleva **qué cambia si es falsa** |
| **RISK** | Algo que puede salir mal | Lleva **probabilidad × daño** y una mitigación ejecutable **esta semana** |
| **DECISION** | Se ha elegido un camino | Lleva **reversibilidad**: tipo 1 (cara de deshacer) o tipo 2 (reversible) |

**No hay más etiquetas.** `OPINION`, `NOTE`, `IDEA` u `OBSERVATION` no cambiarían ninguna
decisión: son las que convierten un contrato en burocracia.

---

## Cómo se usa

No hace falta etiquetar cada frase de una conversación. **Se etiquetan las conclusiones**:
lo que alguien podría citar mañana para justificar una decisión.

```markdown
FACT: los tests pasan — 66/66, ejecutado hoy
FACT: el bundle pesa 119 KB comprimido, budget 150
INFERENCE: no hay problema de peso todavía — pero crece con cada demo
UNKNOWN: si el plan del proveedor incluye eventos personalizados → lo comprueba la persona responsable
ASSUMPTION: el volumen del primer año está en decenas al mes
          → si fuera en miles, la decisión de hosting cambia
RECOMMENDATION: retirar el webhook de ejemplo
          → descartado levantar el orquestador: no hay cliente que lo pague
RISK: la clave sin rotar (media × medio) → rotarla esta semana
DECISION: se usa Postgres gestionado — tipo 2, la salida es un volcado
```

### Señal de que sobra

Si alguien empieza a rellenar etiquetas para cumplir en vez de para pensar, el contrato
estorba y hay que recortarlo.

---

## Alcance

Aplica a agentes, skills y comandos de este repositorio. Cada agente declara además su
**Output mínimo**: los campos concretos que produce. Este documento define el **vocabulario**;
el output mínimo define la **forma**.
