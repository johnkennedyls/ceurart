# EchoPulse AI — envío a NALEF 2026 (CEUR-WS.org)

Manuscrito en formato **CEURART** para el encuentro **NALEF 2026** (Cartagena,
Colombia), volumen de **CEUR Workshop Proceedings**. Es un *system description
paper* de **8 páginas A4**, íntegramente en inglés.

Este directorio (`paper/`) vive **dentro de un fork del repositorio oficial de la
clase**: <https://github.com/johnkennedyls/ceurart> (fork de
`yamadharma/ceurart`, rama `master`). La razón del fork es práctica: Overleaf no
compilaba el proyecto, así que se clonó la plantilla para tener la clase y el
motor de compilación en local. El manuscrito y la plantilla conviven en el mismo
repo; todo lo nuestro está en `paper/`.

---

## 1. Dónde está cada cosa

```
ceurart/                     <- raíz del fork (repo upstream + carpeta paper/)
├── tex/latex/ceurart/
│   └── ceurart.cls          clase oficial generada: v0.6.2, fecha 2025-10-06
├── src/                     fuentes docstrip (.dtx) de la clase y de la muestra
├── doc/latex/ceurart/sample/ muestra oficial (sample__1col.tex, Makefile, .bib)
├── CHANGELOG.md             historial de la clase (0.6.3/0.6.4 solo tocaron la muestra)
├── LICENSE.LPPL             licencia de la clase
├── LICENSE.CC-BY-SA         licencia de la documentación/muestra
└── paper/                   <- TODO LO DEL ENVÍO ESTÁ AQUÍ
    ├── paper.tex            MANUSCRITO DE ENVÍO (538 líneas con notas internas)
    ├── paper-largo.tex      versión larga / archivo maestro (17 pp, no se envía)
    ├── sample-ceur.bib      bibliografía: 44 entradas, 30 citadas
    ├── figures/             7 figuras (1 PNG de arquitectura + 6 PDF de resultados)
    ├── build.sh             compilador local
    ├── make_submission.py   empaquetador del entregable (zip + PDF)
    ├── .gitignore           excluye la clase copiada, PDFs y logs
    ├── ceurart.cls          copia de trabajo que build.sh crea (ignorada por git)
    ├── paper.pdf            último PDF compilado (ignorado por git)
    └── dist/                ENTREGABLES generados (ignorados por git)
```

Archivos versionados en `paper/`: `paper.tex`, `paper-largo.tex`,
`sample-ceur.bib`, `figures/` (7), `build.sh`, `make_submission.py`,
`.gitignore` y este README. `ceurart.cls`, los `.pdf`, `.log`, `.blg` y `dist/`
están ignorados porque se regeneran.

Figuras (`paper/figures/`):

| Archivo | Uso |
|---|---|
| `archEchoPulse.png` (1664×928) | arquitectura del sistema; va en el manuscrito |
| `fig1_performance_comparison.pdf` | comparación de desempeño; va en el manuscrito |
| `fig2_latency_breakdown.pdf` … `fig5_generative_metrics.pdf` | solo en `paper-largo.tex`; se incluyen igual en el zip |
| `fig6_data_flow_architecture.pdf` | no la usa ninguno de los dos `.tex`; va en el zip por si se necesita |

---

## 2. Requisitos de la convocatoria y cómo se cumplen

| Requisito | Estado | Dónde |
|---|---|---|
| Plantilla oficial CEURART | `ceurart.cls` v0.6.2 sin modificar, la misma que distribuye el template de Overleaf. Prueba mecánica: `/Subject` del PDF dice "Layout by CEURART v0.6.2" | `tex/latex/ceurart/ceurart.cls` |
| Una columna, sin `twocolumn` ni `hf` | `\documentclass[]{ceurart}`; sin números de página ni encabezados en las 8 páginas | `paper.tex:20` |
| System description paper, 5–8 páginas, solo inglés | 8 páginas A4 | `paper.tex` |
| Nota de copyright en el pie de la pág. 1 | `\copyrightyear{2026}` + `\copyrightclause{...}` → "© 2026 Copyright for this paper by its authors. Use permitted under Creative Commons License Attribution 4.0 International (CC BY 4.0). NALEF 2026, Cartagena, Colombia." | `paper.tex:46-49` |
| Nombres completos + afiliación de los autores | 4 autores, con ORCID y correo institucional | `paper.tex:62-87` |
| Autores de correspondencia marcados | `\cormark[1]` y `\cormark[2]` con su `\cortext` | `paper.tex:66`, `paper.tex:72`, `paper.tex:89-90` |
| Sección "Declaration on Generative AI" | obligatoria por política CEUR-WS (enero 2025) | `paper.tex` (antes de `\bibliography`) |
| PDF corregido + zip con fuentes LaTeX | ver §4 | `paper/dist/` |

