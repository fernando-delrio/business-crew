# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Versionado según [SemVer](https://semver.org/lang/es/).

## [2.1.0] — 2026-09-15

El equipo pasa de 18 opiniones a 18 **capacidades enrutables**, y el repositorio gana
**cómo se comprueba** que lo son.

### Añadido

- **Contrato de salida central** (`rules/output-contract.md`): `FACT` · `INFERENCE` ·
  `RECOMMENDATION` · `UNKNOWN`, más `ASSUMPTION`, `RISK` y `DECISION`. Los 18 agentes lo
  referencian en lugar de repetirlo.
- **Reglas de orquestación** (`rules/orchestration.md`): mapa de enrutado en lenguaje del
  problema, regla **DOMAIN FIRST / PROCEDURE SECOND** y *minimum necessary crew* — una
  capacidad por defecto, techo de tres, cero si quien pregunta ya sabe qué hacer.
- **`## Output mínimo` en los 18 agentes**, proporcional a cada función: no el mismo molde
  repetido.
- **Evaluador Tier 2** (`evals/tier2_similarity.py`): TF-IDF y similitud coseno sin
  dependencias, sobre dos espacios vectoriales —lo que enruta y la huella semántica— con
  las métricas `UNREACHABLE`, `MISSING`, `AMBIGUOUS`, `UNNECESSARY` y
  `FORBIDDEN-ABOVE-PRIMARY`.
- **Evaluador Tier 3** (`evals/tier3_behavior.py`): validadores deterministas de conducta
  sobre seis dimensiones, con severidades P0-P3 y una regla de transcripción que separa la
  conducta evaluada de los tokens privados.
- **Fixtures congelados:** 12 casos de enrutado, 8 de holdout, 12 de estilo externo y 12 de
  conducta. Más `evals/_selftest/`, que demuestra los validadores sobre respuestas
  sintéticas.
- **Documentación de arquitectura v0.2** (`docs/v0.2/`, 26 documentos): mapa de
  capacidades, contrato del orquestador, quality gates, autoridad humana, ciclo de vida de
  la inteligencia, promoción de skills, enrutado de modelos y los informes de cada fase.
- **Gate estructural de frontera** (`scripts/check-boundary.sh`): detecta importes,
  teléfonos y correos en el contenido publicable. La capa nominal —nombres, lugares,
  competidores, rutas privadas— se evalúa solo si existe una denylist privada fuera de git.

### Cambiado

- **Las 18 descripciones de agente**, reescritas en lenguaje del problema: empiezan por
  cómo lo diría quien tiene el problema y no sabe a quién llamar. Fuera las frases comodín
  del tipo *"sirve para cualquier tipo de producto"*.
- **Fronteras explícitas** en cada agente: a qué deriva y cuándo no aporta.
- **`scrum-master`** deja de ser un router —un subagente no puede convocar a otro— y pasa a
  guardián del ciclo que deriva a **una** capacidad y **nombra el hueco** cuando no existe.
- **`/crew`, `/bet`, `/hill` y `/ship`** declaran a qué momento del ciclo pertenecen.
  `/crew` contrasta **una decisión concreta**; para *"¿por dónde sigo?"* deriva a
  `scrum-master`.
- **Las 3 skills** (`decision-framing`, `design-direction`, `shape-up-cycle`) generalizan su
  descripción y añaden `## Verification`: qué evidencia demuestra que se aplicaron bien y
  qué invalida el resultado.
- **`director-arte`** deja de duplicar a `design-direction`; conserva el criterio y delega
  el procedimiento.

### Corregido

- **Cláusula MIT restaurada.** Un reemplazo global de texto había convertido
  `AUTHORS OR COPYRIGHT HOLDERS BE LIABLE` en una variante corrupta. El titular del
  copyright no cambia.

### Sobre las cifras de esta versión

- **Tier 2 es una prueba de regresión determinista, no una medida de precisión real.**
  Compara descripciones con TF-IDF; el harness real usa selección semántica. Sirve para
  detectar que un cambio empeora el enrutado, no para afirmar que el enrutado acierta.
- **El baseline Tier 3 real sigue `NOT_EVALUATED`:** 0 de 12 casos ejecutados contra el
  sistema actual. El examen existe y está probado contra sus propios casos sintéticos;
  ejecutarlo requiere que el plugin instalado refleje este repositorio.
- **La sonda guardada en `evals/responses-plugin-v2.0.0/` es histórica.** Mide la versión
  **2.0.0** instalada, anterior a estos cambios, y **no constituye el baseline de 2.1.0**.
  Existe para demostrar que el validador no produce falsos positivos sobre texto real.
- **La capa nominal del gate de frontera figura como `NOT_EVALUATED`** mientras no exista
  una denylist privada: el gate informa `ESTRUCTURAL OK - NOMINAL NOT_EVALUATED`, que es un
  aprobado parcial y no una afirmación sobre la frontera entera.

## 2.0.0 — 2026-09-06

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

## 1.0.0 — 2026-09-03

### Añadido

- 16 agentes con persona real, agnósticos de producto: cada uno con contrato de contexto
  (qué es el producto, quién lo usa, de qué tipo, en qué fase), ajuste de criterio por tipo
  de producto y una sección explícita de *cuándo NO aporta*.
- Comando `/crew`: convoca a los 2-4 roles relevantes, los lanza en paralelo y sintetiza
  mostrando dónde no están de acuerdo.
- `PORTFOLIO.template.md` como fuente de verdad de la cartera.

[2.1.0]: https://github.com/fernando-delrio/business-crew/compare/6d95f9beadeba3218f41eea58f2d0d6cd3b57230...v2.1.0
