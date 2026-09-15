# Capacidad de datos

> **2026-09-09.** Este documento **corrige a la auditoría anterior**: el hueco de datos es
> mucho menor de lo que decía, y está en otro sitio.

---

## 1. La corrección

La auditoría anterior afirmó:

> *"H2 · No hay ningún rol de datos / persistencia. Nadie opina sobre modelo de datos,
> esquema, migraciones o retención."*

**Verificado contra lo realmente instalado — es falso en más de la mitad.**

| Capacidad | ¿Cubierta? | Por qué |
|---|:--:|---|
| Antipatrones de esquema | 🟢 **SÍ** | **`saas-toolkit:schema-reviewer`** — claves ajenas ausentes, tipos incorrectos para dinero, EAV, listas separadas por comas, índices, `SELECT *` |
| Estrategia de aislamiento multi-tenant | 🟢 **SÍ** | **`saas-multitenant-architecture`** — `tenant_id` compartido vs esquema por tenant vs BD por tenant, **con checklist IDOR por query** |
| Completitud de CRUD aislado y a escala | 🟢 **SÍ** | **`saas-crud-completeness`** |
| Modelado de entidades e invariantes | 🟡 parcial | `dev-dhh` de refilón |
| Migraciones | 🔴 no | Nadie |
| **Ownership del dato** | 🔴 **no** | **Nadie** |
| **Retención · borrado · exportación** | 🔴 **no** | **Nadie** |
| **Clasificación de PII** | 🔴 **no** | Repartida entre `seguridad` y `legal-basico`, sin dueño |
| **Qué va dentro de un audit trail** | 🔴 **no** | **Nadie** |
| Fronteras de analítica | 🟡 parcial | `analista-datos` dice "no registres PII", sin procedimiento |

Y hay un detalle que hace la corrección más contundente: la skill
`saas-multitenant-architecture` **nace de una auditoría real con 5 fugas IDOR encontradas y
corregidas en un día**. Es conocimiento pagado con bugs reales, ya instalado.

**Escribir una skill de "data/persistence" sería duplicar tres piezas que ya existen y
funcionan.** Ese es exactamente el error que el anti-bloat gate existe para impedir.

---

## 2. El hueco real

Lo que ninguna de las tres cubre no es el **esquema**: es el **ciclo de vida**.

| Pregunta | ¿Alguien la contesta? |
|---|:--:|
| ¿De quién es este dato — del negocio, de su cliente, nuestro? | ❌ |
| ¿Cuánto tiempo se conserva, y quién decidió ese plazo? | ❌ |
| ¿Cómo se borra a una persona que lo pide? | ❌ |
| ¿Cómo se le entrega a un cliente todo lo suyo al terminar? | ❌ |
| ¿Qué es PII, qué es categoría especial, y qué controles cambia eso? | ❌ |
| ¿Qué se guarda en el audit trail — identificadores o contenido? | ❌ |
| ¿Qué datos pueden salir hacia analítica y cuáles no? | ❌ |
| ¿Qué copia queda en los backups después de un borrado? | ❌ |

**Ninguna es de esquema.** Todas son de **ciclo de vida y responsabilidad**, y todas
aparecieron como bloqueantes en un diseño real — el escenario de un negocio con
requisitos documentales sensibles: documentación fiscal y laboral, con posibles datos de
categoría especial dentro, sin ownership ni retención definidos.

Además, hay un patrón ya observado dos veces: **el audit trail y los logs son donde la PII
se acumula sin que nadie lo decida.** Dos casos distintos (una auditoría real y un diseño de
observabilidad) llegaron a la misma conclusión por separado. Eso es señal de patrón, no de
anécdota.

---

## 3. Qué debe cubrir — y qué no

### Sí

| # | Decisión | Momento |
|---|---|---|
| 1 | **Inventario de datos** — qué se guarda, de quién es, para qué | Antes de la primera migración |
| 2 | **Clasificación** — operativo · identificación · contenido libre · documental sensible · categoría especial | idem |
| 3 | **Retención por clase**, con motivo (legal, operativo, o "porque sí" → entonces se acorta) | idem |
| 4 | **Camino de borrado** — qué se borra, qué se anonimiza, qué sobrevive en auditoría | idem |
| 5 | **Camino de exportación** — entregar a un cliente todo lo suyo | idem |
| 6 | **Contenido del audit trail** — identificadores y transiciones, nunca contenido | Al diseñarlo |
| 7 | **Frontera de analítica** — qué sale hacia una herramienta de terceros | Al instrumentar |
| 8 | **Límite de los backups** — el dato borrado sobrevive en las copias. Se documenta, no se ignora | Al definir retención |
| 9 | **Disparador de revisión profesional** — cuándo esto deja de ser técnico | Continuo |

### No — porque ya está cubierto

| Fuera | Quién lo cubre |
|---|---|
| Elegir estrategia de aislamiento | `saas-multitenant-architecture` |
| Checklist IDOR por query | `saas-multitenant-architecture` |
| Antipatrones de esquema, tipos, índices | `schema-reviewer` |
| CRUD completo y aislado a escala | `saas-crud-completeness` |
| Quién accede a qué | `seguridad` |
| Si hace falta un abogado | `legal-basico` |
| Qué métricas medir | `analista-datos` |

