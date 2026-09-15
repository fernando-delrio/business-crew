# Telemetría de uso — diseño, no implementación

> **2026-09-14. Diseño únicamente.** No se toca ningún hook.

---

## 1. La pregunta que hoy no se puede contestar

> **¿`ceo-bezos` se usa? ¿Y `analista-thompson`?**

Ambos están marcados como candidatos a retirada desde el diseño de v0.2, **con un criterio
que no se puede aplicar** porque nada se mide. Retirarlos hoy sería una opinión; mantenerlos
sin datos, también.

Y hay una segunda pregunta, que es la que de verdad importa:

> **Cuando el sistema deriva a una capacidad, ¿acierta?**

El Tier 2 mide si un algoritmo léxico la elegiría. **No mide si la elección sirvió.**

---

## 2. Anti-bloat gate

Antes de proponer nada, porque la telemetría es el sitio clásico donde se construye
infraestructura para datos que nadie mira.

| Pregunta | Respuesta |
|---|---|
| ¿Problema observado? | ✅ Dos decisiones pendientes desde v0.2 no se pueden tomar |
| ¿Existe ya? | ❌ Cero |
| ¿Sección de otro archivo? | ✅ **Sí: el registro es un archivo de texto en `.crew/`, no un sistema** |
| ¿≥2 usos? | ✅ Retirada de capacidades + validación del enrutado |
| ¿Owner? | ✅ Mantenedor, en el cool-down |
| ¿Criterio de eliminación? | ✅ **Si en 2 ciclos nadie lo rellena, se retira** |

**Pasa, pero la respuesta a la tercera pregunta manda sobre todo lo demás:** esto tiene que
ser un archivo, no una plataforma.

---

## 3. Qué se registra

Una línea por invocación. Seis campos.

```
fecha | workflow | capacidad | rol | por_qué | resultado
```

| Campo | Valores | Por qué |
|---|---|---|
| `fecha` | `2026-09-14` | Día, no hora: la hora no responde ninguna pregunta y acerca a identificar a una persona |
| `workflow` | `crew` · `bet` · `hill` · `ship` · `directo` | Distingue invocación por comando de invocación suelta |
| `capacidad` | el nombre | Lo que se quiere contar |
| `rol` | `primary` · `secondary` | Comprueba el techo de 3 y el *minimum necessary crew* |
| `por_qué` | `mapa` · `pedida` · `derivada` · `intuición` | **El campo más valioso.** `intuición` repetido significa que el mapa de enrutado no cubre ese caso |
| `resultado` | `util` · `parcial` · `no-aporto` · `equivocada` | La señal de calidad |

### Ejemplo

```
2026-09-14 | directo | cfo-precios      | primary   | mapa      | util
2026-09-14 | crew    | munger-critico   | secondary | derivada  | util
2026-09-14 | crew    | ceo-bezos        | secondary | intuición | no-aporto
2026-09-15 | directo | coo-graham       | primary   | intuición | equivocada
```

La cuarta línea es la que más enseña: alguien fue a `coo-graham` por intuición y se
equivocó. Repetida tres veces, **es el hueco de automatización apareciendo en datos** en
vez de en un documento.

### Distinción `no-aporto` vs `equivocada`

| Valor | Significa | Qué implica |
|---|---|---|
| `no-aporto` | Era la capacidad correcta y no dijo nada útil | Problema de **contenido** |
| `equivocada` | No era la capacidad correcta | Problema de **enrutado** |

Sin separarlas, un mal enrutado se lee como un mal agente y se retira al inocente.

---

## 4. Dónde vive

**`.crew/uso.md` — por proyecto, fuera de git.**

| | |
|---|---|
| Por qué en `.crew/` | Ya existe, ya está en `.gitignore`, y ya es donde vive el estado del ciclo |
| Por qué fuera de git | El patrón de uso de quien lo usa es información suya. `business-crew` es **público** |
| Por qué no en el repo | Un repo público con el registro de qué consulta su autor cada día es exactamente lo que no debe estar ahí |

---

