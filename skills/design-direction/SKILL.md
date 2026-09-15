---
name: design-direction
description: El procedimiento de dirección visual: las cinco decisiones del brief, el control anti-slop y la rúbrica con la que se puntúa una interfaz. Úsala cuando toque ESTRUCTURAR o VALIDAR una dirección visual que ya está planteada. Si lo que hay es una insatisfacción vaga —«se ve soso», «le falta algo»— el primario es director-arte, que aporta el criterio y luego aplica esta skill.
---

# Dirección de arte

Esta skill no te enseña a animar ni a maquetar. Hay skills mejores para eso y probablemente
ya las tienes instaladas. **Esta skill decide qué se va a hacer antes de hacerlo, y sostiene
el listón mientras se hace.**

Es el hueco real: no falta conocimiento de diseño, falta alguien que fije el brief antes
de que el modelo empiece a generar por defecto.

---

## 1. Por qué el diseño generado por IA se reconoce a un kilómetro

El mecanismo tiene nombre: **convergencia distribucional.** Un modelo predice a partir de
patrones estadísticos, así que cuando la decisión queda abierta devuelve **la mediana de
sus datos de entrenamiento**. Y la mediana de "web moderna bonita" desde 2019 es la paleta
por defecto de Tailwind.

De ahí sale una huella reconocible:

| La huella | De dónde viene |
|---|---|
| **Degradado índigo → morado** | `indigo-500` por defecto. Es la señal más delatora que existe hoy |
| **Tipografía Inter** | El centro estadístico literal de "UI moderna" |
| **Tres tarjetas redondeadas en fila** | El layout de mínima resistencia |
| **Hero que valdría para otros diez mil productos** | Nadie eligió nada; se aceptó lo que salió |
| Emojis como iconos · sombras moradas · `rounded-2xl` en todo | Mismo origen |

Y hay un bucle: cuando un sitio llamativo con degradado morado tiene éxito, entra en el
siguiente entrenamiento y enseña al modelo que el morado es **aún más normal**.

> **El arreglo está documentado y es uno solo: restricciones explícitas ANTES de generar,
> no correcciones después.** Corregir después produce lo genérico con parches encima.

**Regla dura:** ninguna interfaz se empieza sin brief. Si el usuario dice "hazme una landing"
y no hay brief, tu primer trabajo es el brief, no la landing.

---

## 2. El brief — cinco decisiones antes de tocar código

Cada una elimina un grado de libertad donde el modelo caería en la mediana. Ninguna admite
"lo que veas mejor": **eso es exactamente lo que produce lo genérico.**

### 1. Referencia concreta
Dos o tres sitios reales, con URL. No adjetivos ("moderno", "limpio", "profesional"):
los adjetivos no restringen nada. Si el usuario no tiene referencias, mándale a buscarlas
con la lista de la sección 5 — **quince minutos mirando referencias ahorran tres iteraciones.**

### 2. Tipografía con nombre y voz
**Prohibida Inter por defecto.** No porque sea mala —es excelente— sino porque es la
respuesta que sale sola, y por tanto no comunica nada.

Elige por la voz que necesita la marca:

| Voz | Familias |
|---|---|
| Editorial, con autoridad | Instrument Serif, Fraunces, Newsreader, Playfair Display |
| Técnica, industrial | JetBrains Mono, Geist Mono, Space Grotesk, Chakra Petch |
| Neutral pero con carácter | Geist, Satoshi, General Sans, Söhne, ABC Diatype |
| Cálida, cercana | Nunito, Work Sans, Bricolage Grotesque |
| Contraste editorial | Serif de display + sans de cuerpo. Dos familias, no más |

### 3. Color con origen, no con gusto
**Prohibido el degradado azul-morado.** El color debe venir de algún sitio real: el
material del oficio, el entorno físico del usuario, el producto, la historia de la marca.

Un color con origen se defiende y se recuerda. Un color elegido a ojo se cambia cada semana
porque nada lo sostiene.

Y define **roles**, no una paleta suelta → ver el agente `ui-duarte`, sección 3.

### 4. Un gesto memorable, uno solo
Lo que hace que alguien recuerde el sitio. Una transición, un detalle tipográfico, una
textura, un comportamiento al hacer scroll, un vacío deliberado donde todos ponen algo.

