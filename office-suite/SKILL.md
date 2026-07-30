---
name: office-suite
description: "Use when creating, editing, inspecting, or converting everyday office documents in Word (.docx), Excel (.xlsx/.xls/.csv), PowerPoint (.pptx), or PDF, including reports, spreadsheets, financial models, slide decks, and formatted or fillable PDFs. Provides format-specific references, shared OOXML tooling, and helper scripts for reliable create/edit/convert workflows. Loading it activates the per-format guides under references/ and the scripts under scripts/."
---

# Office Suite

One skill for ordinary office-document work across four formats: Word, Excel, PowerPoint, and PDF. This file only routes you to the right per-format reference and states the shared setup. Load the reference for the format you are working on; do not load all of them.

## Route by Format

Identify the target file format, then read the matching reference before writing anything.

| Format | File types | Read |
|---|---|---|
| Word | `.docx`, `.doc` | [references/docx.md](references/docx.md) |
| Excel | `.xlsx`, `.xlsm`, `.xls`, `.csv`, `.tsv` | [references/xlsx.md](references/xlsx.md) |
| PowerPoint | `.pptx` | [references/pptx.md](references/pptx.md) |
| PDF | `.pdf` | [references/pdf.md](references/pdf.md) |

Each format reference points onward to its own deep-dive files (for example `references/pptx-editing.md`, `references/pdf-forms.md`) and names the scripts it needs. Load those only when the reference tells you to.

## Python Environment (shared)

All Python here runs through one local environment defined by `pyproject.toml` at the skill root. Set it up once, then run every script through it:

```bash
# From the office-suite/ skill directory
uv sync                       # creates/updates .venv from pyproject.toml
uv run python scripts/<area>/<script>.py ...
```

`uv run` keeps `.venv` in sync with `pyproject.toml`, so the format libraries (openpyxl, pandas, python-docx, pypdf, pdfplumber, reportlab, Pillow, matplotlib, and the OOXML validators' lxml/defusedxml) are always present. Do not fall back to the system `python3`.

Some capabilities need non-Python tools: LibreOffice (`soffice`, auto-configured via `scripts/office/soffice.py`) for format conversion and recalculation; Poppler (`pdftoppm`, `pdftotext`, `pdfimages`) and `qpdf` for PDF operations; `tesseract` for OCR; and Node packages (`docx`, `pptxgenjs`) installed with `npm install -g`. Install these with the OS package manager or npm as each reference directs.

## Layout

```
office-suite/
  SKILL.md                  # this router
  pyproject.toml            # shared Python deps (uv sync)
  references/               # per-format guides + deep dives
    docx.md  xlsx.md  pptx.md  pdf.md
    pptx-editing.md  pptx-design.md  pptx-pptxgenjs.md  pptx-traps.md
    pdf-forms.md  pdf-reference.md  pdf-layout-defaults.md
  scripts/
    office/                 # shared OOXML pack/unpack/validate/soffice (docx, xlsx, pptx)
    word/                   # accept_changes.py, comment.py, templates/
    xlsx/                   # recalc.py
    pptx/                   # add_slide.py, clean.py, thumbnail.py
    pdf/                    # form-filling, extraction, image-render helpers
  assets/                   # pdf_template.py + Excel demo (build_ai_pricing.py, ai_api_pricing.xlsx)
```

## Cross-Format Conversion

Conversions route through LibreOffice via `scripts/office/soffice.py`:

```bash
uv run python scripts/office/soffice.py --headless --convert-to pdf input.docx
uv run python scripts/office/soffice.py --headless --convert-to pdf input.pptx
uv run python scripts/office/soffice.py --headless --convert-to docx input.doc
```

For PDF-to-image (visual QA of any exported file), use Poppler `pdftoppm` or `scripts/pdf/convert_pdf_to_images.py`. The per-format references cover the details.

