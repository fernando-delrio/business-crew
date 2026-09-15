# Quality gates

> **2026-09-09.** Hoy la palabra "gate" **no aparece en ningún archivo del repositorio**.
> La auditoría anterior los listó como fortaleza; verificado, no existen.

---

## 1. Qué es un gate aquí

Un gate es una **pregunta con respuesta comprobable** que se contesta `PASA` / `FALLA` /
`NO APLICA`, con la evidencia al lado.

| Es un gate | No es un gate |
|---|---|
| *"¿`npm test` termina en 0?"* → salida pegada | *"¿el código tiene calidad?"* |
| *"¿existe un ADR para esta decisión?"* → ruta del archivo | *"¿se ha pensado bien?"* |
| *"¿hay un número de volumen?"* → el número | *"¿está justificado?"* |

**Si un gate no se puede fallar objetivamente, no es un gate: es un recordatorio.** Y los
recordatorios no van en una lista de gates, van en el agente correspondiente.

**Regla de coste:** un gate que se marca `NO APLICA` más de tres veces seguidas está mal
puesto — o sobra, o pertenece a otro workflow.

---

## 2. Los ocho gates

### G1 · DISCOVERY GATE — antes de diseñar nada

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿Hay una conversación real registrada con la persona que pagaría? | Ficha en la fuente privada del proyecto |
| 2 | ¿Está descrito el proceso actual **paso a paso, con sus palabras**? | Cita textual |
| 3 | ¿Se sabe qué paga hoy por resolverlo? | Cifra o "nada", explícito |
| 4 | ¿Hay un volumen? (clientes/mes, avisos/día, expedientes/trimestre) | El número |
| 5 | ¿Está escrito qué NO entra? | Lista de no-go |

**Falla si:** el problema viene de una suposición, de un sector "parecido", o de una lista
escrita desde fuera del oficio.

> La regla que este gate hace comprobable es vieja y se enuncia sola: **la oferta sale de
> lo que diga quien tiene el problema, no de la lista de lo que sabemos hacer.**

### G2 · ARCHITECTURE GATE — antes de implementar algo caro de deshacer

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿La decisión es irreversible o cara de deshacer? Si sí → ¿hay ADR? | Ruta del ADR |
| 2 | ¿El ADR lista al menos una alternativa descartada con su motivo? | Sección del ADR |
| 3 | ¿Hay un número de escala real, no estimado? | El número |
| 4 | ¿Existe abstracción con **menos de dos** implementaciones reales? | Recuento |
| 5 | ¿Se puede volver atrás? ¿Cómo y en cuánto tiempo? | Descrito |

**Falla si:** hay una interfaz con una sola implementación, o un ADR que solo argumenta la
opción elegida.

### G3 · DATA GATE — antes de persistir el primer dato

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿De quién es cada dato? | Tabla de ownership |
| 2 | ¿Cuánto se conserva y quién lo decidió? | Política de retención |
| 3 | ¿Existe camino de **borrado** y de **exportación**, y están probados? | Prueba ejecutada |
| 4 | ¿Está clasificado qué es PII y qué es categoría especial? | Clasificación |
| 5 | ¿El audit trail guarda identificadores en lugar de contenido? | Muestra de una fila |
| 6 | ¿`tenant_id` desde la primera migración? | La migración |
| 7 | ¿Hay test de aislamiento entre tenants que pase? | Salida del test |

**Falla si:** se responde "ya lo definiremos". Es el gate más barato de pasar hoy y el más
caro de retrofitar.

### G4 · AUTOMATION GATE — ningún flujo se entrega sin esto

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿Idempotencia? ¿Qué pasa si el disparador llega dos veces? | Mecanismo descrito |
| 2 | ¿Rama de error? ¿Qué ocurre cuando el proveedor falla? | El flujo la tiene |
| 3 | ¿Política de reintentos, y qué **no** se reintenta? | Clasificación |
| 4 | ¿Fallback humano? ¿Quién se entera y cómo? | Handoff definido |
| 5 | ¿Observabilidad? ¿Se puede responder "¿salió el aviso?" sin entrar en n8n? | Consulta |
| 6 | ¿**Runbook manual**? ¿El negocio puede pasar el día con esto caído? | Runbook escrito |
| 7 | ¿El estado vive fuera del orquestador? | Dónde |

**Los siete son obligatorios.** Un flujo que falla en el 4 o el 6 no es una automatización:
es una dependencia.

