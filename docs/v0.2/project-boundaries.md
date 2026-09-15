# Frontera entre el core y el proyecto

> **2026-09-09** · saneado el **2026-09-14**.
> Qué vive en este repositorio y qué no puede entrar nunca.
>
> *Renombrado el 2026-09-14. El nombre anterior llevaba dentro el de un proyecto
> concreto, y eso ya violaba la frontera que este documento define: un core reutilizable
> no se nombra por uno de sus proyectos.*

---

## 1. Las tres capas

| Capa | Contiene | Visibilidad |
|---|---|---|
| **CORE** — este repositorio | **CÓMO TRABAJAMOS** — criterio, procedimientos, gates, orquestación, evaluación | 🌍 **Público, MIT** |
| **PROJECT CONTEXT** | **QUÉ CONSTRUIMOS** — producto, arquitectura, decisiones, configuración | 🔒 Privado, por proyecto |
| **PRIVATE INTELLIGENCE** | **CON QUIÉN Y POR CUÁNTO** — precios, clientes, conversaciones, competencia, métricas, credenciales, estrategia | 🔒 **Nunca en un repositorio público.** A menudo, fuera de git |

La frontera no es de tema: es de **generalidad**.

> Si valdría igual en otro proyecto, con otro cliente y en otro sector → **CORE**.
> Si describe este producto, su arquitectura o su configuración → **PROJECT CONTEXT**.
> Si menciona a una persona, un precio o un competidor → **PRIVATE INTELLIGENCE**.

---

## 2. La prueba

Antes de escribir algo en el core:

> **¿Podría leerlo un desconocido en GitHub sin enterarse de nada sobre los clientes de
> quien lo usa, sus precios o su estrategia comercial?**

Si la respuesta es no, no va aquí.

Es una prueba dura y es la correcta: el repositorio es **público y con licencia MIT**.

---

## 3. Casos decididos

| Contenido | Capa | Por qué |
|---|---|---|
| *"El orquestador vive después del commit y nunca es autoridad"* | **CORE** | Vale para cualquier orquestador y cualquier proyecto |
| Un ADR con el contexto de un producto concreto | PROJECT | Es la decisión de **ese** producto |
| La **plantilla** de ADR | **CORE** | El formato es genérico |
| *"Un placeholder se comporta como un valor real"* | **CORE** | Patrón. Anónimo y reutilizable |
| El relato de un fallo concreto, con fecha y archivo | PROJECT | Es la historia de ese producto |
| *"`tenant_id` desde la primera fila"* | **CORE** | Genérico |
| Un modelo de datos con sus tablas | PROJECT | Es el dominio de ese producto |
| **Una tabla de precios** | 🔴 **PRIVATE** | Estrategia comercial |
| *"El precio se calcula sobre el valor, no sobre el coste"* | **CORE** | Ya está en `cfo-precios`. Genérico |
| **Cuotas y comisiones de competidores concretos** | 🔴 **PRIVATE** | Inteligencia de mercado de un sector |
| Fixtures de eval por sector, anonimizados | **CORE** | Sin datos reales. Ver §5 |
| **Notas de conversaciones con personas reales** | 🔴 **PRIVATE** | Identificables. Fuera de git |
| **Listas de prospectos o clientes** | 🔴 **PRIVATE** | Nombres y teléfonos de terceros |
| Workflows de automatización de un cliente | PROJECT (el suyo) | Suyos |
| Credenciales | 🔴 **Ningún repositorio** | — |

---

## 4. Lo que nunca cruza al core

| 🔴 Prohibido | Motivo |
|---|---|
| Nombres de clientes, prospectos o negocios reales | El repositorio es público |
| Teléfonos, correos, direcciones | Datos personales |
| Citas textuales de conversaciones | Identificables |
| Precios, márgenes, cuotas | Estrategia comercial |
| Competidores concretos y lo que cobran | Inteligencia de mercado |
| Código de producción | Es el producto, no el método |
| Configuraciones de cliente | Datos de terceros |
| Credenciales, tokens, claves | Nunca, en ningún repositorio |
| **Rutas concretas hacia la inteligencia privada** | Decir *dónde* está es casi tan malo como publicarla |
| Volcados de base de datos, aunque sean "de prueba" | — |

### La regla sobre las rutas

Una documentación pública puede decir:

> *"la evidencia de discovery se obtiene de la fuente privada autorizada del proyecto"*

**No puede decir** en qué archivo, en qué carpeta ni en qué servicio está esa fuente.

---

## 5. El caso delicado: los sectores en los fixtures

Los fixtures de evaluación usan sectores reales de negocio local. **¿Cruza eso la frontera?**