## 5. PII

**Cero.** El registro guarda **nombres de capacidad y categorías**, nunca el contenido de
la consulta.

| No se registra | Por qué |
|---|---|
| El texto de la pregunta | Contendría nombres de clientes, precios, detalles de negocio |
| Nombres de proyecto o de cliente | Son de terceros |
| La respuesta | Idem |
| Hora exacta, duración, sesión | No responde ninguna pregunta y acerca a un perfil de actividad |

**La prueba:** el registro entero debe poder pegarse en un issue público sin revelar nada.
Si una línea no pasa esa prueba, sobra el campo que la rompe.

---

## 6. Cómo se rellena

Tres opciones, de menos a más automática. **La recomendación es la primera.**

| # | Cómo | Coste | Fiabilidad |
|---|---|---|---|
| **1** | **A mano, al cerrar la sesión.** Una línea | Segundos | 🟡 Depende de que se haga |
| 2 | El hook de `Stop` pregunta y añade la línea | Bajo | 🟡 Fricción al cerrar |
| 3 | El hook detecta la invocación y registra automáticamente | Medio | 🔴 `por_qué` y `resultado` **no se pueden detectar**: son juicio |

**Se propone la 1.** Los dos campos con más valor —`por_qué` y `resultado`— **no son
observables**: solo los sabe la persona. Automatizar los cuatro que sí lo son y dejar
vacíos los dos que importan produce un registro que parece medición y no lo es.

Y encaja con `coo-graham`: con cero clientes y un operador, esto es exactamente una tarea
de volumen bajo que se hace a mano. Automatizarla antes sería automatizar el proceso
equivocado.

---

## 7. Qué se contesta, y cuándo

En el cool-down, con **dos ciclos** de datos:

| Pregunta | Cómo se contesta |
|---|---|
| ¿Se usa `ceo-bezos`? | Contar sus líneas. **Cero en 2 ciclos → se archiva** |
| ¿Se usa `analista-thompson`? | Igual |
| ¿El mapa de enrutado sirve? | Proporción de `mapa` frente a `intuición` |
| ¿Hay un hueco de capacidad? | `intuición` + `equivocada` repetidos sobre la misma consulta |
| ¿Se respeta el techo de 3? | Contar `secondary` por decisión |
| ¿Alguna capacidad no aporta nunca? | `no-aporto` mayoritario → problema de **contenido**, no de enrutado |

### Umbral de decisión, escrito ahora

| Observación en 2 ciclos | Acción |
|---|---|
| 0 invocaciones | Se archiva |
| 1-2 invocaciones, todas `util` | **Se mantiene.** Poco usado ≠ inútil: `legal-basico` se usará dos veces al año y una evitará un problema caro |
| ≥3 invocaciones con `no-aporto` mayoritario | Se revisa su contenido |
| ≥3 `equivocada` | Se revisa el **mapa**, no el agente |

---

## 8. Lo que NO se construye

| No | Por qué |
|---|---|
| Base de datos | Son decenas de líneas al mes |
| Panel | El archivo se lee entero en un minuto |
| Métricas agregadas automáticas | Se cuentan a mano en el cool-down |
| Hook que registre solo | Los dos campos que importan no son observables |
| Tiempos, duraciones, tokens | No responden ninguna pregunta pendiente |
| Registro en el repo público | Ver §4 |

---

## 9. Cuándo implementarlo

**No en esta fase.** Precondiciones:

| # | Precondición | Estado |
|---|---|---|
| 1 | Aprobación humana | Pendiente |
| 2 | Que haya uso real que registrar | El sistema se acaba de reescribir |
| 3 | Que exista un ciclo abierto donde el cool-down tenga sentido | Pendiente |

**Y la prueba honesta antes de implementarlo:** ¿la persona operadora escribiría una línea al
cerrar una sesión? Si la respuesta es *"probablemente no"*, esto no se construye — se acepta que
las decisiones sobre capacidades se toman por criterio, y se dice así en lugar de montar un
registro vacío que da falsa sensación de medición.
