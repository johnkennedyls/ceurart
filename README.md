# [CEUR-WS.org](http://ceur-ws.org/) proceedings style

## Directories

### doc

Documentation.

### src

Sources for LaTeX class.

### template

User templates and guide.

### tex

LaTeX class.

## [Overleaf template](https://www.overleaf.com/latex/templates/template-for-submissions-to-ceur-workshop-proceedings-ceur-ws-dot-org/pkfscdkgkhcq)

- Authors: Dmitry S. Kulyabov, Ilaria Tiddi, Manfred Jeusfeld
- License: Creative Commons Attribution (CC BY 4.0)
- Abstract: CEUR-WS's article template provides a consistent LaTeX
  style for use across CEUR-WS publications, and incorporates
  accessibility and metadata-extraction functionality. This document
  will explain the major features of the document class.

---

## Note about this fork

Upstream content is unchanged: `tex/latex/ceurart/ceurart.cls` is still the
generated **v0.6.2 (2025-10-06)**, and tags `0.6.3` / `0.6.4` only touched the
sample, not the class. Nothing outside `paper/` has been modified.

This fork adds [`paper/`](paper), the manuscript submitted to **NALEF 2026**
(Cartagena, Colombia, CEUR-WS volume) — a 8-page CEURART system description
paper. Where every file lives, how to compile locally (Tectonic portable or
LuaLaTeX) and how to build the submission package is documented in
**[`paper/README.md`](paper/README.md)**.