**Uno.** Dos gestos compiten entre sí y ninguno se recuerda.

### 5. Qué se niega a hacer
Las decisiones de omisión son las que más definen. Sin carrusel. Sin stock photos. Sin
modo oscuro en la v1. Sin iconos. Escribirlo evita reabrir la discusión cada semana.

---

## 3. La rúbrica — cómo se puntúa de verdad

Awwwards puntúa con cuatro criterios, y los pesos sorprenden a casi todo el mundo:

| Criterio | Peso | Qué mide de verdad |
|---|---|---|
| **Diseño** | **40%** | Composición, tipografía, color, consistencia del sistema |
| **Usabilidad** | **30%** | Navegación, claridad, rendimiento, accesibilidad, móvil |
| **Creatividad** | **20%** | Originalidad del concepto. Lo que nadie más hizo |
| **Contenido** | **10%** | Calidad de textos, imágenes, vídeo |

**Dos lecturas que cambian cómo trabajas:**

**Usabilidad + Contenido = 40%.** Casi la mitad de la nota no es estética. Un sitio
espectacular que va lento, no se navega o tiene textos de relleno **no gana**. El mito de
"premiado = espectacular" es falso y hace perder mucho tiempo.

**Creatividad es solo el 20%.** El concepto original importa, pero pesa la mitad que la
ejecución. Un concepto brillante mal ejecutado pierde contra uno sobrio impecable.

De más de 15.000 envíos al año, **menos de 365 ganan Site of the Day: alrededor del 2,4%.**
Dilo cuando alguien lo plantee como objetivo — no para desanimar, sino para que use la
rúbrica como listón de calidad, que es donde está el valor real.

### Puntuar un trabajo

Cuando revises una interfaz, puntúa los cuatro y **di cuál es el que más sube la nota
por unidad de esfuerzo**. Casi siempre es usabilidad o contenido, no diseño: son los que
todo el mundo descuida.

```
Diseño       __/40   <lo que falla>
Usabilidad   __/30   <lo que falla>
Creatividad  __/20   <lo que falla>
Contenido    __/10   <lo que falla>
             ──────
             __/100

Mayor retorno ahora: <el criterio y el cambio concreto>
```

---

## 4. Enrutado — no reimplementes lo que ya existe

Esta skill dirige. La ejecución es de otros. Cuando llegue el momento de construir,
**nombra la herramienta en vez de improvisar**:

| Necesidad | A dónde |
|---|---|
| Sistema visual: escala, roles de color, densidad, estados | agente `ui-duarte` |
| El flujo confunde al usuario | agente `ux-norman` |
| Construir la interfaz con criterio de diseño | skills `frontend-design`, `design-taste-frontend`, `high-end-visual-design` |
| Animación y movimiento | skills `animate`, `emil-design-eng`, `apple-design` |
| Auditar la animación existente | skills `review-animations`, `improve-animations` |
| Buscar dónde falta movimiento | skill `find-animation-opportunities` |
| Accesibilidad (parte del 30% de usabilidad) | skill `accessibility` |
| Rendimiento (también parte de ese 30%) | skill `performance` |
| Revisión contra guías de interfaz | skill `web-design-guidelines` |
| Generar referencias visuales antes de construir | skills `imagegen-frontend-web`, `imagegen-frontend-mobile` |

**Si alguna no está instalada, dilo y sigue con lo que haya.** No inventes su contenido.

---

## 5. Dónde buscar referencia

Awwwards es el escaparate, no la única fuente. Para diferenciarte hace falta mirar donde
no mira todo el mundo:

| Fuente | Para qué |
|---|---|
| **Awwwards** | El escaparate. Ojo: sesgado a espectáculo sobre producto |
| **Godly** | Curación más estricta y menos ruido |
| **SiteInspire** | El mejor filtrado por estilo, tipo y sector |
| **Land-book** · **Lapa Ninja** | Específicos de landings — el más útil si eso es lo que construyes |
| **Httpster** | Minimalismo tipográfico. Contención en vez de espectáculo |
| **Mobbin** · **Refero** · **Page Flows** | **Producto real, no marketing.** Para un SaaS valen más que Awwwards |
| **Typewolf** · **Fonts in Use** | Tipografía en uso real. La mejor cura contra Inter |
| **Brand New** | Identidad y marca |
| **Emil Kowalski** (emilkowal.ski, animations.dev) | Movimiento en producto real. Diseñador en Linear, autor de Sonner y Vaul |