---

## 3. Compilar

### Opción A — local, en esta máquina (verificada)

No hay TeX Live instalado. Se usa **Tectonic portable**, que en esta máquina
está en:

```
D:\FUP\2026-2\doc for sco2\tools\tectonic-msvc\tectonic.exe        # Tectonic 0.17.0
```

Debe ser el build **MSVC** (`…-x86_64-pc-windows-msvc.zip`); el build GNU no
arranca en este Windows (falta `api-ms-win-core-winrt-error-l1-1-0.dll`).

```bash
cd paper
bash build.sh                 # compila paper.tex
bash build.sh paper-largo     # compila la versión larga
python make_submission.py     # genera el paquete de envío (usa pypdf)
```

`build.sh` hace dos cosas además de compilar: copia `ceurart.cls` desde
`../tex/latex/ceurart/` al directorio del paper (TeX solo busca la clase en el
directorio actual) y lanza el motor **dos veces**, porque en la primera pasada se
genera el `.bbl` y en la segunda se tipografían las referencias. Si existe
`lualatex` en el `PATH`, usa la receta oficial de la clase
(`lualatex → lualatex → bibtex → lualatex ×3`) en lugar de Tectonic.

Dependencias Python: `pypdf` (contador de páginas y normalización de metadatos).

Avisos que se pueden ignorar. Los tres primeros aparecen **idénticos** al
compilar la muestra oficial `doc/latex/ceurart/sample/sample__1col.tex`, o sea
que son de la clase o del motor, no del manuscrito:

- `! Package pdfx Error: CreationDate is not properly supported` — bajo Tectonic
  `pdfx` no genera `creationdate.lua` y el PDF hereda la fecha fija 2018-10-28
  que trae el bundle. `make_submission.py` la corrige en el PDF entregado.
- `Overfull \hbox (407.66833pt too wide) detected at \maketitle` — son las
  keywords dentro de un `\hbox_to_wd:nn{\z@}` de la propia clase.
- Avisos `ToUnicode` de FontAwesome5.
- `Warning--empty pages in loshchilov2019decoupled` (BibTeX) — este sí es
  nuestro: la entrada citada de AdamW no trae páginas. Inofensivo.

### Opción B — Overleaf

El `paper.tex` del zip **no lleva comentario mágico de motor** (`% !TeX program`),
porque las fuentes entregadas van limpias de comentarios. No hace falta: tampoco
depende de XeLaTeX/LuaLaTeX. Todo el texto no-ASCII son acentos Latin-1 de los
nombres propios (`Ordoñez`, `Méndez`), que LaTeX trata como UTF-8 por defecto
desde 2018 sin cargar `inputenc`, y la clase activa `\RequirePackage[T1]{fontenc}`
solo cuando compila con pdfLaTeX; Libertinus se carga únicamente si está
disponible. Por tanto:

1. Menú > **Upload project** > subir `dist/EchoPulseAI-NALEF2026-fuentes.zip`.
   Sus entradas están en la raíz del zip (igual que *Download > Source* de
   Overleaf), así que `paper.tex` aparece directamente.
2. Motor: **pdfLaTeX** (el que viene por defecto). `Main document`: `paper.tex`.
3. Rebuild. Con LuaLaTeX (receta oficial de la clase) también compila; puede que
   alguna línea se mueva, así que **revisar el conteo de páginas** tras cambiar
   de motor.

Nota: la verificación local se hizo con XeTeX (Tectonic). Con pdfLaTeX u otros
motores los saltos de línea pueden moverse alguna línea; **la página 8 va casi
llena**, así que cualquier añadido empuja el paper a 9 páginas y rompe el límite.

### Opción C — TeX Live normal

```bash
kpsewhich ceurart.cls || cp tex/latex/ceurart/ceurart.cls paper/
cd paper
lualatex paper.tex && bibtex paper && lualatex paper.tex && lualatex paper.tex
```

---

## 4. Los dos entregables

`python make_submission.py` genera en `paper/dist/`:

- **`EchoPulseAI-NALEF2026-paper.pdf`** — el artículo corregido, con metadatos
  normalizados (título, autores, asunto, keywords, fechas reales).
- **`EchoPulseAI-NALEF2026-fuentes.zip`** (≈2,3 MB) — proyecto autocontenido:
  `paper.tex`, `references.bib`, `figures/` con las 7 figuras, `ceurart.cls` y
  `elsarticle-num-names.bst` (el estilo que la clase exige; se copia de la caché
  de Tectonic para que compile aunque el árbol local no lo tenga) y
  `LEEME-compilar.txt`.
