# Política de seguridad

## Qué ejecuta este plugin en tu máquina

Conviene ser transparente, porque un plugin de Claude Code con hooks **sí ejecuta código
en tu equipo**. Business Crew ejecuta exactamente dos scripts de shell:

| Script | Cuándo | Qué hace |
|---|---|---|
| `scripts/cargar-ciclo.sh` | `SessionStart` | **Lee** `.crew/estado.md` del proyecto actual e imprime un recordatorio |
| `scripts/recordar-cierre.sh` | `Stop` | **Lee** la fecha de fin del ciclo. Escribe un único fichero: `.crew/.aviso-cierre`, con la fecha de hoy, para no repetir el aviso |

Lo que **no** hacen, y puedes verificarlo leyéndolos (menos de 100 líneas cada uno):

- No hacen peticiones de red
- No leen nada fuera de `.crew/` del directorio actual
- No envían telemetría
- No tocan tu configuración, tus credenciales ni tus variables de entorno
- Solo escriben ese fichero de marca

Los agentes y skills son ficheros Markdown: instrucciones para el modelo, no código.

## Si no quieres los hooks

Son opcionales. Borra `hooks/hooks.json` de tu copia y el resto del plugin funciona igual;
pierdes solo el recordatorio automático al abrir el proyecto.

## Versiones con soporte

| Versión | Soporte |
|---|---|
| 2.x | ✅ |
| 1.x | ❌ — actualiza a 2.x |

## Reportar una vulnerabilidad

**No abras un issue público** para una vulnerabilidad.

Usa [Security Advisories](https://github.com/fernando-delrio/business-crew/security/advisories/new)
de GitHub, que es privado.

Incluye: qué falla, cómo reproducirlo, qué impacto tiene y en qué sistema operativo y
versión de Claude Code lo has visto.

Respondo en un plazo razonable — esto lo mantiene una persona, no un equipo. Si es real,
lo arreglo y te acredito en el aviso salvo que prefieras lo contrario.

## Sobre el consejo de seguridad que da el plugin

El agente `seguridad` y el agente `legal-basico` dan **una primera lectura, no una
auditoría**. Ambos están escritos para decirte explícitamente cuándo el riesgo requiere
un profesional certificado: cumplimiento formal de protección de datos, auditoría de
intrusión, datos de salud o de menores, pagos.

**No sustituyen a un auditor de seguridad ni a un abogado.** Si un agente te da el visto
bueno, eso no es una certificación de nada.
