# Estructura objetivo del repositorio

> **2026-09-09.** La estructura del encargo se evalúa carpeta a carpeta. **Se rechazan tres.**

---

## 1. La propuesta del encargo, evaluada

```
business-crew/
  agents/ skills/ workflows/ rules/ templates/
  intelligence/ evals/ playbooks/ hooks/ scripts/ docs/
```

Once carpetas. Anti-bloat gate aplicado a cada una:

| Carpeta | ¿Contenido real hoy? | ¿Problema observado? | Decisión |
|---|---|---|---|
| `agents/` | 18 archivos | — | ✅ **Existe. Se queda** |
| `skills/` | 3 archivos | — | ✅ **Existe. Se queda** |
| `commands/` | 4 archivos | — | ✅ **Existe. Se queda** (el encargo la omitió) |
| `hooks/` | 1 archivo | — | ✅ **Existe. Se queda** |
| `scripts/` | 2 archivos | — | ✅ **Existe. Se queda** |
| `docs/` | Este directorio | Sí — no había dónde poner el diseño | ✅ **Se crea** |
| `rules/` | 3 archivos previstos | Sí — no hay contrato ni política de convocatoria | ✅ **Se crea** |
| `intelligence/` | 2 archivos previstos | Sí — el repo no ha aprendido nada en 2 commits | ✅ **Se crea** |
| `evals/` | 3 elementos previstos | Sí — cero evaluación, colisión probable | ✅ **Se crea** |
| `templates/` | **1 archivo** | 🟡 Marginal | 🟡 **Se aplaza** — ver §3 |
| `workflows/` | 3 archivos previstos | Sí | ❌ **Se rechaza como carpeta** — ver §3 |
| `playbooks/` | **0 archivos** | ❌ Ninguno | ❌ **Se rechaza** |

**Once propuestas → nueve carpetas, de las cuales cinco ya existen.** Se crean cuatro.

---

## 2. La estructura propuesta

```
business-crew/
├── agents/          18 personas · el QUIÉN
├── skills/          procedimientos · el CÓMO
├── commands/        puntos de entrada · el CUÁNDO  ← aquí viven los workflows
├── rules/           restricciones siempre activas  ← NUEVO
├── intelligence/    patrones generalizados         ← NUEVO
├── evals/           que esto funcione de verdad    ← NUEVO
├── docs/            diseño y decisiones            ← NUEVO
├── hooks/           lo que pasa sin que nadie lo pida
├── scripts/         lo determinista
└── .claude-plugin/  metadatos
```

**Diez directorios, cuatro nuevos, cero vacíos.**

---

## 3. Los tres rechazos, con argumento

### ❌ `workflows/` — porque un workflow **es** un comando

`agent-skills` es explícito: *"Slash commands — user-facing entry points. The **when**. The
orchestration layer."* Un workflow sin punto de entrada no se puede invocar; con punto de
entrada, **es** un comando.

Tener `commands/ship.md` y `workflows/release.md` como cosas distintas crea dos sitios
donde buscar lo mismo y la garantía de que se desincronizan.

> **Decisión:** `/discover`, `/design` y `/release` van a `commands/`, junto a `/bet`,
> `/hill`, `/ship` y `/crew`. **Siete comandos, un solo sitio.**

Y resuelve de paso la colisión de `/ship`: al estar los siete juntos, es imposible no verla.

### ❌ `playbooks/` — cero contenido

No hay ni un playbook, ni un caso observado que lo pida. Un directorio vacío en un repo
público es una promesa sin cumplir.

Y si lo hubiera, sería: ¿un playbook es un procedimiento (→ `skills/`) o una secuencia
coordinada (→ `commands/`)? **Sin un caso real no se puede responder**, y crear la carpeta
sin poder responder garantiza que acabe siendo el cajón de sastre.

> **Disparador:** cuando exista algo que no sea ni skill ni comando ni regla, se vuelve a
> plantear.

### 🟡 `templates/` — aplazada, con un único archivo previsto

El único candidato real es la plantilla de ADR. Un directorio para un archivo es ruido.

**Decisión:** la plantilla de ADR vive **dentro de la skill que la usa**
(`skills/decision-framing/adr-template.md`), como material de apoyo — que es exactamente el
patrón de `agent-skills`: *"material used by exactly one skill is a supporting file inside
that skill's directory"*.

> **Disparador para crear `templates/`:** cuando haya **tres** plantillas usadas por más de
> una skill o comando.

Nota: `PORTFOLIO.template.md` ya vive en la raíz y ahí se queda. Moverlo rompería los
enlaces de los 18 agentes que lo referencian, a cambio de nada.

---

## 4. Contrato de cada directorio

### `agents/` — el QUIÉN

| | |
|---|---|
| **Propósito** | Un rol con perspectiva, criterio y límites |
| **Permitido** | Un `.md` por persona. Frontmatter `name`/`description`/`model`. Secciones de contexto, método, ajuste por producto, *"Cuándo NO aportas"* y **output verificable** |
| **Prohibido** | Reproducir el contenido de una skill (el caso `director-arte`) · enrutar a otros agentes (no se puede ejecutar) · procedimientos paso a paso (eso es una skill) |
| **Owner** | Mantenedor. Alta y baja por `agent-audit.md` §4 |
| **Criterio de baja** | Sin invocar en 4 ciclos, o colisión ≥75 % con otro |