**No, con tres condiciones:**

1. **Sector, no marca.** `peluqueria-citas`, nunca el nombre comercial de un negocio —
   aunque ese nombre sea ficticio, si está publicado y asociado a un proyecto, deja de ser
   anónimo.
2. **Cifras inventadas y redondas.** Nada que pueda confundirse con un precio real.
3. **Cero citas.** Ninguna frase salida de una conversación con una persona.

Un fixture que dice *"una peluquería con dos profesionales quiere que dejen de llamarla
para pedir hora"* describe un **problema de dominio**, no un cliente. Es lo que hace falta
para evaluar un workflow y no revela nada.

**Y el fixture más sensible —el de documentos— no necesita ningún dato real:** lo que pone
a prueba es si el sistema se detiene ante datos sensibles, y eso se comprueba con un
escenario inventado.

---

## 6. El flujo del conocimiento

```
PRIVATE INTELLIGENCE        PROJECT CONTEXT           CORE
(fuera de git)              (privado)                 (PÚBLICO)
      │                          │                        │
 conversación real          trabajo real            método genérico
      │                          │                        │
      │  ── se generaliza ──────►│                        │
      │     (sin nombres)        │                        │
      │                          │  ── ≥2 casos ────────► │
      │                          │     + se anonimiza     │
      │                          │                        │
      └────────── NUNCA directamente ───────────────────► ✗
```

**La flecha tachada es la regla.** Nada pasa de una conversación a un repositorio público
sin atravesar el filtro de generalización de
[`intelligence-lifecycle.md`](intelligence-lifecycle.md) §3.

### Cómo se comprueba

`scripts/check-boundary.sh` falla si aparece un patrón prohibido. Detecta regresiones
obvias, no sutiles, y **no sustituye al criterio**.

Tiene dos mitades, y la separación es el punto:

| Mitad | Qué busca | Dónde vive |
|---|---|---|
| **Estructural** | Importes, teléfonos, correos | En el script. **Público** |
| **Nominal** | Nombres comerciales, apellidos, localidades, competidores, rutas privadas | `.crew/frontera-denylist.txt`. **Fuera de git** |

**Por qué la segunda mitad no puede vivir en el script:** una lista de nombres de clientes
dentro de un repositorio público *publica los nombres de los clientes*. Sería cometer la
infracción mientras se escribe la comprobación que la persigue.

Los importes se permiten bajo `evals/`, por la condición 2 de §5: un caso de prueba sobre
precios necesita una cifra —inventada y redonda— para existir.

### El veredicto dice qué capa se ha mirado

| Salida | Significa | Exit |
|---|---|:--:|
| `FRONTERA: n hallazgos` | Hay algo, **o una comprobación falló al ejecutarse** | 1 |
| `ESTRUCTURAL OK · NOMINAL NOT_EVALUATED` | La capa estructural está limpia. **La nominal no se ha mirado** porque no hay denylist | 0 |
| `FRONTERA OK` | Las dos capas evaluadas y limpias | 0 |

**El caso del medio es el que importa.** En un clon público no hay denylist, así que ese es
el resultado normal — y decir ahí *«FRONTERA OK»* sería confundir *«la mitad que medí está
limpia»* con *«la frontera está limpia»*. Que es exactamente el error contra el que existe
este documento. Devuelve `0` para poder correr en CI público, pero no miente sobre qué
comprobó.

Y una propiedad que costó encontrar: si el `grep` de una regla **revienta**, el script lo
reporta como fallo, no como aprobado. Un check que se cae en silencio pasa siempre, y eso
es peor que no tener check.

---

## 7. Qué hacer cuando la frontera ya se ha cruzado

Ocurrió: la primera versión de estos documentos contenía precios reales, nombres de
competidores, un nombre comercial y una nota sobre dónde se guardan las conversaciones
con dueños de negocio.

**El documento que definía la frontera era el que más la cruzaba.** Merece decirse, porque
es el fallo típico: quien escribe la regla está inmerso en el proyecto y no ve que su
ejemplo es un dato privado.

El procedimiento que funcionó:

1. **Buscar sistemáticamente**, no de memoria: nombres propios, símbolos de moneda,
   nombres de competidores, rutas de archivo, referencias a un proyecto concreto.
2. **Clasificar cada aparición** antes de tocar nada: genérica · específica del producto ·
   comercial · operativa privada.
3. **Sustituir, no borrar.** La enseñanza se queda; el dato se va.
4. **Dejar un test** que falle si vuelve a entrar.

**El paso 3 es el que salva el documento.** Borrar el ejemplo deja una regla abstracta que
nadie sabe aplicar; sustituirlo por su forma genérica conserva las dos cosas.
