# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Versionado según [SemVer](https://semver.org/lang/es/).

## [2.0.0] — 2026-09-06

Business Crew deja de ser una colección de agentes y pasa a tener **un ciclo de trabajo**.

### Añadido

- **Ciclo Shape Up** (skill `shape-up-cycle`) en lugar de ceremonias de Scrum: appetite en
  vez de estimación, hill chart en vez de porcentajes, circuit breaker contra el pulido
  infinito, cool-down obligatorio y ausencia deliberada de backlog.
- **Comandos del ciclo:** `/bet` (dar forma y apostar), `/hill` (posición en la colina y
  detección de atascos) y `/ship` (cierre, retro y archivado).
- **Estado persistente** en `.crew/estado.md` dentro de cada proyecto, con historial de
  apuestas en `.crew/historial.md`.
- **Hooks:** `SessionStart` recuerda la apuesta activa, los días consumidos y avisa si el
  punto de la colina lleva dos días sin moverse. `Stop` avisa solo si el appetite está
  vencido, y como mucho una vez al día.
- **Agente `director-arte`** y skill `design-direction`: brief obligatorio de cinco
  decisiones antes de construir interfaz, detección de la huella del diseño generado por IA
  (degradado índigo-morado, Inter por defecto, tres tarjetas en fila) y rúbrica de Awwwards
  (Diseño 40 · Usabilidad 30 · Creatividad 20 · Contenido 10). Enruta a las skills de diseño
  y animación ya instaladas en lugar de duplicarlas.
- **Agente `analista-datos`:** qué instrumentar, métrica única por tipo de producto, embudo
  mínimo de cinco pasos y distinción entre métricas de vanidad y accionables.
- **Skill `decision-framing`:** regla dura de no responder sí/no a una pregunta de producto.
  Se reformula a dos o tres caminos comparados, incluyendo siempre el de no construir nada.
- **`marketplace.json`** para instalar directamente desde el repositorio.
- **Diagramas Mermaid** en el README: ciclo, ciclo de vida de los hooks y enrutado del equipo.

### Cambiado

- `scrum-master` ahora protege el ciclo activo y trabaja con Shape Up, no con Scrum.
  Si hay apuesta abierta, lo que no pertenece a ella se anota para el cool-down.
- `pm-producto` incorpora la regla de comparar en lugar de evaluar.
- `ceo-bezos` enlaza la clasificación tipo 1 / tipo 2 con `decision-framing`.
- `/crew` tiene en cuenta el ciclo activo y enruta a los dos agentes nuevos.

### Corregido

- **`.gitattributes` fuerza LF en los `.sh`.** En Windows con `core.autocrlf=true` los
  scripts se convertían a CRLF al clonar y los hooks fallaban con `$'\r': command not found`.

## [1.0.0] — 2026-09-03

### Añadido

- 16 agentes con persona real, agnósticos de producto: cada uno con contrato de contexto
  (qué es el producto, quién lo usa, de qué tipo, en qué fase), ajuste de criterio por tipo
  de producto y una sección explícita de *cuándo NO aporta*.
- Comando `/crew`: convoca a los 2-4 roles relevantes, los lanza en paralelo y sintetiza
  mostrando dónde no están de acuerdo.
- `PORTFOLIO.template.md` como fuente de verdad de la cartera.

[2.0.0]: https://github.com/fernando-delrio/business-crew/releases/tag/v2.0.0
[1.0.0]: https://github.com/fernando-delrio/business-crew/releases/tag/v1.0.0
