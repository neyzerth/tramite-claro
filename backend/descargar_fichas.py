#!/usr/bin/env python3
"""
Descarga el corpus del RETyS de Baja California para el proyecto MUAC Sin Barreras.

Fuentes oficiales:
  1. Catálogo completo (JSON):  https://retys.bajacalifornia.gob.mx/api/Tramites/get
  2. Ficha completa de cada trámite (HTML): https://retys.bajacalifornia.gob.mx/Portal/TyS/{Id}

Uso:
  python3 descargar_fichas.py            # baja la selección curada (recomendado para el hackathon)
  python3 descargar_fichas.py --todas    # baja las 730 fichas (~110 MB, tarda varios minutos)

Salida:
  fichas/<id>_<slug>.html   ficha original
  fichas/<id>_<slug>.txt    texto plano listo para el RAG
  fichas_index.json         índice con id, nombre, organismo, homoclave y archivos
"""
import json
import os
import re
import html as htmllib
import sys
import time
import unicodedata
import urllib.request

BASE = "https://retys.bajacalifornia.gob.mx"
CATALOGO = "retys_catalogo.json"
OUTDIR = "fichas"
UA = "Mozilla/5.0 (X11; Linux x86_64) corpus-hackathon"

# Selección curada: (campo, texto a buscar). El campo puede ser "nombre", "organismo" o "descripcion".
SELECCION = [
    ("nombre", "revalidación de licencia de conducir"),
    ("nombre", "expedición de licencia de conducir"),
    ("nombre", "antecedentes penales"),
    ("nombre", "tarjeta de circulación"),
    ("nombre", "placas"),
    ("nombre", "no inhabilitación"),
    ("nombre", "acta de matrimonio"),
    ("nombre", "acta de nacimiento"),
    ("organismo", "centro de justicia para las mujeres"),
    ("organismo", "secretaría de las mujeres"),
    ("organismo", "secretaría de inclusión social"),
    ("nombre", "constancia de residencia"),
    ("nombre", "beca"),
    ("nombre", "apoyo"),
    ("nombre", "credencial"),
    ("nombre", "permiso"),
]


def fetch(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def slug(texto: str, limite: int = 60) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:limite]


def html_a_texto(bruto: str) -> str:
    t = re.sub(r"<script.*?</script>", " ", bruto, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def campo_texto(t: dict, campo: str) -> str:
    """Devuelve el texto buscable de un registro para el campo pedido."""
    if campo == "nombre":
        return ((t.get("NombreCiudadano") or "") + " " + (t.get("NombreOficial") or "")).lower()
    if campo == "descripcion":
        return (t.get("Descripcion") or "").lower()
    return (t.get(campo) or "").lower()


def main() -> None:
    todas = "--todas" in sys.argv
    os.makedirs(OUTDIR, exist_ok=True)

    if not os.path.exists(CATALOGO):
        print(f"Descargando catálogo {CATALOGO} ...")
        with open(CATALOGO, "wb") as f:
            f.write(fetch(f"{BASE}/api/Tramites/get"))
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))["Datos"]
    print(f"Catálogo: {len(catalogo)} trámites")

    if todas:
        elegidos = catalogo
    else:
        elegidos, vistos = [], set()
        for campo, aguja in SELECCION:
            for t in catalogo:
                if aguja in campo_texto(t, campo) and t["Id"] not in vistos:
                    elegidos.append(t)
                    vistos.add(t["Id"])
                    break

    indice = []
    for i, t in enumerate(elegidos, 1):
        tid, nombre = t["Id"], (t.get("NombreCiudadano") or t.get("NombreOficial") or "tramite").strip()
        archivo = f"{tid}_{slug(nombre)}"
        ruta_html, ruta_txt = f"{OUTDIR}/{archivo}.html", f"{OUTDIR}/{archivo}.txt"
        try:
            if not os.path.exists(ruta_html):
                bruto = fetch(f"{BASE}/Portal/TyS/{tid}").decode("utf-8", "ignore")
                open(ruta_html, "w", encoding="utf-8").write(bruto)
                time.sleep(0.4)  # cortesía con el servidor
            texto = html_a_texto(open(ruta_html, encoding="utf-8").read())
            open(ruta_txt, "w", encoding="utf-8").write(texto)
            m = re.search(r"Homoclave:\s*([A-Z0-9\-]+)", texto)
            homoclave = m.group(1) if m else t.get("Homoclave")
            indice.append({
                "id": tid, "nombre": nombre, "organismo": t.get("Organismo"),
                "homoclave": homoclave, "html": ruta_html, "txt": ruta_txt,
            })
            print(f"[{i}/{len(elegidos)}] {tid} {homoclave or '—'} · {nombre[:70]}")
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(elegidos)}] ERROR {tid}: {e}")

    with open("fichas_index.json", "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=1)
    print(f"\nListo: {len(indice)} fichas en {OUTDIR}/ + fichas_index.json")


if __name__ == "__main__":
    main()
