"""Empaqueta las fuentes LaTeX del paper para el envio a NALEF 2026.

Genera una copia limpia de paper.tex (sin las notas internas de trabajo),
los recursos necesarios para compilar de forma autonoma y un .zip.

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

HEADER = """%% EchoPulse AI -- envio a NALEF 2026 / CEUR-WS.org
%% Plantilla oficial: clase ceurart (https://github.com/yamadharma/ceurart)
%% Compilar con: lualatex x2 -> bibtex -> lualatex x3  (o pdflatex equivalente)
%% Sin numeros de pagina ni encabezados: no usar las opciones twocolumn ni hf.
"""


def clean_tex(src: Path, dst: Path) -> None:
    lines = src.read_text(encoding="utf-8").splitlines()
    kept = [ln for ln in lines if not ln.lstrip().startswith("%%")]

    body = "\n".join(kept)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = body.replace(
        r"\bibliography{" + BIB_SRC.replace(".bib", "") + "}",
        r"\bibliography{" + BIB_DST.replace(".bib", "") + "}",
    )
    dst.write_text(HEADER + body.rstrip() + "\n", encoding="utf-8")


def figure_names(tex: Path):
    text = tex.read_text(encoding="utf-8")
    return {m.group(1) for m in re.finditer(r"\\includegraphics\[[^\]]*\]\{([^}]+)\}", text)}


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
            "/CreationDate": now,
            "/ModDate": now,
            "/Title": "EchoPulse AI: A Hybrid Local Data Architecture for "
            "Multimodal Music Recommendation",
            "/Author": "John Kennedy Landazuri Sandoval; "
            "Cristian Camilo Ordonez Quintero; Hugo Armando Ordonez Erazo; "
            "Cristian Mendez Rodriguez",
            "/Subject": "NALEF 2026 system description paper (CEUR-WS.org)",
            "/Keywords": "Multimodal recommendation; Transformer architecture; "
            "Local data lakehouse; Music information retrieval; Cold-start "
            "problem; Popularity bias mitigation",
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
    (STAGE / "figures").mkdir()

    clean_tex(HERE / "paper.tex", STAGE / "paper.tex")
    shutil.copy2(HERE / BIB_SRC, STAGE / BIB_DST)

    cls = HERE / "ceurart.cls"
    if not cls.exists():
        raise SystemExit("Falta ceurart.cls en el directorio del paper (ejecuta build.sh primero).")
    shutil.copy2(cls, STAGE / "ceurart.cls")

    bst = find_bst()
    if bst:
        shutil.copy2(bst, STAGE / bst.name)
    else:
        print("AVISO: no se encontro elsarticle-num-names.bst; la clase lo exige.")

    used = figure_names(STAGE / "paper.tex")
    for name in sorted(used):
        frm = HERE / "figures" / name
        if not frm.exists():
            raise SystemExit(f"Falta la figura {name}")
        shutil.copy2(frm, STAGE / "figures" / Path(name).name)

    (STAGE / "LEEME-compilar.txt").write_text(
        "EchoPulse AI -- NALEF 2026 (CEUR-WS.org)\n\n"
        "Archivos:\n"
        "  paper.tex                       manuscrito principal\n"
        "  references.bib                  bibliografia\n"
        "  ceurart.cls                     clase oficial CEURART v0.6.2\n"
        "  elsarticle-num-names.bst        estilo bibliografico que exige la clase\n"
        "  figures/                        unicas figuras referenciadas\n\n"
        "Compilacion (receta de la propia clase):\n"
        "  lualatex paper.tex\n"
        "  bibtex   paper\n"
        "  lualatex paper.tex\n"
        "  lualatex paper.tex\n\n"
        "Equivalente con pdflatex o con Overleaf (plantilla oficial CEURART).\n"
        "Resultado esperado: 8 paginas A4, sin numeros de pagina ni encabezados.\n",
        encoding="utf-8",
    )

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STAGE.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(STAGE.parent))

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
