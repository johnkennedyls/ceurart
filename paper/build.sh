#!/usr/bin/env bash
# Compilar el manuscrito dentro del fork de CEURART.
#
#   bash build.sh                 -> compila paper.tex   (version de envio)
#   bash build.sh paper-largo     -> compila paper-largo.tex
#
# Usa LuaLaTeX si esta instalado (receta oficial de la clase); si no, usa el
# Tectonic portable que esta en ../../tools/tectonic-msvc/.
set -euo pipefail
cd "$(dirname "$0")"

doc="${1:-paper}"
cls=../tex/latex/ceurart/ceurart.cls

# TeX busca la clase en el directorio actual: se copia la generada en el repo.
cp -f "$cls" ceurart.cls

if command -v lualatex >/dev/null 2>&1; then
  echo ">> LuaLaTeX + BibTeX"
  lualatex -interaction=nonstopmode "$doc"
  lualatex -interaction=nonstopmode "$doc"
  bibtex "$doc" || true
  for _ in 1 2 3; do lualatex -interaction=nonstopmode "$doc"; done
else
  tex="${TECTONIC:-../../tools/tectonic-msvc/tectonic.exe}"
  if [ ! -x "$tex" ]; then
    echo "No hay LuaLaTeX ni Tectonic en $tex." >&2
    echo "Descarga tectonic-*-x86_64-pc-windows-msvc.zip, descomprimalo ahi y vuelve." >&2
    exit 1
  fi
  echo ">> Tectonic ($tex)"
  # Dos pasadas: la primera genera el .bbl y la segunda lo tipografia completo.
  "$tex" "$doc.tex" -Z continue-on-errors --keep-logs
  "$tex" "$doc.tex" -Z continue-on-errors --keep-logs
fi

if command -v python >/dev/null 2>&1; then
  python - "$doc.pdf" <<'PY'
import sys
from pypdf import PdfReader
pages = len(PdfReader(sys.argv[1]).pages)
print(f"Paginas: {pages}  (limite NALEF 2026: 5-8)")
PY
fi