**Regla al elegir referencia:** que sea del mismo *tipo* de producto. Copiar el movimiento
de una web de agencia premiada dentro de un panel de administración produce algo lento y
cansino a la tercera sesión.

---

## 6. Ajuste por tipo de producto

| Tipo | Dónde está el listón |
|---|---|
| **SaaS / herramienta** | Producto, no espectáculo. Densidad, velocidad, consistencia. Referencia: Mobbin y Linear, no Awwwards |
| **Landing / marketing** | Aquí sí caben el gesto memorable y el contraste tipográfico dramático. Es donde la rúbrica de Awwwards aplica más literalmente |
| **Ecommerce** | El producto manda; el sistema se aparta. La foto es el 80% del diseño percibido |
| **Portfolio** | El trabajo es el contenido. Un portfolio sobrediseñado tapa lo que quiere enseñar |
| **Contenido** | Tipografía de lectura y ritmo vertical por encima de todo |
| **Herramienta interna** | Optimiza para la sesión doscientos, no para la primera impresión. Aquí el espectáculo estorba |

---

## 7. Antes de dar por bueno cualquier trabajo

- [ ] ¿Hay brief escrito con las cinco decisiones? Si no, se hizo a ciegas
- [ ] ¿Alguna de las huellas de la sección 1? Inter por defecto, degradado morado, tres tarjetas
- [ ] ¿Se distingue de la competencia con una captura a 200px, sin logo?
- [ ] ¿Existen los ocho estados de componente? (ver `ui-duarte`)
- [ ] ¿Móvil de verdad, o escritorio encogido? Es el 30% de usabilidad
- [ ] ¿El movimiento tiene función, o es decoración que estorba a la tercera vez?
- [ ] ¿Los textos son reales, o "Lorem ipsum" con otra ropa? Es el 10% de contenido
- [ ] ¿Respeta `prefers-reduced-motion`?

**Fuentes:** [Sistema de evaluación de Awwwards](https://www.awwwards.com/about-evaluation/) ·
[Why AI Design Looks Generic](https://superdesign.dev/blog/why-ai-design-looks-generic) ·
[AI Slop Design Tells](https://www.925studios.co/blog/ai-slop-design-tells)

## Verification

El brief está listo cuando se cumple todo esto. Antes, no se construye.

- [ ] **Las cinco decisiones del brief están tomadas** (§2), ninguna como "lo que veas
      mejor"
- [ ] **Hay dos o tres referencias concretas con URL.** Si son adjetivos —"moderno",
      "limpio", "profesional"— **no hay brief**
- [ ] **La tipografía está elegida**, con un motivo que no sea "es la que había"
- [ ] **El color tiene origen**, no es un tono agradable al azar
- [ ] **Hay un gesto memorable, y solo uno**
- [ ] **Está escrito qué se niega a hacer** esta interfaz
- [ ] **Pasa el control anti-slop** (§1): sin degradado índigo-morado por defecto, sin la
      tipografía que viene de fábrica, sin tres tarjetas redondeadas como única idea
- [ ] **Puntuado con la rúbrica** (§3), y dicho **cuál sube más la nota por unidad de
      esfuerzo**
- [ ] **La ejecución está derivada** a la skill concreta (§4), sin improvisar su contenido

### Qué invalida el resultado

| Señal | Qué pasó |
|---|---|
| Referencias en forma de adjetivo | No hay restricción: saldrá la mediana estadística |
| Dos o más gestos memorables | Compiten y no se recuerda ninguno |
| Nota alta en estética y baja en contenido | Se puntuó lo que se pule, no lo que pesa (Diseño 40 / **Usabilidad 30** / Creatividad 20 / **Contenido 10**) |
| El brief se escribió después de maquetar | Es una justificación, no un brief |
| El flujo confunde y se maquilló | Un sistema visual precioso sobre un flujo roto sigue siendo un flujo roto → `ux-norman` |
