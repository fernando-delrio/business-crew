#!/usr/bin/env bash
# Business Crew - SessionStart
# Al abrir el proyecto, recuerda el ciclo activo y avisa si el punto de la
# colina lleva dias sin moverse. Silencioso si el proyecto no usa ciclos:
# un hook que habla en proyectos que no le corresponden es ruido.

set -u

ESTADO=".crew/estado.md"
[ -f "$ESTADO" ] || exit 0

# --- utilidades de fecha portables (GNU date y BSD/macOS date) -------------
a_epoch() {
  # $1 = fecha YYYY-MM-DD -> segundos epoch, o vacio si no se puede parsear
  date -d "$1" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$1" +%s 2>/dev/null || echo ""
}

dias_desde() {
  # $1 = fecha YYYY-MM-DD -> dias transcurridos hasta hoy
  local ini fin
  ini=$(a_epoch "$1"); [ -n "$ini" ] || { echo ""; return; }
  fin=$(date +%s)
  echo $(( (fin - ini) / 86400 ))
}

campo() {
  # $1 = etiqueta -> valor en negrita markdown: **Etiqueta:** valor
  grep -m1 -i "^\*\*$1:\*\*" "$ESTADO" 2>/dev/null \
    | sed "s/^\*\*[^:]*:\*\* *//" \
    | sed "s/[[:space:]]*$//"
}

# --- cool-down -------------------------------------------------------------
if grep -qi "^# Cool-down" "$ESTADO" 2>/dev/null; then
  # En cool-down, Desde y Hasta suelen ir en la misma linea
  HASTA=$(grep -m1 -oE '\*\*Hasta:\*\* *[0-9]{4}-[0-9]{2}-[0-9]{2}' "$ESTADO" 2>/dev/null \
    | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  echo "[Business Crew] Cool-down${HASTA:+ hasta el $HASTA}. Sin apuesta activa."
  echo "Bugs sueltos y mantenimiento. Cuando toque decidir la siguiente: /bet"
  exit 0
fi

# --- ciclo activo ----------------------------------------------------------
APUESTA=$(campo "Apuesta")
[ -n "$APUESTA" ] || exit 0

APPETITE=$(campo "Appetite")
EMPEZO=$(campo "Empezó")
[ -n "$EMPEZO" ] || EMPEZO=$(campo "Empezo")
TERMINA=$(campo "Termina")
COLINA=$(campo "Colina")
MOVIMIENTO=$(campo "Último movimiento")
[ -n "$MOVIMIENTO" ] || MOVIMIENTO=$(campo "Ultimo movimiento")

echo "[Business Crew] Ciclo activo: $APUESTA"
[ -n "$APPETITE" ] && echo "Appetite: $APPETITE${TERMINA:+ · termina el $TERMINA}"
[ -n "$COLINA" ] && echo "Colina: $COLINA"

# Dias consumidos frente al total previsto
if [ -n "$EMPEZO" ] && [ -n "$TERMINA" ]; then
  INI=$(a_epoch "$EMPEZO"); FIN=$(a_epoch "$TERMINA")
  if [ -n "$INI" ] && [ -n "$FIN" ] && [ "$FIN" -gt "$INI" ]; then
    TOTAL=$(( (FIN - INI) / 86400 ))
    HECHOS=$(dias_desde "$EMPEZO")
    if [ -n "$HECHOS" ] && [ "$TOTAL" -gt 0 ]; then
      echo "Dia $HECHOS de $TOTAL."
      if [ "$HECHOS" -gt "$TOTAL" ]; then
        echo "AVISO: el appetite esta agotado. Circuit breaker: recortar y enviar, cancelar,"
        echo "o volver a apostar a conciencia. Seguir sin decidir no es una opcion. Usa /ship."
      elif [ $(( HECHOS * 2 )) -ge "$TOTAL" ] && printf '%s' "$COLINA" | grep -qi "arriba"; then
        echo "AVISO: mas de medio appetite consumido y sigues cuesta arriba."
        echo "Es el momento de recortar alcance, mientras todavia da tiempo. Usa /hill."
      fi
    fi
  fi
fi

# El punto que no se mueve es una mano levantada (Shape Up, cap. 13)
if [ -n "$MOVIMIENTO" ]; then
  FECHA_MOV=$(printf '%s' "$MOVIMIENTO" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
  if [ -n "$FECHA_MOV" ]; then
    QUIETO=$(dias_desde "$FECHA_MOV")
    if [ -n "$QUIETO" ] && [ "$QUIETO" -ge 2 ]; then
      echo "AVISO: llevas $QUIETO dias sin mover el punto de la colina."
      echo "Un punto que no se mueve es una mano levantada. Revisalo con /hill."
    fi
  fi
fi

exit 0
