"""Empaqueta las fuentes LaTeX del paper para el envio a NALEF 2026.

Genera una copia limpia de paper.tex y references.bib (sin las notas internas
de trabajo), copia todas las figuras y los recursos que hacen falta para
compilar de forma autonoma, y comprime todo con la misma estructura de
carpetas que produce Overleaf en Menu > Download > Source.

Uso:  python make_submission.py
"""

import glob
import re
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE / "dist" / "EchoPulseAI-NALEF2026"
ZIP = HERE / "dist" / "EchoPulseAI-NALEF2026-fuentes.zip"
BIB_SRC = "sample-ceur.bib"
BIB_DST = "references.bib"


def strip_comments(text: str) -> str:
    """Quita las lineas de comentario completo (la primera que no esta en blanco
    empieza por %).

    Las lineas que terminan en % se mantienen: ahi el % suprime el salto de
    linea y quitarlo cambiaria la composicion del documento. Los % escapados
    (\\%) tampoco se tocan, por eso el PDF sale igual con y sin esta pasada.
    """
    kept = [ln for ln in text.splitlines() if not ln.lstrip().startswith("%")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept))


def clean_tex(src: Path, dst: Path) -> None:
    body = strip_comments(src.read_text(encoding="utf-8"))
    body = body.replace(
        r"\bibliography{" + BIB_SRC.replace(".bib", "") + "}",
        r"\bibliography{" + BIB_DST.replace(".bib", "") + "}",
    )
    dst.write_text(body.rstrip() + "\n", encoding="utf-8")


def clean_bib(src: Path, dst: Path) -> None:
    body = strip_comments(src.read_text(encoding="utf-8"))
    dst.write_text(body.rstrip() + "\n", encoding="utf-8")


def find_bst() -> Path | None:
    pats = [
        str(Path.home() / "AppData/Local/TectonicProject/**/elsarticle-num-names.bst"),
        str(Path.home() / "AppData/**/elsarticle-num-names.bst"),
    ]
    for pat in pats:
        for hit in glob.glob(pat, recursive=True):
            return Path(hit)
    return None


def stamp_pdf(src: Path, dst: Path) -> None:
    """Normaliza los metadatos del PDF.

    Bajo Tectonic, pdfx no genera creationdate.lua y hereda la fecha fija
    2018-10-28 que trae el bundle; la muestra oficial de la clase la copia
    igual. Se corrige en el PDF entregado, no en las fuentes.
    """
    from datetime import datetime, timezone
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter(clone_from=str(src))
    now = datetime.now(timezone.utc).strftime(r"D:%Y%m%d%H%M%S+00'00'")
    writer.add_metadata(
        {
            "/Title": "EchoPulse AI: A Hybrid Local Data Architecture for "
            "Multimodal Music Recommendation",
            "/Author": "John Kennedy Landazuri Sandoval; "
            "Cristian Camilo Ordonez Quintero; Hugo Armando Ordonez Erazo; "
            "Cristian Mendez Rodriguez",
            "/Subject": "NALEF 2026 system description paper (CEUR-WS.org)",
            "/Keywords": "Multimodal recommendation; Transformer architecture; "
            "Local data lakehouse; Music information retrieval; Cold-start "
            "problem; Popularity bias mitigation",
            "/CreationDate": now,
            "/ModDate": now,
        }
    )
    dst.write_bytes(b"")
    with dst.open("wb") as fh:
        writer.write(fh)
    pages = len(PdfReader(str(dst)).pages)
    print(f"PDF entregado: {dst.name} ({pages} paginas)")


def main() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    clean_tex(HERE / "paper.tex", STAGE / "paper.tex")
    clean_bib(HERE / BIB_SRC, STAGE / BIB_DST)

    cls = HERE / "ceurart.cls"
    if not cls.exists():
        raise SystemExit("Falta ceurart.cls en el directorio del paper (ejecuta build.sh primero).")
    shutil.copy2(cls, STAGE / "ceurart.cls")

    bst = find_bst()
    if bst:
        shutil.copy2(bst, STAGE / bst.name)
    else:
        print("AVISO: no se encontro elsarticle-num-names.bst; la clase lo exige.")

    shutil.copytree(HERE / "figures", STAGE / "figures")

    (STAGE / "LEEME-compilar.txt").write_text(
        "EchoPulse AI - NALEF 2026 (CEUR-WS.org)\n"
        "Paper de descripcion de sistema, plantilla oficial CEURART.\n\n"
        "Contenido\n"
        "  paper.tex                    manuscrito principal\n"
        "  references.bib               bibliografia (30 referencias citadas)\n"
        "  ceurart.cls                  clase oficial CEURART v0.6.2, sin modificar\n"
        "  elsarticle-num-names.bst     estilo bibliografico que carga la clase\n"
        "  figures/                     todas las figuras del proyecto\n\n"
        "Compilacion\n"
        "En Overleaf: subir este .zip (Menu > Upload project > Overleaf project),\n"
        "dejar el motor en pdfLaTeX y pulsar Rebuild. No hace falta tocar nada mas:\n"
        "la entrada \\documentclass[]{ceurart} y la ruta figures/ ya estan resueltas\n"
        "por \\graphicspath.\n\n"
        "En local, con TeX Live:\n"
        "  lualatex paper.tex\n"
        "  bibtex   paper\n"
        "  lualatex paper.tex\n"
        "  lualatex paper.tex\n\n"
        "Equivalente con pdflatex (o con latexmk, que repite las pasadas solo).\n"
        "Resultado esperado: 8 paginas A4, sin numeros de pagina ni encabezados.\n"
        "No usar las opciones twocolumn ni hf de la clase.\n",
        encoding="utf-8",
    )

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STAGE.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(STAGE))

    pdf = HERE / "paper.pdf"
    if pdf.exists():
        stamp_pdf(pdf, HERE / "dist" / "EchoPulseAI-NALEF2026-paper.pdf")
    else:
        print("AVISO: no hay paper.pdf compilado; ejecuta build.sh antes de empacar.")

    print("Stage:", STAGE)
    for f in sorted(STAGE.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(STAGE)}  {f.stat().st_size:,} bytes")
    print("Zip:", ZIP, f"{ZIP.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
