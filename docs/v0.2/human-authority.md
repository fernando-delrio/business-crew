# Autoridad humana

> **2026-09-09.** Qué exige autoridad humana, y qué barrera lo garantiza.

---

## 1. La barrera que ya existe — y que no se toca

`~/.claude/settings.json` deniega a nivel de programa:

```
Bash(git add)      Bash(git add:*)      Bash(git add *)
Bash(git commit)   Bash(git commit:*)   Bash(git commit *)
Bash(git push)     Bash(git push:*)     Bash(git push *)
```

El razonamiento está registrado en la bitácora del 06/09:

> *"La regla «Claude nunca hace commit» existía solo como texto en las instrucciones. Un
> `deny` es una barrera del programa, no una norma que el agente tenga que recordar en
> cada sesión."*

**Y funcionó.** El 09/09, con aprobación humana explícita para hacer una serie de
commits y un push, la barrera bloqueó el `git add`. El trabajo se detuvo y se le devolvieron los
comandos.

Eso es exactamente lo que tenía que pasar. **Una barrera que se puede rodear cuando el
resultado interesa no es una barrera.**

> **Esta política no propone levantarla, ni siquiera "temporalmente" ni "solo para esta
> fase".** Si algún día hay que cambiarla, se cambia en `settings.json` a mano, por
> decisión consciente, y se registra.

---

## 2. Los tres niveles

| Nivel | Significa | Barrera |
|---|---|---|
| 🔴 **BLOQUEADO** | Claude **no puede**, aunque se le pida | `deny` en `settings.json` |
| 🟠 **APROBACIÓN PREVIA** | Claude puede, pero pregunta **antes** y espera respuesta | Política + gate HUMAN |
| 🟢 **AUTÓNOMO** | Claude hace y reporta | — |

La diferencia entre 🔴 y 🟠 importa: el rojo es una barrera del programa; el naranja
depende de que el agente la respete. **Lo irreversible y lo externo van en rojo cuando se
puede.**

---

## 3. La tabla

| Acción | Nivel | Por qué |
|---|:--:|---|
| **`git add` · `commit` · `push`** | 🔴 | Barrera existente. No se toca |
| **Merge a rama principal** | 🟠 | No está en el `deny`, pero es irreversible de hecho. **Candidato a pasar a 🔴** |
| **Deploy a producción** | 🟠 | Lo ve un cliente. Hoy lo dispara un push, que ya está en rojo |
| **Gasto** — contratar servicio, comprar dominio, subir de plan | 🔴 de hecho | Requiere tarjeta. Claude propone; la autoridad humana aprueba y realiza el pago |
| **Alta de proveedor** (Supabase, n8n Cloud, WhatsApp API) | 🟠 | Compromiso contractual + DPA + datos de terceros |
| **Borrar datos** | 🟠 | Irreversible. Exige exportación previa verificada |
| **Migración destructiva** (`DROP`, `ALTER` que pierde datos) | 🟠 | Exige rollback probado |
| **Tocar producción** — editar un registro, ejecutar SQL en la BD real | 🟠 | Sin red de seguridad |
| **Enviar comunicaciones reales** — correo, WhatsApp, publicar en redes | 🟠 | Va a una persona real y no se deshace |
| **Decisiones legales** — aceptar cláusula, firmar, publicar textos legales | 🔴 conceptual | No es competencia de Claude |
| **Cambiar precios** | 🟠 | Es la oferta del negocio |
| **Publicación pública** — publicar repo, release, redes | 🟠 | No se deshace: queda indexado y cacheado |
| **Rotar o crear credenciales** | 🟠 | Requiere paneles externos |
| Escribir y editar archivos | 🟢 | `defaultMode: acceptEdits` |
| Ejecutar tests, build, lint | 🟢 | Reversible, sin efecto externo |
| Leer, buscar, analizar | 🟢 | — |
| Crear documentación | 🟢 | Reversible |
| Ejecutar git de solo lectura (`status`, `diff`, `log`) | 🟢 | Ya permitido |

---

## 4. Cómo se pide una aprobación

Dentro del `DECISIONS REQUIRED` del contrato del orquestador. No como una pregunta suelta
al final de un texto largo.

```markdown
## DECISIONS REQUIRED

### 1. 🟠 Alta en Supabase — plan de pago

**Qué:** contratar el plan X para el piloto.
**Por qué ahora:** bloquea C0 del roadmap.
**Coste:** <cifra> al mes.
**Alternativa descartada:** Postgres autogestionado — más barato en dinero,
más caro en operación (parches, backups, monitorización).
**Irreversibilidad:** tipo 2 — se puede migrar con `pg_dump`.
**Necesito de ti:** que lo contrates, o que digas que no y por qué.
```

Cinco campos: qué · por qué ahora · coste · alternativa · reversibilidad. Sin ellos no es
una petición de aprobación: es una pregunta.

---

## 5. Las tres reglas que evitan el desgaste

Una política que pide permiso para todo se ignora en una semana.

| Regla | |
|---|---|
| **1 · La aprobación no se hereda entre contextos** | Aprobar un commit no aprueba el siguiente. Aprobar un proveedor no aprueba subir de plan |
| **2 · Lo reversible no se pregunta** | Si Claude puede deshacerlo solo y nadie externo lo vio, se hace y se reporta. Preguntar por lo reversible entrena a la autoridad humana a decir "sí" sin leer — **y eso es lo que rompe la política** |
| **3 · Las aprobaciones se agrupan** | Todas las de una ejecución juntas, al final, en `DECISIONS REQUIRED`. No goteando |

**La regla 2 es la que sostiene a las otras dos.** La utilidad de una barrera depende de
que se lea lo que hay detrás.

---

## 6. Qué NO requiere autoridad humana

Merece decirse porque el riesgo opuesto —parálisis— también es real:

| No requiere aprobación |
|---|
| Escribir, editar y reorganizar documentación |
| Ejecutar la batería de verificación |
| Proponer arquitectura, escribir ADRs, diseñar workflows |
| Investigar, leer repositorios, comparar alternativas |
| Preparar los comandos exactos de algo que él ejecutará |
| Decir que algo está mal, aunque lo haya decidido él |

**La última importa:** la política es sobre **acciones**, no sobre **opiniones**. Que
la autoridad humana apruebe una arquitectura no obliga a Claude a dejar de señalar un fallo en ella.

---

## 7. Lo que esta política no resuelve

| Hueco | Estado |
|---|---|
| **`merge` no está en el `deny`** | Técnicamente ejecutable. Recomendación: añadirlo. **Decisión del mantenedor** |
| El `deny` es global de usuario, no por repositorio | Es más restrictivo, no menos. No es un hueco |
| No hay registro de aprobaciones | Se resuelve con el `DECISION` del contrato |
| Un `rm -rf` no está bloqueado | Fuera del alcance de este documento, pero merece mirarse |

---

## 8. La prueba

El 09/09 la política se probó sola: hubo aprobación humana explícita de commits y push, la
barrera los bloqueó, y el trabajo se detuvo con los comandos entregados en lugar de buscar
una vía alternativa.

**Ese es el comportamiento correcto**, y conviene dejarlo escrito para que no se confunda
con un fallo la próxima vez: cuando una barrera y una instrucción se contradicen, gana la
barrera, y quien resuelve la contradicción es la persona.