### `skills/` — el CÓMO

| | |
|---|---|
| **Propósito** | Un procedimiento repetible con criterio de salida |
| **Permitido** | `skills/<nombre>/SKILL.md` ≤500 líneas. Anatomía: Overview · When to Use · Core Process · Common Rationalizations · Red Flags · **Verification**. `scripts/` y `references/` **solo si se usan** |
| **Prohibido** | Skills sin Verification · directorios `scripts/` vacíos · duplicar una skill instalada fuera · conocimiento específico de un cliente |
| **Owner** | Mantenedor, vía `skill-promotion.md` |
| **Criterio de baja** | Sin invocar en 4 ciclos, o su contenido pasa a estar cubierto fuera |

### `commands/` — el CUÁNDO

| | |
|---|---|
| **Propósito** | Punto de entrada y capa de orquestación. **El único sitio que puede convocar capacidades** |
| **Permitido** | Un `.md` por comando, con `description` y `argument-hint`. Convoca agentes, lee skills, aplica gates |
| **Prohibido** | Lógica de negocio que debería ser skill · convocar más de 3 capacidades sin justificarlo · duplicar el nombre de otro comando |
| **Owner** | Mantenedor |
| **Criterio de baja** | Por workflow, en `workflow-design.md` §7 |

### `rules/` — lo siempre activo

| | |
|---|---|
| **Propósito** | Restricciones que aplican sin invocación |
| **Permitido** | **Tres archivos:** `orchestration.md` (contrato de evidencia + mapa de intención + minimum necessary crew) · `human-authority.md` · `model-routing.md` |
| **Prohibido** | Procedimientos (→ skill) · criterio de dominio (→ agente) · un cuarto archivo sin retirar otro |
| **Owner** | Mantenedor |
| **Criterio de baja** | Una regla que nunca ha cambiado una decisión |

### `intelligence/` — lo aprendido

| | |
|---|---|
| **Propósito** | Patrones generalizados que valen en otro proyecto |
| **Permitido** | `patterns.md` (≤300 líneas) y `candidates.md`. **Solo** contenido genérico y anónimo |
| **Prohibido** | 🔴 **Nombres de clientes · teléfonos · correos · citas identificables · nombres de negocio reales · cualquier PII.** El repositorio es público con licencia MIT |
| **Owner** | Mantenedor, en el cool-down |
| **Criterio de baja** | Patrón sin aplicar en 6 meses, o ascendido a skill |

### `evals/` — que esto funcione

| | |
|---|---|
| **Propósito** | Comprobar que las capacidades se disparan cuando deben |
| **Permitido** | `README.md`, `cases/<nombre>.json`, `fixtures/<escenario>/` |
| **Prohibido** | 🔴 **Datos reales en los fixtures.** Sectores sí, negocios no · bajar un umbral para que pase una regresión |
| **Owner** | Mantenedor |
| **Criterio de baja** | Si en 2 ciclos ningún fallo produjo un cambio real |

### `docs/` — diseño y decisiones

| | |
|---|---|
| **Propósito** | Por qué el sistema es como es |
| **Permitido** | `docs/vX.Y/` por iteración de diseño |
| **Prohibido** | Documentación de un proyecto consumidor o de un cliente · restatear lo que una skill ya dice (se enlaza) |
| **Owner** | Mantenedor |
| **Criterio de baja** | Una versión cuyo diseño se implementó o se descartó se archiva, no se borra |

### `hooks/` y `scripts/`

| | |
|---|---|
| **Propósito** | Lo que ocurre sin que nadie lo pida · lo determinista |
| **Permitido** | `hooks.json` · scripts `bash` con `set -e`, mensajes a stderr, salida legible a stdout |
| **Prohibido** | Hooks que escriban en el repo sin decirlo · scripts que necesiten credenciales |
| **Owner** | Mantenedor |
| **Criterio de baja** | Un hook que molesta más de lo que avisa |

---

## 5. Regla transversal

> **Ningún directorio se crea vacío.** Se crea con su primer contenido real.

Aplicado a este plan: `rules/`, `intelligence/` y `evals/` **no se crean en esta fase** —
se crean cuando se escriba su primer archivo, en la fase de implementación.

Esta fase solo crea `docs/v0.2/`, que es donde estás leyendo.

---

## 6. Comparación

| | Encargo | Propuesta | Diferencia |
|---|--:|--:|---|
| Directorios | 11 | **10** | −`workflows` −`playbooks` −`templates` +`commands` |
| Nuevos a crear | 6 | **4** | Tres rechazados con argumento |
| Vacíos | 1-2 | **0** | Regla de §5 |
| Sitios donde buscar un workflow | 2 | **1** | `commands/` |
| Sitios donde buscar una plantilla | 1 | 1 | Dentro de su skill |
