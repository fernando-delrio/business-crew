#!/usr/bin/env bash
# Business Crew - Stop
# El evento Stop se dispara cada vez que Claude termina de responder, asi que
# este script esta escrito para CALLARSE casi siempre. Solo habla cuando el
# appetite esta agotado, y como mucho una vez al dia.
#
# Un hook que avisa en cada respuesta deja de leerse a la semana.

set -u

ESTADO=".crew/estado.md"
[ -f "$ESTADO" ] || exit 0

# En cool-down no hay nada que recordar
grep -qi "^# Cool-down" "$ESTADO" 2>/dev/null && exit 0

TERMINA=$(grep -m1 -i "^\*\*Termina:\*\*" "$ESTADO" 2>/dev/null \
  | sed "s/^\*\*[^:]*:\*\* *//" \
  | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
[ -n "$TERMINA" ] || exit 0

a_epoch() {
  date -d "$1" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$1" +%s 2>/dev/null || echo ""
}

FIN=$(a_epoch "$TERMINA"); [ -n "$FIN" ] || exit 0
HOY_EPOCH=$(date +%s)
[ "$HOY_EPOCH" -gt "$FIN" ] || exit 0   # todavia dentro del appetite: silencio

# Throttle: como mucho un aviso al dia
HOY=$(date +%Y-%m-%d)
MARCA=".crew/.aviso-cierre"
[ -f "$MARCA" ] && [ "$(cat "$MARCA" 2>/dev/null)" = "$HOY" ] && exit 0
printf '%s' "$HOY" > "$MARCA" 2>/dev/null || true

VENCIDO=$(( (HOY_EPOCH - FIN) / 86400 ))
echo "[Business Crew] El appetite vencio hace $VENCIDO dia(s) (termino el $TERMINA)."
echo "Circuit breaker: recortar y enviar, cancelar, o volver a apostar a conciencia."
echo "Cierra el ciclo con /ship."

exit 0
