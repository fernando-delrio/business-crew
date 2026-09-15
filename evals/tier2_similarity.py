#!/usr/bin/env python3
"""
Tier 2 — Evaluador de enrutado y colisión para Business Crew.

Qué responde
------------
1. ¿Dos capacidades tienen descripciones tan parecidas que el enrutado es una
   moneda al aire?
2. ¿Alguna descripción es tan genérica que competiría por casi cualquier consulta?
3. Ante una consulta realista, ¿gana la capacidad correcta?

Por qué así
-----------
Determinista, local, sin API, sin LLM, sin dependencias: solo la librería estándar.
Un evaluador que necesita red o tokens no se ejecuta, y uno que no se ejecuta no mide
nada. TF-IDF + coseno es una aproximación LÉXICA: no entiende significado. Eso es una
limitación real y está documentada en docs/v0.2/evals-baseline.md §Limitaciones.

Se acepta porque detecta los dos fallos que dominan los bugs de enrutado:
  - una descripción que no lleva las palabras que la gente usa  (falso negativo)
  - una descripción tan ancha que le gana el turno a la correcta (falso positivo)

Uso
---
    python evals/tier2_similarity.py                 # informe a stdout
    python evals/tier2_similarity.py --json out.json # + volcado reproducible
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# 1. EXTRACCIÓN — qué texto entra en la comparación, y por qué
# ─────────────────────────────────────────────────────────────────────────────
#
# Comparar archivos enteros mide el ESTILO de la plantilla, no la capacidad: los 18
# agentes comparten encabezados, tono y estructura, así que todos se parecerían a
# todos. Se extraen cuatro campos y se descartan el resto.
#
# ENTRAN                                      POR QUÉ
#   name          nombre del archivo/frontmatter   es parte del enrutado
#   description   frontmatter                      ES lo que el harness usa para enrutar
#   mission       primer párrafo tras el frontmatter  declara la responsabilidad
#   boundaries    "Cuándo NO aportas" / "Tus límites"  declara ownership por exclusión
#
# NO ENTRAN                                   POR QUÉ
#   "Contexto — siempre antes de responder"   boilerplate: en los 18. Ruido puro
#   "Ajuste por tipo de producto"             estructura repetida en 15 de 18
#   tablas, bloques de código, ejemplos       vocabulario del ejemplo, no de la capacidad
#   sintaxis markdown                         ruido
#
# Se calculan DOS espacios vectoriales distintos, y la diferencia entre ambos es el
# hallazgo más útil de todo el evaluador:
#
#   desc  = name + description
#           → lo que de verdad decide el enrutado hoy
#   full  = name + description + mission + boundaries
#           → la huella semántica real de la capacidad
#
#   desc ALTO + full BAJO  → capacidades distintas con descripciones que chocan
#                            = BUG DE DESCRIPCIÓN (barato de arreglar)
#   desc ALTO + full ALTO  → las capacidades se solapan de verdad
#                            = PROBLEMA DE DISEÑO (fusionar o redefinir)

SECCIONES_EXCLUIDAS = (
    "contexto — siempre antes de responder",
    "contexto - siempre antes de responder",
    "ajuste por tipo de producto",
    "tono",
)

# Encabezados cuyo contenido SÍ es declaración de fronteras.
SECCIONES_FRONTERA = (
    "cuándo no aportas",
    "cuando no aportas",
    "tus límites",
    "tus limites",
    "cuándo no se usa",
    "when not to use",
)


def leer_frontmatter(texto: str) -> tuple[dict, str]:
    """Devuelve (frontmatter, cuerpo). Frontmatter YAML plano: clave: valor."""
    if not texto.startswith("---"):
        return {}, texto
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return {}, texto
    meta: dict[str, str] = {}
    clave_actual = None
    for linea in partes[1].splitlines():
        if not linea.strip():
            continue
        m = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", linea)
        if m:
            clave_actual = m.group(1).strip()
            meta[clave_actual] = m.group(2).strip()
        elif clave_actual:  # continuación de una descripción multilínea
            meta[clave_actual] += " " + linea.strip()
    return meta, partes[2]


def limpiar_markdown(texto: str) -> str:
    texto = re.sub(r"```.*?```", " ", texto, flags=re.S)      # bloques de código
    texto = re.sub(r"`[^`]*`", " ", texto)                     # código en línea
    texto = re.sub(r"^\s*\|.*$", " ", texto, flags=re.M)       # filas de tabla
    texto = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texto)     # enlaces → su texto
    texto = re.sub(r"[*_>#]+", " ", texto)                     # énfasis y citas
    return texto


def partir_secciones(cuerpo: str) -> list[tuple[str, str]]:
    """[(titulo_normalizado, contenido)]. El preámbulo va con título ''."""
    trozos = re.split(r"^##\s+(.+)$", cuerpo, flags=re.M)
    salida = [("", trozos[0])]
    for i in range(1, len(trozos) - 1, 2):
        salida.append((trozos[i].strip().lower(), trozos[i + 1]))
    return salida


def extraer_unidad(ruta: Path, tipo: str) -> dict:
    texto = ruta.read_text(encoding="utf-8")
    meta, cuerpo = leer_frontmatter(texto)

    nombre = meta.get("name") or (
        ruta.parent.name if ruta.name == "SKILL.md" else ruta.stem
    )
    descripcion = meta.get("description", "")
    if tipo == "command" and meta.get("argument-hint"):
        # La pista de argumento es parte de lo que el usuario ve al elegir.
        descripcion += " " + meta["argument-hint"]

    # Se parte en secciones ANTES de limpiar el markdown: `limpiar_markdown` borra
    # los `#`, así que hacerlo al revés deja el documento sin encabezados y todas
    # las fronteras vacías. (Este era un bug real de la primera versión.)
    secciones = partir_secciones(cuerpo)
    mision, fronteras = "", []
    for titulo, contenido in secciones:
        contenido = limpiar_markdown(contenido)
        if titulo == "":
            # Primer párrafo real del preámbulo.
            parrafos = [p.strip() for p in contenido.split("\n\n") if p.strip()]
            mision = parrafos[0] if parrafos else ""
        elif any(titulo.startswith(f) for f in SECCIONES_FRONTERA):
            fronteras.append(contenido)
        elif any(titulo.startswith(x) for x in SECCIONES_EXCLUIDAS):
            continue

    return {
        "id": ("/" + nombre) if tipo == "command" else nombre,
        "tipo": tipo,
        "ruta": str(ruta.relative_to(RAIZ)).replace("\\", "/"),
        "name": nombre,
        "description": descripcion.strip(),
        "mission": mision.strip(),
        "boundaries": " ".join(fronteras).strip(),
        "tiene_fronteras": bool(fronteras),
        "lineas": len(texto.splitlines()),
    }


def cargar_unidades() -> list[dict]:
    unidades = []
    for ruta in sorted((RAIZ / "agents").glob("*.md")):
        unidades.append(extraer_unidad(ruta, "agent"))
    for ruta in sorted((RAIZ / "skills").glob("*/SKILL.md")):
        unidades.append(extraer_unidad(ruta, "skill"))
    for ruta in sorted((RAIZ / "commands").glob("*.md")):
        unidades.append(extraer_unidad(ruta, "command"))
    return unidades


# ─────────────────────────────────────────────────────────────────────────────
# 2. NORMALIZACIÓN — español, sin dependencias
# ─────────────────────────────────────────────────────────────────────────────

VACIAS = set("""
a al algo alguna algunas alguno algunos ante antes aquel aquella aquello aqui asi aun aunque
cada casi como con contra cual cuales cuando cuanto cuyo de del desde donde dos el ella ellas
ello ellos en entre era eran eres es esa esas ese eso esos esta estan estar estas este esto
estos ha habia han hace hacen hacer hacia hasta hay la las le les lo los mas me mi mientras
mucho muchos muy nada ni no nos nunca o otra otras otro otros para pero poco por porque que
quien se sea segun ser si sin sobre solo son su sus tan tanto te tiene tienen todo todos tu
tus un una uno unos usa usalo uso vez y ya sera seran debe deben puede pueden hay dice decir
tambien tras ademas mismo misma cuál qué cómo dónde
""".split())

# Se conservan a propósito: "no", "nunca", "sin" no se filtran porque en las secciones
# de frontera son portadoras de significado ("NO aportas", "sin datos").
VACIAS -= {"no", "nunca", "sin"}

SUFIJOS = (
    "aciones", "amiento", "imiento", "aciones", "adores", "adoras",
    "antes", "ancia", "encia", "ables", "ibles", "istas", "mente",
    "ción", "cion", "ador", "adora", "ante", "able", "ible", "ista",
    "ando", "endo", "ados", "adas", "idos", "idas", "ores", "oras",
    "ado", "ada", "ido", "ida", "oso", "osa", "ivo", "iva", "ión", "ion",
    "es", "os", "as", "or", "ar", "er", "ir", "an", "en",
    "a", "o", "e", "s",
)


def sin_tildes(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def raiz(palabra: str) -> str:
    """Stemmer español por sufijos. Deliberadamente conservador: nunca deja
    menos de 4 caracteres, para no fusionar palabras distintas."""
    for suf in SUFIJOS:
        if palabra.endswith(suf) and len(palabra) - len(suf) >= 4:
            return palabra[: -len(suf)]
    return palabra


def tokenizar(texto: str) -> list[str]:
    texto = sin_tildes(texto.lower())
    crudos = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", texto)
    return [raiz(p) for p in crudos if len(p) > 2 and p not in VACIAS]


# ─────────────────────────────────────────────────────────────────────────────
# 3. TF-IDF + COSENO
# ─────────────────────────────────────────────────────────────────────────────

def construir_espacio(documentos: dict[str, str]) -> tuple[dict, dict]:
    """Devuelve (vectores L2-normalizados, idf). tf sublineal, idf suavizado."""
    tokens = {k: tokenizar(v) for k, v in documentos.items()}
    n = len(tokens)
    df = Counter()
    for ts in tokens.values():
        df.update(set(ts))
    idf = {t: math.log((1 + n) / (1 + d)) + 1.0 for t, d in df.items()}

    vectores = {}
    for clave, ts in tokens.items():
        tf = Counter(ts)
        v = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items()}
        norma = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vectores[clave] = {t: x / norma for t, x in v.items()}
    return vectores, idf


def coseno(a: dict, b: dict) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(peso * b.get(t, 0.0) for t, peso in a.items())


def vectorizar_consulta(texto: str, idf: dict) -> dict:
    tf = Counter(tokenizar(texto))
    v = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items() if t in idf}
    norma = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {t: x / norma for t, x in v.items()}


# ─────────────────────────────────────────────────────────────────────────────
# 4. GENERICIDAD
# ─────────────────────────────────────────────────────────────────────────────
#
# Tres señales, porque ninguna sola basta:
#   G1  frases comodín declaradas ("cualquier tipo de producto")
#   G2  similitud media con TODAS las demás  → si se parece a todo, compite con todo
#   G3  IDF medio de sus términos            → bajo = usa el vocabulario común

FRASES_COMODIN = [
    "cualquier tipo de producto", "cualquier producto", "cualquier stack",
    "cualquier proyecto", "para todo", "sirve para cualquier",
    "en cualquier caso", "todo tipo de",
]


def analizar_genericidad(unidades, vec_desc, idf):
    filas = []
    ids = [u["id"] for u in unidades]
    for u in unidades:
        desc = u["description"].lower()
        comodines = [f for f in FRASES_COMODIN if f in sin_tildes(desc)
                     or f in desc]
        otros = [coseno(vec_desc[u["id"]], vec_desc[o]) for o in ids if o != u["id"]]
        sim_media = sum(otros) / len(otros) if otros else 0.0
        toks = tokenizar(u["description"])
        idf_medio = (sum(idf.get(t, 0.0) for t in toks) / len(toks)) if toks else 0.0
        filas.append({
            "id": u["id"], "tipo": u["tipo"],
            "comodines": comodines,
            "n_comodines": len(comodines),
            "sim_media": sim_media,
            "idf_medio": idf_medio,
            "palabras_desc": len(toks),
        })
    # Genericidad compuesta, 0-100. Documentada en evals-baseline.md.
    if filas:
        max_sim = max(f["sim_media"] for f in filas) or 1.0
        max_idf = max(f["idf_medio"] for f in filas) or 1.0
        for f in filas:
            norm_sim = f["sim_media"] / max_sim
            norm_idf_inv = 1 - (f["idf_medio"] / max_idf)
            f["genericidad"] = round(
                100 * (0.5 * norm_sim + 0.3 * norm_idf_inv
                       + 0.2 * min(f["n_comodines"], 2) / 2), 1)
    return sorted(filas, key=lambda f: -f["genericidad"])


# ─────────────────────────────────────────────────────────────────────────────
# 5. INFORME
# ─────────────────────────────────────────────────────────────────────────────

def evaluar_casos(casos, vec_desc, idf, unidades):
    """Enruta cada consulta contra el espacio `desc` y calcula las métricas.

    Extraída de main() en la Fase 2 para poder ejecutar varios fixtures sin
    duplicar la lógica: tres fixtures con tres copias del mismo bucle es la forma
    más rápida de que uno se quede viejo.
    """
    resultados = []
    top1 = top3 = malos = ambiguos = inalcanzables = sin_ruta = 0
    for c in casos:
        q = vectorizar_consulta(c["query"], idf)
        marcador = sorted(((coseno(q, vec_desc[u["id"]]), u["id"])
                           for u in unidades), reverse=True)
        # Una puntuación de 0 NO es un enrutado: es ausencia de coincidencia.
        positivos = [(s, n) for s, n in marcador if s > 0]
        ranking = [n for _, n in positivos[:3]]
        puntuaciones = [s for s, _ in positivos[:3]]
        esperado = c["expected_primary"]
        s_esp = next((s for s, n in marcador if n == esperado), 0.0)
        alcanzable = s_esp > 0
        inalcanzables += not alcanzable
        ok1 = bool(ranking) and ranking[0] == esperado
        ok3 = esperado in ranking
        top1 += ok1
        top3 += ok3
        prohibidos = [r for r in ranking if r in c.get("should_not_route_to", [])]
        malos += bool(prohibidos)
        # FORBIDDEN ABOVE PRIMARY: una prohibida por ENCIMA de la esperada.
        # Más útil que la mera presencia en top-3, que penaliza casos que mejoraron.
        pos_esp = ranking.index(esperado) if ok3 else 99
        por_encima = [r for r in prohibidos if ranking.index(r) < pos_esp]
        if not ranking:
            sin_ruta += 1
            amb, margen = True, 0.0
        else:
            margen = (puntuaciones[0] - puntuaciones[1]
                      if len(puntuaciones) > 1 else puntuaciones[0])
            amb = margen < 0.05 or puntuaciones[0] < 0.15
        ambiguos += amb
        resultados.append({
            "id": c["id"], "query": c["query"], "expected": esperado,
            "top3": ranking, "scores": [round(s, 3) for s in puntuaciones],
            "expected_score": round(s_esp, 4), "expected_reachable": alcanzable,
            "top1_ok": ok1, "top3_ok": ok3,
            "forbidden_in_top3": prohibidos,
            "forbidden_above_primary": por_encima,
            "ambiguous": amb, "margin": round(margen, 4),
        })
    n = len(casos) or 1
    metricas = {
        "TOP-1": 100 * top1 / n, "TOP-3": 100 * top3 / n,
        "UNNECESSARY": 100 * malos / n, "MISSING": 100 * (n - top3) / n,
        "AMBIGUOUS": 100 * ambiguos / n, "UNREACHABLE": 100 * inalcanzables / n,
        "FORBIDDEN-ABOVE-PRIMARY": 100 * sum(
            1 for r in resultados if r["forbidden_above_primary"]) / n,
        "NO-ROUTE": 100 * sin_ruta / n,
    }
    return {"casos": resultados, "metricas": metricas}


UMBRAL_ERROR = 0.75   # colisión: descripciones prácticamente intercambiables
UMBRAL_AVISO = 0.50   # vigilar: empiezan a competir


def tipo_par(a, b):
    return " ↔ ".join(sorted([a["tipo"], b["tipo"]]))


def interpretar(s_desc, s_full):
    if s_desc >= UMBRAL_ERROR:
        return ("BUG DE DESCRIPCIÓN — capacidades distintas, descripciones que chocan"
                if s_full < UMBRAL_AVISO else
                "SOLAPAMIENTO REAL — se pisan de verdad")
    if s_desc >= UMBRAL_AVISO:
        return "VIGILAR — compiten por consultas parecidas"
    if s_full >= UMBRAL_ERROR:
        return "CONTENIDO SOLAPADO, descripciones distintas"
    return "distintas"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="volcado reproducible")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--cases", default="routing-cases.json",
                    help="fixture alternativo dentro de evals/fixtures/")
    ap.add_argument("--all-fixtures", action="store_true",
                    help="ejecuta los tres fixtures y agrega en MACRO")
    ap.add_argument("--json-prefix",
                    help="con --all-fixtures: guarda un volcado por fixture")
    args = ap.parse_args()

    out = sys.stdout
    if hasattr(out, "reconfigure"):
        out.reconfigure(encoding="utf-8", errors="replace")

    unidades = cargar_unidades()
    idx = {u["id"]: u for u in unidades}

    docs_desc = {u["id"]: f"{u['name']} {u['description']}" for u in unidades}
    docs_full = {u["id"]: " ".join([u["name"], u["description"],
                                    u["mission"], u["boundaries"]])
                 for u in unidades}
    vec_desc, idf_desc = construir_espacio(docs_desc)
    vec_full, _ = construir_espacio(docs_full)

    print("=" * 78)
    print("TIER 2 — BASELINE DE ENRUTADO Y COLISIÓN · Business Crew")
    print("=" * 78)
    n = Counter(u["tipo"] for u in unidades)
    print(f"\nUnidades: {len(unidades)}  "
          f"(agents {n['agent']} · skills {n['skill']} · commands {n['command']})")
    sin_front = [u["id"] for u in unidades
                 if u["tipo"] == "agent" and not u["tiene_fronteras"]]
    if sin_front:
        print(f"Agentes SIN sección de fronteras: {', '.join(sin_front)}")

    # ── Pares ────────────────────────────────────────────────────────────────
    pares = []
    for i, a in enumerate(unidades):
        for b in unidades[i + 1:]:
            sd = coseno(vec_desc[a["id"]], vec_desc[b["id"]])
            sf = coseno(vec_full[a["id"]], vec_full[b["id"]])
            pares.append({
                "a": a["id"], "b": b["id"], "tipo": tipo_par(a, b),
                "s_desc": round(sd, 4), "s_full": round(sf, 4),
                "interpretacion": interpretar(sd, sf),
            })
    pares.sort(key=lambda p: -p["s_desc"])

    print(f"\n{'─' * 78}\nTOP {args.top} PARES POR SIMILITUD DE DESCRIPCIÓN\n{'─' * 78}")
    print(f"{'A':<22}{'B':<22}{'DESC':>7}{'FULL':>7}  {'TIPO':<20}")
    for p in pares[:args.top]:
        marca = "!!" if p["s_desc"] >= UMBRAL_ERROR else (
            " !" if p["s_desc"] >= UMBRAL_AVISO else "  ")
        print(f"{p['a']:<22}{p['b']:<22}{p['s_desc']:>7.3f}{p['s_full']:>7.3f}"
              f"  {p['tipo']:<20}{marca}")

    print(f"\nColisiones >= {UMBRAL_ERROR}: "
          f"{sum(1 for p in pares if p['s_desc'] >= UMBRAL_ERROR)}")
    print(f"Avisos     >= {UMBRAL_AVISO}: "
          f"{sum(1 for p in pares if UMBRAL_AVISO <= p['s_desc'] < UMBRAL_ERROR)}")

    # Media por tipo de par
    print(f"\n{'─' * 78}\nMEDIA DE SIMILITUD POR TIPO DE PAR\n{'─' * 78}")
    por_tipo = {}
    for p in pares:
        por_tipo.setdefault(p["tipo"], []).append(p["s_desc"])
    for t, vs in sorted(por_tipo.items()):
        print(f"  {t:<22} n={len(vs):>3}  media={sum(vs)/len(vs):.3f}  "
              f"max={max(vs):.3f}")

    # ── Hipótesis ────────────────────────────────────────────────────────────
    hipotesis = [
        ("H1", "director-arte", "design-direction", "alta"),
        ("H2", "scrum-master", "/crew", "alta"),
        ("H3a", "munger-critico", "qa-bach", "proxima-diferenciada"),
        ("H3b", "munger-critico", "seguridad", "proxima-diferenciada"),
        ("H3c", "qa-bach", "seguridad", "proxima-diferenciada"),
        ("H4", "dev-dhh", "devops-hightower", "baja"),
        ("H5", "ux-norman", "ui-duarte", "baja"),
    ]
    print(f"\n{'─' * 78}\nHIPÓTESIS\n{'─' * 78}")
    res_hip = []
    for etiqueta, x, y, esperado in hipotesis:
        p = next((q for q in pares
                  if {q["a"], q["b"]} == {x, y}), None)
        if not p:
            print(f"  {etiqueta}: par no encontrado ({x}, {y})")
            continue
        sd, sf = p["s_desc"], p["s_full"]
        if esperado == "alta":
            veredicto = "CONFIRMADA" if sd >= UMBRAL_AVISO else "RECHAZADA"
        elif esperado == "baja":
            veredicto = "CONFIRMADA" if sd < UMBRAL_ERROR else "RECHAZADA"
        else:
            veredicto = "CONFIRMADA" if sd < UMBRAL_ERROR else "RECHAZADA"
        res_hip.append({**p, "hipotesis": etiqueta, "esperado": esperado,
                        "veredicto": veredicto})
        print(f"  {etiqueta:<5}{x:<18}{y:<20}desc={sd:.3f} full={sf:.3f}"
              f"  esperado={esperado:<22}{veredicto}")

    # ── Genericidad ──────────────────────────────────────────────────────────
    gen = analizar_genericidad(unidades, vec_desc, idf_desc)
    print(f"\n{'─' * 78}\nGENERICIDAD (0 = específica · 100 = compite con todo)"
          f"\n{'─' * 78}")
    print(f"{'UNIDAD':<24}{'GEN':>6}{'SIM.MED':>9}{'IDF.MED':>9}{'PAL':>5}  COMODINES")
    for f in gen:
        com = ", ".join(f["comodines"])[:34] or "—"
        print(f"{f['id']:<24}{f['genericidad']:>6.1f}{f['sim_media']:>9.3f}"
              f"{f['idf_medio']:>9.2f}{f['palabras_desc']:>5}  {com}")

    # ── Casos de enrutado ────────────────────────────────────────────────────
    ruta_casos = RAIZ / "evals" / "fixtures" / args.cases
    resultados_casos = []
    if ruta_casos.exists():
        casos = json.loads(ruta_casos.read_text(encoding="utf-8"))["cases"]
        print(f"\n{'─' * 78}\nCASOS DE ENRUTADO  ({len(casos)})\n{'─' * 78}")
        top1 = top3 = 0
        malos = 0
        ambiguos = 0
        inalcanzables = 0
        sin_ruta = 0
        for c in casos:
            q = vectorizar_consulta(c["query"], idf_desc)
            marcador = sorted(((coseno(q, vec_desc[u["id"]]), u["id"])
                               for u in unidades), reverse=True)
            # Una puntuación de 0 NO es un enrutado: es ausencia de coincidencia.
            # Rellenar el top-3 con ceros inventaba candidatos y marcaba como
            # "prohibida" a una capacidad que en realidad no competía por nada.
            # (Este era un bug real de la primera versión.)
            positivos = [(s, nombre) for s, nombre in marcador if s > 0]
            ranking = [nombre for _, nombre in positivos[:3]]
            puntuaciones = [s for s, _ in positivos[:3]]
            esperado = c["expected_primary"]

            # Alcanzabilidad: ¿la capacidad esperada comparte ALGO de vocabulario?
            s_esperado = next((s for s, nombre in marcador if nombre == esperado), 0.0)
            alcanzable = s_esperado > 0
            inalcanzables += not alcanzable

            ok1 = bool(ranking) and ranking[0] == esperado
            ok3 = esperado in ranking
            top1 += ok1
            top3 += ok3
            prohibidos = [r for r in ranking if r in c.get("should_not_route_to", [])]
            malos += bool(prohibidos)

            if not ranking:
                sin_ruta += 1
                amb, margen = True, 0.0
            else:
                margen = (puntuaciones[0] - puntuaciones[1]
                          if len(puntuaciones) > 1 else puntuaciones[0])
                amb = margen < 0.05 or puntuaciones[0] < 0.15
            ambiguos += amb

            resultados_casos.append({
                "id": c["id"], "query": c["query"], "expected": esperado,
                "top3": ranking, "scores": [round(s, 3) for s in puntuaciones],
                "expected_score": round(s_esperado, 4),
                "expected_reachable": alcanzable,
                "top1_ok": ok1, "top3_ok": ok3,
                "forbidden_in_top3": prohibidos, "ambiguous": amb,
                "margin": round(margen, 4),
            })
            estado = "OK " if ok1 else ("~3 " if ok3 else "MAL")
            print(f"\n  [{c['id']}] {estado} esperado={esperado} "
                  f"(score {s_esperado:.3f}{'' if alcanzable else ' · INALCANZABLE'})")
            print(f"     \"{c['query'][:66]}\"")
            print("     top: " + (" · ".join(
                f"{r}({s:.3f})" for r, s in zip(ranking, puntuaciones))
                or "— ninguna capacidad comparte vocabulario con la consulta"))
            if prohibidos:
                print(f"     PROHIBIDA EN TOP: {', '.join(prohibidos)}")
            if amb:
                print(f"     AMBIGUO (margen {margen:.3f})")

        t = len(casos)
        print(f"\n{'─' * 78}\nMÉTRICAS BASELINE\n{'─' * 78}")
        print(f"  TOP-1 CORRECT           {top1}/{t} = {100*top1/t:.0f}%")
        print(f"  TOP-3 COVERAGE          {top3}/{t} = {100*top3/t:.0f}%")
        print(f"  UNNECESSARY CAPABILITY  {malos}/{t} = {100*malos/t:.0f}%"
              f"   (prohibida entre las candidatas reales)")
        print(f"  MISSING CAPABILITY      {t-top3}/{t} = {100*(t-top3)/t:.0f}%"
              f"   (esperada fuera del top-3)")
        print(f"  AMBIGUOUS ROUTE         {ambiguos}/{t} = {100*ambiguos/t:.0f}%")
        print(f"  UNREACHABLE CAPABILITY  {inalcanzables}/{t} = "
              f"{100*inalcanzables/t:.0f}%   (score 0: cero vocabulario en común)")
        print(f"  NO ROUTE AT ALL         {sin_ruta}/{t} = {100*sin_ruta/t:.0f}%"
              f"   (ninguna candidata)")

    if args.all_fixtures:
        # MACRO = promedio SIMPLE entre fixtures, no ponderado por nº de casos.
        # Un fixture de 8 casos pesa igual que uno de 12: cada uno mide una cosa
        # distinta y ninguno debe diluir al otro.
        nombres = ["routing-cases.json", "holdout-cases.json",
                   "external-style-cases.json"]
        etiquetas = ["ORIGINAL", "HOLDOUT", "EXTERNAL"]
        filas, todos = [], {}
        for fx, et in zip(nombres, etiquetas):
            ruta = RAIZ / "evals" / "fixtures" / fx
            if not ruta.exists():
                continue
            casos = json.loads(ruta.read_text(encoding="utf-8"))["cases"]
            r = evaluar_casos(casos, vec_desc, idf_desc, unidades)
            filas.append((et, r["metricas"], len(casos)))
            todos[et] = r
            if args.json_prefix:
                Path(f"{args.json_prefix}-{et.lower()}.json").write_text(
                    json.dumps({"fixture": fx, **r}, ensure_ascii=False, indent=2),
                    encoding="utf-8")
        claves = ["TOP-1", "TOP-3", "UNREACHABLE", "MISSING", "AMBIGUOUS",
                  "UNNECESSARY", "FORBIDDEN-ABOVE-PRIMARY"]
        barra = "=" * 78
        print("")
        print(barra)
        print("EVAL THREE-WAY")
        print(barra)
        print(f"{'MÉTRICA':<24}" + "".join(f"{e:>12}" for e, _, _ in filas) + f"{'MACRO':>12}")
        for k in claves:
            vals = [m[k] for _, m, _ in filas]
            macro = sum(vals) / len(vals)
            print(f"{k:<24}" + "".join(f"{v:>11.0f}%" for v in vals) + f"{macro:>11.1f}%")
        print("")
        print("MACRO = promedio simple entre fixtures, sin ponderar por numero "
              "de casos: cada fixture mide una cosa distinta y ninguno debe "
              "diluir al otro.")
        print("Los tres se reportan siempre por separado: el MACRO no los sustituye.")
        return

    if args.json:
        Path(args.json).write_text(json.dumps({
            "unidades": unidades, "pares": pares, "hipotesis": res_hip,
            "genericidad": gen, "casos": resultados_casos,
            "umbrales": {"error": UMBRAL_ERROR, "aviso": UMBRAL_AVISO},
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nVolcado: {args.json}")


if __name__ == "__main__":
    main()
