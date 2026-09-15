#!/usr/bin/env bash
# Business Crew - comprobacion de frontera
#
# Este repositorio es PUBLICO y MIT. La frontera que vigila este script esta
# definida en docs/v0.2/project-boundaries.md: aqui entra COMO trabajamos, no
# CON QUIEN ni POR CUANTO.
#
# Detecta regresiones obvias y no pretende mas: un DLP no cabe en un
# repositorio de 40 archivos, y el que lo intenta acaba desactivado a la
# primera falsa alarma.
#
# --- La decision de diseno que importa -------------------------------------
# Una lista de nombres de clientes dentro de un script publico PUBLICA los
# nombres de los clientes. Es exactamente el error que este repositorio ya
# cometio una vez (project-boundaries.md seccion 7).
#
# Por eso aqui solo viven patrones ESTRUCTURALES, seguros de publicar porque
# no nombran a nadie. Los nombres concretos, si hacen falta, viven en un
# archivo fuera de git que este script lee si existe.
#
# Uso:  bash scripts/check-boundary.sh
#
# --- Contrato de salida ------------------------------------------------------
# El check tiene DOS capas y el veredicto dice cual se ha evaluado:
#
#   exit 1  FRONTERA: hay hallazgos, o una comprobacion fallo al ejecutarse
#   exit 0  ESTRUCTURAL OK - NOMINAL NOT_EVALUATED
#           La capa estructural paso. La nominal NO se ha evaluado porque no
#           hay denylist. Es el resultado normal en un clon publico, y es un
#           aprobado PARCIAL: no afirma que la frontera este limpia.
#   exit 0  FRONTERA OK
#           Las dos capas evaluadas y las dos limpias. Requiere denylist.
#
# exit 0 sin denylist es deliberado -para que el check sirva en CI publico-,
# pero el texto nunca dice "FRONTERA OK" si la capa nominal no se ha mirado.

set -u

DENYLIST_PRIVADA=".crew/frontera-denylist.txt"
HALLAZGOS=0
NOMINAL_EVALUADA=0   # solo pasa a 1 si la denylist existe y tiene patrones
TMP="${TMPDIR:-/tmp}/bc-frontera.$$"
trap 'rm -f "$TMP" "$TMP.err"' EXIT

rojo()  { printf '\033[31m%s\033[0m\n' "$1"; }
verde() { printf '\033[32m%s\033[0m\n' "$1"; }
amar()  { printf '\033[33m%s\033[0m\n' "$1"; }

# Que se mira: prosa (.md) y fixtures (.json). Lo que NO se mira, y por que:
#   .git/                 no es contenido
#   .crew/                estado local fuera de git; ahi vive la denylist, que
#                         si se mirase se denunciaria a si misma
#   evals/results-*.json  volcados numericos derivados. Sus decimales
#                         contienen secuencias de 9 digitos que parecen
#                         telefonos y no lo son; ademas se regeneran
#   los .sh, .png, etc.   quedan fuera solos, por los --include
contar_archivos() {
  find . -type f \( -name '*.md' -o -name '*.json' \) \
    -not -path './.git/*' -not -path './.crew/*' -not -name 'results-*.json' 2>/dev/null | wc -l | tr -d ' '
}

# grep devuelve 0 si encuentra, 1 si no encuentra y >=2 si algo fue mal.
# Ese >=2 es el caso peligroso: un grep que revienta y cuyo error se tira a
# /dev/null deja un check que SIEMPRE pasa, que es peor que no tener check.
# Paso por aqui de verdad: en GNU grep 3.0 sobre Git Bash, -i junto a -f
# ABORTA con SIGABRT, y la regla 4 pasaba en silencio.
#
# buscar() corre dentro de $(...), o sea en una subshell: no puede tocar el
# contador. Solo marca la salida, y reportar() -que si corre en el shell
# principal- es quien cuenta.
MARCA_ERROR="__COMPROBACION_FALLIDA__"
buscar() {
  salida=$("$@" 2>"$TMP.err"); rc=$?
  [ "$rc" -ge 2 ] && { printf '%s\n%s' "$MARCA_ERROR" "$(cat "$TMP.err")"; return 0; }
  printf '%s' "$salida"
}

# Un hallazgo = un patron que no deberia aparecer nunca en un repo publico.
reportar() {
  titulo="$1"; salida="$2"
  [ -z "$salida" ] && return 0
  case "$salida" in
    "$MARCA_ERROR"*)
      rojo "! $titulo - LA COMPROBACION FALLO. Esto NO es un aprobado"
      printf '%s\n' "${salida#"$MARCA_ERROR"}" | sed 's/^/    /' ;;
    *)
      rojo "x $titulo"
      printf '%s\n' "$salida" | sed 's/^/    /' ;;
  esac
  HALLAZGOS=$((HALLAZGOS + 1))
}

# OJO con --exclude: en GNU grep 3.0, en cuanto aparece UN --exclude, el
# --include deja de restringir y grep se pone a leer .sh y .png. Comprobado.
# Por eso aqui solo hay --include y --exclude-dir, que si se comportan; lo
# que sobra se quita despues, con sin_derivados().
ALCANCE="-r --exclude-dir=.git --exclude-dir=.crew
         --include=*.md --include=*.json"