### G5 · SECURITY GATE — antes de exponer nada

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿Secretos bajo seguimiento de git? | `git ls-files` |
| 2 | ¿Algún endpoint que mute estado sin autenticación? | Lista de endpoints |
| 3 | ¿Acceso entre tenants posible? | Test de aislamiento |
| 4 | ¿Webhooks críticos con firma verificada? | Verificación |
| 5 | ¿PII en logs? | Muestra |
| 6 | ¿Auditoría de dependencias limpia? | `npm audit` |

### G6 · UX GATE — antes de que lo vea un usuario real

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿Responsive comprobado en móvil real, no solo redimensionando? | Captura |
| 2 | ¿Contraste AA? | Comprobación ejecutada |
| 3 | ¿Estados de error, **con texto escrito por nosotros**? | Captura |
| 4 | ¿Estados de carga y de vacío? | Captura |
| 5 | ¿Navegable con teclado? | Comprobado |

**El punto 3 tiene nombre y fecha:** `Failed to fetch` en una demo real, en
producción, en inglés, durante días.

### G7 · QUALITY GATE — lo que el proyecto ya tenga

| # | Pregunta |
|---|---|
| 1 | ¿Typecheck en verde? |
| 2 | ¿Lint en verde? |
| 3 | ¿Tests en verde — **todos**, no "los que importan"? |
| 4 | ¿Build en verde? |
| 5 | ¿Se ejecutaron **en esta sesión**, con la salida pegada? |

**No se añade una herramienta solo para tener un gate que ejecutar.** Si el proyecto no
tiene linter, el gate es `NO APLICA`.

### G8 · BUSINESS GATE — el que más se salta

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿Qué comportamiento observable diría que esto funcionó? | La frase |
| 2 | ¿Está instrumentado, o al menos se sabe cómo se sabrá? | Evento o consulta |
| 3 | ¿Quién lo pidió? | Persona concreta, no "sería útil" |
| 4 | ¿Qué pasa si no se hace? | Consecuencia |

**Falla si** la respuesta a la 3 es *"quedaría bien"*. Es la pregunta de `analista-datos`,
convertida en barrera — y es el gate que un proyecto consumidor se saltó durante
entregas sucesivas: varios despliegues sin una sola métrica.

---

## 3. Qué gate aplica a qué workflow

| Gate | `/discover` | `/design` | build | `/release` |
|---|:--:|:--:|:--:|:--:|
| G1 DISCOVERY | ✅ | entrada | — | — |
| G2 ARCHITECTURE | — | ✅ | ✅ | — |
| G3 DATA | — | ✅ | ✅ | ✅ |
| G4 AUTOMATION | — | ✅ | ✅ | ✅ |
| G5 SECURITY | — | ✅ | — | ✅ |
| G6 UX | — | — | — | ✅ |
| G7 QUALITY | — | — | ✅ | ✅ |
| G8 BUSINESS | ✅ | ✅ | — | ✅ |
| **HUMAN** | — | ✅ decisiones | ✅ commit | ✅ deploy |

---

## 4. Cómo se contesta un gate

```markdown
## QUALITY GATES

G7 · QUALITY — PASA
  typecheck: exit 0
  tests:     todos en verde, ninguno omitido
  build:     dentro del budget declarado
  Ejecutado en esta sesión, con la salida real pegada.

G3 · DATA — NO APLICA
  No se persiste ningún dato en este cambio.

G8 · BUSINESS — FALLA
  Sin respuesta a "¿quién lo pidió?". Se para hasta tenerla.
```

**Un `FALLA` detiene el workflow.** No se anota como riesgo para seguir adelante: esa es
exactamente la forma en que un gate se convierte en decoración.

**La única excepción:** la autoridad humana puede levantar un gate explícitamente, y entonces se
registra como `DECISION` con su motivo. Un gate levantado a conciencia es una decisión; un
gate ignorado es un descuido.

---

## 5. Anti-burocracia

| Regla |
|---|
| Ocho gates en total. No se añade un noveno sin retirar uno |
| Un gate cabe en una tabla. Si necesita una página, es una skill |
| `NO APLICA` tres veces seguidas → el gate está mal asignado |
| Ningún gate pregunta por intenciones. Todos piden evidencia |
| Si contestar todos los gates cuesta más que el cambio, el cambio no necesitaba workflow |