**La skill empieza donde acaban las otras tres, y lo dice en su primera línea.**

---

## 4. Forma: ¿agente, skill o workflow?

| Forma | ¿Encaja? | Razonamiento |
|---|:--:|---|
| **AGENT** | ❌ | El criterio ya está repartido y bien: `seguridad` (acceso), `legal-basico` (obligación), `analista-datos` (medición). Lo que falta es el **procedimiento** que los une antes de crear la primera tabla |
| **SKILL** | ✅ | Nueve decisiones en orden, con gate (G3) y artefacto (tabla de ownership + retención) |
| **WORKFLOW** | ❌ | Se invoca dentro de `/design`, no coordina capacidades |

### Decisión: **una skill delgada — `data-lifecycle`**

El nombre importa: **no** `data-persistence` ni `data-modeling`. Esos nombres invitan a
duplicar lo que ya existe; `data-lifecycle` declara la frontera desde el título.

**Anti-bloat gate:**

| Pregunta | Respuesta |
|---|---|
| ¿Problema observado? | ✅ Un negocio con documentación sensible, sin ownership ni retención. Bloqueante escrito |
| ¿Existe algo que lo resuelva? | 🟡 **Parcialmente** — tres piezas cubren esquema y aislamiento, **ninguna cubre ciclo de vida**. Por eso la skill es delgada |
| ¿Puede ser sección de otro archivo? | 🟡 Se evaluó meterlo en `seguridad`. **No**: `seguridad` revisa lo construido; esto decide antes de construir, y se invoca desde otro momento del workflow |
| ¿≥2 workflows lo usarán? | ✅ `/design` y `/release` (G3) |
| ¿Tiene owner? | ✅ Invocada por `/design`. Escala a `legal-basico` en los disparadores |
| ¿Criterio para eliminarla? | ✅ Si `saas-toolkit` publica una skill que cubra ciclo de vida, esta se retira |

### Tamaño objetivo: **≤ 150 líneas**

Es deliberadamente la mitad que `automation-architecture`. Una skill delgada que **enlaza**
a tres piezas existentes vale más que una gruesa que las reimprime — que es exactamente el
error de `director-arte` con `design-direction`.

---

## 5. Estructura propuesta

```
skills/data-lifecycle/
  SKILL.md          ≤ 150 líneas
```

| Sección | Contenido |
|---|---|
| **Overview** | Lo que las otras tres skills no cubren: de quién es el dato, cuánto vive, cómo se borra |
| **When to Use** | Antes de la primera migración de un proyecto con datos de terceros. **NO** para elegir aislamiento (→ `saas-multitenant-architecture`) ni para revisar un esquema (→ `schema-reviewer`) |
| **Core Process** | Las 9 decisiones de §3 |
| **Common Rationalizations** | Ver abajo |
| **Red Flags** | `deleted_at` en todas las tablas · PII en el audit trail · retención "indefinida" · sin camino de exportación · teléfono en los logs |
| **Verification** | El gate G3, sus siete puntos |

### Tabla de racionalizaciones

| Racionalización | Realidad |
|---|---|
| *"La retención la definimos cuando haya datos"* | Cuando haya datos ya hay una obligación en marcha y un borrado que no se puede hacer |
| *"`tenant_id` lo añado cuando entre el segundo cliente"* | Es la migración más cara que existe: todas las tablas y todas las consultas, con un cliente en producción |
| *"Guardo todo en el audit trail por si acaso"* | Se convierte en el mayor depósito de PII del sistema y el más difícil de borrar cuando alguien ejerce supresión |
| *"Borrado blando en todo, por seguridad"* | Hay que recordarlo en cada consulta, y el día que se olvida se filtra |
| *"Los backups ya los gestiona el proveedor"* | Y conservan el dato después del borrado. Eso se documenta, no se ignora |
| *"Exportar los datos ya lo haremos si lo piden"* | Si no se ha probado, no existe. Y se pide justo cuando el cliente se va enfadado |

---

## 6. Lo que NO se hace

| No | Por qué |
|---|---|
| Crear `data-persistence` o `data-modeling` | Duplicaría tres piezas instaladas |
| Crear un agente de datos | El criterio ya está repartido y funciona |
| Meter modelado de Postgres | `schema-reviewer` lo cubre mejor y con una fuente mejor |
| Dar plazos de retención concretos | **No es asesoramiento legal.** La skill da la estructura; los plazos los valida un profesional |
| Escribirla en esta fase | Ver `implementation-plan.md` |

---

## 7. Nota sobre la instalación de `saas-toolkit`

Durante la verificación apareció una anomalía ajena a este repo pero que afecta al
enrutado: **`saas-claude-toolkit` está cacheado dos veces** (`1.0.0` y `e1043df70418`), con
`saas-multitenant-architecture` duplicada en ambas.

Sumado a los cuatro agentes de ese toolkit registrados **dos veces** (sueltos en
`~/.claude/agents/` y como plugin, con contenido divergente), hay un problema real de
enrutado ambiguo.

No es de business-crew y no se toca aquí. Se anota porque **afecta a cualquier política de
convocatoria que se diseñe**: si dos definiciones del mismo revisor están activas, la
política no puede garantizar cuál responde.
