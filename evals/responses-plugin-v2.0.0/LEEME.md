# ⚠️ Respuestas del PLUGIN v2.0.0 — NO son el sistema actual

Estas respuestas salen de los agentes **instalados** (`business-crew` v2.0.0 del
marketplace), que **NO contienen los cambios de las fases 1 y 2**: sin `Output mínimo`,
sin descripciones reescritas, sin `rules/output-contract.md`.

**Sirven para una sola cosa:** comprobar que el validador determinista funciona sobre
texto real de agente y no produce falsos positivos absurdos.

**NO son un baseline de Tier 3.** Las dimensiones CONTRACT y VERIFICATION fallarán de
forma trivial porque esos contratos no existen en la versión instalada.

---

## Qué son exactamente estos archivos

| | |
|---|---|
| **Transcripción histórica** | Texto real producido por los agentes instalados en su momento |
| **Redacción mínima** | Dos nombres de proyecto → `[PROYECTO REDACTADO 1]` y `[PROYECTO REDACTADO 2]`. Numerados porque eran entidades distintas |
| **Conducta sin alterar** | Ni una afirmación, ni una cifra, ni una estructura, ni una omisión |
| **No es baseline** | Mide el sistema anterior a las fases 1 y 2 |

**Por qué se redactó:** este repositorio es público y MIT, y las respuestas nombraban
proyectos consumidores concretos. La frontera está en
[`../../docs/v0.2/project-boundaries.md`](../../docs/v0.2/project-boundaries.md).

Cada archivo redactado lo declara al final, en un comentario HTML:
`<!-- redactado: N tokens (tipo) -->`. El procedimiento completo lo imprime
`python evals/tier3_behavior.py --manifest`, paso 3.

**Por qué la redacción no invalida la sonda:** el validador determinista lee cifras y
etiquetas de contrato. Los identificadores sustituidos no eran ni lo uno ni lo otro, así
que **ninguna métrica cambia**. Lo que la sonda demuestra —que el validador no produce
falsos positivos sobre texto real— se sostiene igual.

Lo que **no** se ha hecho: retocar la respuesta para que puntúe mejor, recortar una
afirmación incómoda o arreglar una frase torpe. Una transcripción editada para quedar bien
no sirve como evidencia de nada.

---

Las respuestas del sistema actual irían en `evals/responses/`, que está vacía a
propósito. Ver [`../../docs/v0.2/tier3-baseline.md`](../../docs/v0.2/tier3-baseline.md).