# Los volcados results-*.json son artefactos numericos derivados: se regeneran
# desde el codigo y sus decimales contienen cualquier secuencia de digitos.
sin_derivados() { grep -v '/results-[^/]*\.json:'; }

# --- 1 - Importes -----------------------------------------------------------
# Un precio es estrategia comercial. La excepcion son los fixtures de
# evaluacion, donde project-boundaries.md seccion 5 permite cifras inventadas
# y redondas: un caso de prueba sobre precios necesita un numero para existir.
#
# Solo se busca moneda con simbolo o codigo. Un "$" suelto se descarta a
# proposito: en markdown es el prompt de un bloque de codigo, no un precio.
IMPORTES=$(buscar grep $ALCANCE --exclude-dir=evals \
  -noE '[0-9][0-9.,]*[ ]?(€|EUR\b|USD\b)|€[ ]?[0-9]' . | sin_derivados)
reportar "Importe fuera de evals/ - un precio es estrategia comercial" "$IMPORTES"

# --- 2 - Telefonos ----------------------------------------------------------
# Formato espanol, con o sin prefijo. Nunca es legitimo: ningun ejemplo
# didactico necesita un telefono que marque de verdad.
# Se exige separador o prefijo: nueve digitos seguidos y sueltos aparecen
# dentro de los decimales de cualquier volcado numerico.
TELEFONOS=$(buscar grep $ALCANCE \
  -noE '(\+34[ -]?)?[6789][0-9]{2}[ -][0-9]{3}[ -][0-9]{3}\b|\+34[ -]?[6789][0-9]{8}\b' . | sin_derivados)
reportar "Posible telefono - dato personal de un tercero" "$TELEFONOS"

# --- 3 - Correos ------------------------------------------------------------
# Se permiten los noreply de plataforma y los dominios reservados por la
# RFC 2606, que existen precisamente para poner ejemplos.
CORREOS=$(buscar grep $ALCANCE \
  -noiE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' . | sin_derivados \
  | grep -viE '@(users\.)?noreply\.|@(example|ejemplo|invalid|test)\.')
reportar "Correo electronico - dato personal" "$CORREOS"

# --- 4 - Denylist privada (opcional, fuera de git) --------------------------
# Un patron por linea, texto literal. Se ignoran lineas vacias y las que
# empiezan por #. Aqui es donde van los nombres reales: nombres comerciales,
# apellidos, localidades, competidores, rutas a la inteligencia privada.
#
# Los patrones se pasan en la linea de comandos y no con -f, porque -i junto
# a -f aborta en GNU grep 3.0 (ver buscar()). Quedan visibles en `ps` durante
# el instante que dura el grep: es un check local, y el intercambio a favor de
# una comprobacion que de verdad funciona vale la pena. No lo ejecutes en un
# runner compartido con la denylist presente.
if [ -f "$DENYLIST_PRIVADA" ]; then
  # Se escapan los metacaracteres: sin -F, un punto de una ruta valdria por
  # cualquier caracter.
  PATRONES=$(grep -vE '^[[:space:]]*(#|$)' "$DENYLIST_PRIVADA" \
    | sed 's/[][\.^$*+?(){}|\\]/\\&/g' | paste -sd '|' -)
  if [ -n "$PATRONES" ]; then
    NOMINAL_EVALUADA=1
    PRIVADOS=$(buscar grep $ALCANCE -noiE "$PATRONES" . | sin_derivados)
    reportar "Coincide con la denylist privada" "$PRIVADOS"
  fi
else
  printf '  (sin denylist en %s: la capa nominal NO se evalua)\n' "$DENYLIST_PRIVADA"
fi

# --- Veredicto --------------------------------------------------------------
echo
N=$(contar_archivos)
if [ "$HALLAZGOS" -eq 0 ] && [ "$NOMINAL_EVALUADA" -eq 1 ]; then
  verde "FRONTERA OK - estructural + nominal, 0 hallazgos en $N archivos"
  exit 0
fi

if [ "$HALLAZGOS" -eq 0 ]; then
  # Aprobado PARCIAL. Decir "FRONTERA OK" aqui seria confundir "la mitad que
  # se midio esta limpia" con "la frontera esta limpia", que es justo el error
  # que este script existe para no cometer.
  amar "ESTRUCTURAL OK - NOMINAL NOT_EVALUATED  ($N archivos)"
  echo "  Importes, telefonos y correos: limpios."
  echo "  Nombres, lugares, competidores y rutas privadas: SIN COMPROBAR."
  echo "  Para evaluar la capa nominal, crea $DENYLIST_PRIVADA (un patron por linea)."
  exit 0
fi

rojo "FRONTERA: $HALLAZGOS tipo(s) de hallazgo"
echo
echo "Que hacer, en este orden (project-boundaries.md seccion 7):"
echo "  1. Clasificar: ejemplo generico / especifico del producto / comercial / operativo"
echo "  2. SUSTITUIR, no borrar. La ensenanza se queda, el dato se va"
echo "  3. Si es un falso positivo legitimo, NO se debilita el patron:"
echo "     se reescribe el ejemplo, o se justifica por escrito en este archivo"
exit 1
