# Enrutado de modelo

> **2026-09-09.** Ya existe enrutado en el repo. Lo que falta es la política que lo explique.

---

## 1. Lo que ya hay

Los 18 agentes declaran `model` en su frontmatter. **No es una capa nueva: es una capa sin
documentar.**

| Modelo | Nº | Quiénes |
|---|--:|---|
| `opus` | **7** | `analista-thompson` · `ceo-bezos` · `dev-dhh` · `director-arte` · `munger-critico` · `ui-duarte` · `ux-norman` |
| `sonnet` | **11** | `analista-datos` · `cfo-precios` · `cmo-godin` · `coo-graham` · `devops-hightower` · `legal-basico` · `pm-producto` · `qa-bach` · `scrum-master` · `seguridad` · `ventas-ross` |

### ¿Está bien repartido?

Mayormente sí. El criterio implícito parece ser *"razonamiento sobre ambigüedad"*, y se
sostiene: `munger-critico` (pre-mortem sobre lo desconocido) y `ux-norman` (modelos
mentales) son razonamiento denso; `devops-hightower` (diagnóstico con tabla) y `qa-bach`
(charter) son más procedimentales.

**Tres asignaciones que merecen revisarse**, con argumento y sin cambiarlas aquí:

| Agente | Hoy | Observación |
|---|---|---|
| `seguridad` | sonnet | 🟠 Su output alimenta un gate que decide si algo se expone a internet. **Un falso negativo aquí es caro y silencioso.** Candidato a subir |
| `legal-basico` | sonnet | 🟠 Mismo argumento: detectar una señal de alarma que no se detecta sale caro. Y se invoca muy poco, así que subirlo apenas cuesta |
| `ceo-bezos` | opus | 🟡 Es candidato a retirada por infrautilización. Gastar el modelo caro en el agente que menos se usa |

---

## 2. La política

Por **tipo de trabajo**, no por persona. La pregunta que decide es:

> **¿Cuánto cuesta que esto salga mal, y cuánto cuesta descubrirlo tarde?**

| Nivel | Tipo de trabajo | Criterio |
|---|---|---|
| 🟢 **BAJO / RÁPIDO** | Clasificación, formato, transformaciones deterministas, rellenar plantillas, extraer campos, ejecutar y reportar comandos, aplicar una checklist | El resultado es **verificable de un vistazo**. Un error se ve al leerlo |
| 🟡 **ESTÁNDAR** | Análisis de un dominio, implementación con especificación clara, revisión de código, QA, redacción, diagnóstico con tabla de decisión | Hay criterio, pero **acotado y comprobable**. Un error se detecta con tests o revisión |
| 🔴 **ALTO RAZONAMIENTO** | Arquitectura, estrategia ambigua, seguridad, **decisiones irreversibles**, depuración compleja, pre-mortem, síntesis de fan-out | Un error es **caro, silencioso o irreversible**. No hay test que lo detecte |

### Reglas de asignación

| # | Regla |
|---|---|
| 1 | **Lo irreversible sube de nivel.** La reversibilidad manda sobre la dificultad aparente. Ver `decision-framing` |
| 2 | **Lo silencioso sube de nivel.** Si un error no lo detecta ningún test ni ninguna persona, hace falta más razonamiento |
| 3 | **Lo frecuente baja de nivel.** Algo que corre cien veces al día justifica optimizarse; algo dos veces al año, no |
| 4 | **La síntesis de un fan-out sube.** Reconciliar tres informes contradictorios es más difícil que producir cualquiera de ellos |
| 5 | **Si es determinista, no es un trabajo de modelo: es un script.** Nivel cero |

**La regla 5 es la que más ahorra.** Comprobar si una URL es un placeholder no necesita
modelo: necesita una expresión regular.

---

## 3. Aplicado a los workflows

| Workflow | Paso | Nivel |
|---|---|:--:|
| `/discover` | Preparar, registrar, formatear la ficha | 🟢 |
| | Analizar y decidir go/no-go | 🟡 |
| `/design` | Encuadrar, alcance | 🟡 |
| | **Arquitectura, automatización, datos, seguridad** | 🔴 |
| | **Síntesis del fan-out** | 🔴 (regla 4) |
| | **Pre-mortem** | 🔴 |
| | Redactar el ADR desde las decisiones tomadas | 🟢 |
| build | Plan e implementación | 🟡 |
| | **Depuración que no cede a la primera** | 🔴 |
| `/release` | Ejecutar verificación y reportar | 🟢 |
| | QA exploratorio, revisión | 🟡 |
| | **Seguridad** | 🔴 (regla 2) |
| | **Veredicto final antes del gate humano** | 🔴 |

**Un mismo workflow usa los tres niveles.** Por eso la política es por tarea y no por
agente — y por eso el enrutado por frontmatter, que es fijo por persona, es solo una
aproximación.

---

## 4. Lo que esta política NO hace

| No hace | Por qué |
|---|---|
| **Nombrar modelos concretos más allá de lo ya escrito** | Los `model:` de los 18 agentes ya existen y son una decisión tomada. Fijar más nombres en documentación es atarse a un catálogo que cambia |
| Cambiar las 18 asignaciones actuales | Funcionan. §1 señala tres a revisar, con argumento, y la decisión es del mantenedor |
| Prometer ahorro | No se mide el coste hoy. Prometer un porcentaje sería inventarlo |
| Enrutar automáticamente | No hay mecanismo. Es una guía de decisión, no un router |

---

## 5. Lo que se propone hacer, y es poco

| Acción | Coste |
|---|---|
| Escribir esta política como `rules/model-routing.md` | Un archivo |
| Revisar las tres asignaciones de §1 | Una decisión del mantenedor |
| Nada más | — |

**No se propone construir un enrutador.** Con 18 agentes que ya declaran su modelo y tres
workflows, una guía de decisión cubre el caso. Un router automático sería infraestructura
para un problema que no se ha medido — el error que `dev-dhh` está ahí para señalar.

---

## 6. Cuándo volver a esto

| Disparador | Qué haría falta |
|---|---|
| El coste mensual de modelos se vuelve visible en la cuenta | Medir antes de optimizar |
| Un workflow se ejecuta decenas de veces al día | Bajar de nivel sus pasos deterministas |
| Un fallo caro se rastrea a un modelo insuficiente | Subir ese paso y anotarlo como patrón |

**Hasta que ocurra alguno, esto es una página y no un sistema.**