- `dist/EchoPulseAI-NALEF2026/` es la carpeta que se comprime, para revisarla a
  mano antes de adjuntar.

Qué hace exactamente el script, y por qué:

- **Copia `paper.tex` sin comentarios y le cambia la bibliografía** a
  `\bibliography{references}` (el `.bib` se renombra `references.bib` dentro del
  zip). Se eliminan únicamente las **líneas completas** de comentario; se
  conservan las líneas que *terminan* en `%` (ahí el `%` suprime el salto de
  línea y es código) y los `\%` del texto. Por eso el PDF del paquete sale con
  texto idéntico, verificado comparando el MD5 del texto extraído.
- Los marcadores internos `%% VERIFICAR (autores)` y `%% EDITOR` **solo**
  desaparecen de la copia entregada; siguen vivos en `paper.tex`, que es donde
  sirven. No borrarlos de ahí.
- `ceurart.cls` se copia **byte-idéntico** del upstream y no se le quitan sus
  comentarios: es la plantilla oficial y su integridad es parte de la prueba de
  cumplimiento.

El zip se puede validar compilando `dist/EchoPulseAI-NALEF2026/` desde un
directorio limpio con Tectonic:

```bash
cd dist/EchoPulseAI-NALEF2026
../../../../tools/tectonic-msvc/tectonic.exe paper.tex -Z continue-on-errors --keep-logs
# (repetir la línea una segunda vez para que entre el .bbl)
```

---

## 5. Autores

| # | Nombre | Afiliación |
|---|---|---|
| 1 | John Kennedy Landazuri Sandoval | [1] IMS Research Group, FUP — ORCID 0009-0004-7437-2779, `\cormark[1]` |
| 2 | Cristian Camilo Ordoñez Quintero | [1] FUP — ORCID 0000-0003-4157-1611, `\cormark[2]` |
| 3 | Hugo Armando Ordoñez Erazo | [2] GT, Universidad del Cauca — ORCID 0000-0002-3465-5617 |
| 4 | Cristian Méndez Rodríguez | [1] FUP — ORCID 0000-0002-4489-2712 |

`paper.tex:84-90` define las dos `\address` y los dos `\cortext`; hoy solo los
autores 1 y 2 son de correspondencia.

---

## 6. Pendientes antes de enviar

Están marcados en `paper.tex` y **no se resuelven inventando datos**; hay que
preguntarlos a los autores:

1. `%% VERIFICAR` — profundidades numéricas de los encoders de MST-MR.
2. `%% VERIFICAR` — protocolo de las pruebas de throughput y tasa de éxito
   (tamaño de lote, carga, duración) y qué máquina midió cada cifra. Dato
   descubierto al cruzar fuentes: los 185 vs 73 inferencias/s se midieron en un
   **i7-11800H**, mientras el entrenamiento fue en un **i5-7200U**; son máquinas
   distintas.
3. `%% VERIFICAR` — de qué campo de los datos salen los recuentos de oyentes
   mensuales que alimentan $\tau = 10{,}000$.
4. `%% VERIFICAR` — unidad de contraste y *n* de las t-tests (¿usuarios, queries
   o listas recomendadas?).
5. `%% VERIFICAR` — dónde se publicarán los scripts antes de afirmar que están
   disponibles.
6. `%% EDITOR` (`paper.tex:52`) — confirmar el nombre oficial del volumen
   CEUR-WS; hoy dice "NALEF 2026: 9th Encuentro de Semilleros de Investigación",
   pero el "9th" no se pudo verificar.
7. `%% EDITOR` — ajustar la lista de herramientas de IA generativa de la
   declaración a lo realmente usado.
8. Decisión de estilo: ¿el 4.º autor también lleva `\cormark`?

Bibliografía: auditada el 2026-10-21 contra Crossref, dblp, DataCite e ISMIR. Se
corrigieron 7 entradas y se **eliminó una referencia inexistente**
(`pimentel2021dataversioning`). Si se añade literatura nueva, verificar el DOI
antes de escribir la entrada.

---

## 7. Git

```bash
git status
git log --oneline -3
git push origin master          # requiere autorización explícita cada vez
```

- El fork está forkeado de un repositorio público, así que **casi con certeza es
  público**: el manuscrito queda visible en GitHub.
- `dist/`, `ceurart.cls`, los PDFs y los logs están ignorados; si alguien clona
  el repo, necesita ejecutar `bash build.sh` (que recrea `paper/ceurart.cls`) y
  luego `python make_submission.py` para volver a producir los entregables.
- Commits del manuscrito: `25d1ccc` (envío inicial), `68fd6b2` (pase de
  objetividad), `33da070` (auditoría bibliográfica), `a37ec56` (paquete limpio
  con todas las figuras).
