# Contribuir a Business Crew

Gracias por querer aportar. Este proyecto tiene una regla que lo gobierna todo, y conviene
leerla antes que cualquier otra cosa.

## La regla que lo gobierna todo

> **Ningún agente puede saber nada de un proyecto concreto.**

Los agentes no llevan dentro nombres de empresas, sectores, stacks ni competidores.
**Saben preguntar.** El conocimiento de proyecto vive en `~/.claude/PORTFOLIO.md`, que es
del usuario y no de este repositorio.

Esto no es purismo: un agente con un proyecto grabado dentro deja de servir para el
siguiente, y lo peor es que **no falla de forma visible** — responde con total confianza
sobre el proyecto equivocado.

Un pull request que meta "para tiendas de ropa haz X" dentro de un agente será rechazado.
Eso va en la sección de ajuste por tipo de producto, en abstracto.

## Anatomía de un agente

Todo agente en `agents/` sigue la misma estructura. Si añades uno, cópiala:

```markdown
---
name: nombre-en-kebab-case
description: Cuándo usarlo, en una o dos frases. Es lo único que se carga en cada
  sesión, así que tiene que decir con precisión cuándo activarlo y cuándo no.
model: sonnet | opus
---

Quién eres y cuál es tu premisa, en dos o tres líneas.

## Contexto — siempre antes de responder
1. Lee `~/.claude/PORTFOLIO.md` si existe.
2. Si no, dedúcelo del directorio actual.
3. Qué necesitas saber sí o sí. **Y la orden de preguntar en vez de inventar.**

## Tu método
Las heurísticas del rol. Concretas y accionables, no teoría.

## Ajuste por tipo de producto
Cómo cambia tu criterio en SaaS / ecommerce / landing / marketplace /
herramienta interna / contenido.

## Cuándo NO aportas
A qué otro agente o skill derivar. **Esta sección es obligatoria.**
```

### Por qué "cuándo NO aportas" es obligatorio

Es lo que impide que dieciocho agentes opinen de todo. Un equipo bueno sabe quién no tiene
por qué estar en esta conversación. Sin esa sección, `ventas-ross` te montaría un embudo
en una landing.

## Criterios de aceptación

| # | Criterio |
|---|---|
| 1 | ¿Cero referencias a proyectos, empresas, sectores o stacks concretos? |
| 2 | ¿Tiene sección de ajuste por tipo de producto? |
| 3 | ¿Tiene sección de "cuándo NO aportas" con derivaciones reales? |
| 4 | ¿El agente **opina**, sin escribir código ni ejecutar nada? |
| 5 | ¿La `description` dice con precisión cuándo activarlo? Es lo único siempre en contexto |
| 6 | ¿No duplica una skill que el usuario probablemente ya tenga? Deriva en vez de reimplementar |
| 7 | ¿Las afirmaciones fuertes llevan fuente enlazada? |

## Estilo

- **En español.** Los `name:` de agentes y skills, en kebab-case.
- **Tablas antes que párrafos** cuando haya que comparar cosas.
- **Concreto sobre abstracto.** "Se ve genérico" no vale; "no hay tipografía elegida, se
  está usando la que sale por defecto" sí.
- **Nada de relleno motivacional.** Si una línea no cambia una decisión, sobra.

## Fuentes

Business Crew se apoya en trabajo ajeno y lo cita. Si añades una afirmación fuerte
—una métrica, una regla, un porcentaje— **enlaza la fuente real**. No infografías, no
capturas: la fuente primaria.

## Antes de abrir el PR

```bash
# Los JSON parsean
python -c "import json;[json.load(open(f,encoding='utf-8')) for f in ['.claude-plugin/plugin.json','.claude-plugin/marketplace.json','hooks/hooks.json']]"

# Los scripts no tienen errores de sintaxis
bash -n scripts/cargar-ciclo.sh && bash -n scripts/recordar-cierre.sh

# Ningún .sh con CRLF (romperia los hooks fuera de Windows)
file scripts/*.sh | grep CRLF && echo "ARREGLALO" || echo "OK"

# Cero hardcodeo de proyectos
grep -rniE "weldix|kinovia|mi-empresa" agents/ skills/ commands/ && echo "RESIDUOS" || echo "OK"
```

## Commits

Semánticos: `feat(agents): ...`, `fix(hooks): ...`, `docs(readme): ...`,
`refactor(skills): ...`, `chore(ci): ...`.

## Licencia

Al contribuir aceptas que tu aportación se publique bajo [MIT](LICENSE).
