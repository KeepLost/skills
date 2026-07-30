# PDF Reference

Loaded from `office-suite`. Script paths below are relative to the skill root (`office-suite/`); PDF helpers live in `scripts/pdf/` and the document template in `assets/pdf_template.py`. Set up the Python environment once with `uv sync` from the skill root, then run scripts with `uv run python ...`.

## ⚠️ Agent Execution Rules (read before touching any code)

These rules exist because PDF generation tasks have historically caused **runaway context and cost**. Follow them without exception.

1. **Plan completely before executing.** Write the full script to a file first, then run once. Never write-run-fix in a loop.
2. **Large content → chunked heredoc only.** If content exceeds ~60 lines, use `cat >> file << 'TAG'` chunks (≤80 lines each). Never use the `write` tool or single-exec heredocs for large scripts — they silently drop the `content`/`command` parameter.
3. **No iterative screenshot review.** Render pages to PNG to verify layout, but read at most 3 sample pages (cover + 1 body + 1 formula/table page). Do not read every page.
4. **Fix bugs with targeted sed/python patches**, not full rewrites. If a script has a bug, patch the specific lines.
5. **No color in academic/technical documents unless explicitly requested.** Default style: pure black, matching the templet.pdf reference (see `tech-doc-layout` section below).

---

## Decision Tree

Pick the right path before writing anything:

| Goal | Tool / Path |
|------|-------------|
| Extract text (digital PDF) | `pdfplumber` or `pdftotext` CLI |
| Extract tables | `pdfplumber` |
| Extract text (scanned PDF) | `pytesseract` + `pdf2image` |
| Merge / split / rotate / watermark | `pypdf` or `qpdf` CLI |
| Create a new formatted document | `reportlab` — see **Tech Doc Layout** below |
| Fill a PDF form | → Read **[pdf-forms.md](pdf-forms.md)** first, follow every step |
| Encrypt / decrypt | `pypdf` or `qpdf` |
| Extract embedded images | `pdfimages -all` CLI |
| Render pages to images | `pypdfium2` or `scripts/pdf/convert_pdf_to_images.py` |
| Advanced / JS / performance | → Read **[pdf-reference.md](pdf-reference.md)** |

---

## Tech Doc Layout (default for generated documents)

Derived from measured values of `templet.pdf` (Xi'an University thesis template).
**Use these values as defaults** for all generated technical documents unless the user specifies otherwise.

```
Page:       A4 (595.28 × 841.89 pt)
Margins:    Left 85pt  Right 71pt  Top 90pt  Bottom 55pt
Body width: 439pt

Header:     Document title centered, 9pt
            Double black hairlines at y = PAGE_H-78 and PAGE_H-80  (0.5pt each)
Footer:     Single hairline at BOTTOM+14pt, page number centered below

Fonts:      Register FreeSerif.otf family as DocSerif / DocSerifB / DocSerifI
            (path: /usr/share/fonts/opentype/freefont/)
            Use registerFontFamily(), NOT addMapping()
            Fallback: Times-Roman / Times-Bold / Times-Italic
            Code blocks: Courier, 9pt, light-grey background (#F4F4F4)

Sizes:      H1 (chapter)  16pt bold  centered   spaceAfter=12
            H2 (section)  13pt bold  left        spaceAfter=4
            Body          12pt       justified   leading=20
            Caption        10pt       centered    spaceAfter=10
            Code            9pt       left        leading=13
            Footer/header   9pt

Colour:     BLACK only — no blue, no colour accents whatsoever

Tables:     0.5pt black grid lines, no fill, repeat header row
Formulas:   Centered in a 2-col Table([formula_text, num]), right-align number
            Use <sub>/<super> tags for sub/superscripts (NOT Unicode ₂ ²)
Figures:    matplotlib, dpi=150, facecolor='white'
            Caption below figure, centered 10pt
Cover:      Double thick rule (2pt) top and bottom; no colour bands
TOC:        Use reportlab TableOfContents + doc.multiBuild()
```

Template script: `assets/pdf_template.py` — base this for all new documents.

---

## Python Environment

```bash
# One-time setup, from the office-suite/ skill root — creates .venv from pyproject.toml
uv sync

# Run any script or inline snippet through the skill environment
uv run python script.py
```

`uv run` auto-creates/updates `.venv` from the skill's `pyproject.toml`, which already pins `pypdf`, `pdfplumber`, `reportlab`, `pypdfium2`, `pdf2image`, `pytesseract`, and `matplotlib`. Do not use the system `python3` directly. System tools (`qpdf`, `pdftoppm`, `pdftotext`, `tesseract`) install via the OS package manager.

---

## Common Tasks

### Extract Text
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```
CLI (fastest): `pdftotext -layout input.pdf output.txt`

### Extract Tables → Excel
```python
import pdfplumber, pandas as pd
with pdfplumber.open("doc.pdf") as pdf:
    dfs = [pd.DataFrame(t[1:], columns=t[0])
           for p in pdf.pages for t in p.extract_tables() if t]
pd.concat(dfs).to_excel("tables.xlsx", index=False)
```

### OCR Scanned PDF
```python
import pytesseract
from pdf2image import convert_from_path
images = convert_from_path("scanned.pdf")
text = "\n\n".join(f"Page {i+1}:\n{pytesseract.image_to_string(img)}"
                   for i, img in enumerate(images))
```

### Merge / Split
```bash
qpdf --empty --pages doc1.pdf doc2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- part1.pdf
```

### ReportLab: subscripts/superscripts
```python
# NEVER use Unicode ₂ ² — they render as black boxes in built-in fonts
# Use XML tags inside Paragraph() only:
Paragraph("H<sub>2</sub>O and x<super>2</super>", style)
# For canvas.drawString() text, adjust fontSize + y manually
```

### Encrypt / Decrypt
```bash
qpdf --encrypt userpass ownerpass 256 -- input.pdf encrypted.pdf
qpdf --password=secret --decrypt encrypted.pdf decrypted.pdf
```

### Render Pages to PNG
```bash
# Use the bundled script (handles output dir creation etc.)
uv run python scripts/pdf/convert_pdf_to_images.py input.pdf output_dir/
```

---

## Scripts (in `scripts/pdf/` directory)

Always prefer these over hand-rolled equivalents.

| Script | Usage |
|--------|-------|
| `scripts/pdf/convert_pdf_to_images.py <pdf> <dir/>` | Render each page to PNG |
| `scripts/pdf/check_fillable_fields.py <pdf>` | Detect fillable form fields |
| `scripts/pdf/extract_form_field_info.py <pdf> <out.json>` | Dump field IDs, types, bounding boxes |
| `scripts/pdf/extract_form_structure.py <pdf> <out.json>` | Extract labels/lines/checkboxes from non-fillable PDFs |
| `scripts/pdf/check_bounding_boxes.py <fields.json>` | Validate bounding boxes before filling |
| `scripts/pdf/fill_fillable_fields.py <pdf> <values.json> <out.pdf>` | Fill interactive form fields |
| `scripts/pdf/fill_pdf_form_with_annotations.py <pdf> <fields.json> <out.pdf>` | Fill non-interactive forms via annotations |
| `scripts/pdf/create_validation_image.py` | Visual overlay to verify filled form output |

Run all scripts from the **skill root** (`office-suite/`) via `uv run python scripts/pdf/<script>.py`. Note `fill_fillable_fields.py` imports `extract_form_field_info` as a sibling module, so keep them together in `scripts/pdf/`.

---

---

## Visual Design System (Optional Enhancements)

For documents where visual quality matters (proposals, portfolios, reports), apply these design principles from `minimax-pdf`.

### Document Type → Color Palette

| Content Type | Mood | Background | Accent | Text |
|-------------|------|------------|--------|------|
| Research, science | Authoritative | `#0F1F2E` deep ink | `#00B4A6` teal | `#F0EDE6` warm white |
| Business, finance | Confident | `#1C1C2B` near-black | `#E8A020` amber | `#F5F2EC` cream |
| Creative, portfolio | Expressive | `#1A0A2E` deep violet | `#FF6B6B` coral | `#FAF5FF` lavender |
| Education, academic | Scholarly | `#FAFAF7` warm white | `#2C4A7C` navy | `#1A1A2E` dark |
| Healthcare | Calm | `#F5F9F8` pale mint | `#2D8B72` forest | `#1E3830` deep green |
| Resume / personal | Clean | `#FFFFFF` white | pick from content | `#111111` near-black |
| Technical docs | Terminal | `#0D1117` near-black | `#39D353` neon green | `#E6EDF3` cool white |

**Rules:**
- One accent color only (appears on: cover elements, section rules, callout borders, table headers)
- Accent must contrast with background by 4.5:1 (WCAG AA)
- Avoid: purple gradients, navy+gold clichés, all-black backgrounds

### Cover Patterns

| Pattern | Best For | Visual Style |
|---------|----------|--------------|
| `fullbleed` | Reports, general | Deep bg, left-aligned title, dot-grid texture |
| `split` | Proposals | 42% left panel (color) + 58% right (off-white), hard divide |
| `typographic` | Resumes, academic | White bg, oversized title (60-80pt), first word in accent |
| `atmospheric` | Portfolios | Near-black, radial glow, centered-left title |
| `minimal` | Clean docs | White, 8px left accent bar, light-weight type |
| `magazine` | Publications | Warm cream, centered stack, hero image optional |
| `terminal` | Developer docs | Near-black, grid lines, monospace, neon accent |

### Typography Scale (for enhanced documents)

| Element | Size | Leading | Usage |
|---------|------|---------|-------|
| Display (cover title) | 54pt | 1.0 | Cover only |
| H1 (section) | 22pt | 1.3 | Major sections |
| H2 (subsection) | 15pt | 1.4 | Subsections |
| H3 | 11.5pt | 1.5 | Sub-subsection |
| Body | 10.5pt | 1.6 | Main prose |
| Caption | 8.5pt | 1.4 | Figure/table captions |
| Meta | 8pt | 1.3 | Headers/footers |

### Spacing System

```
margin_outer: 2.8cm (left/right)
margin_top: 2.8cm
margin_bottom: 2.5cm
section_gap: 26pt (before H1)
para_gap: 8pt (after paragraph)
line_gap: 17pt (body leading)
```

### Design Anti-Patterns (Never Use)

- ❌ Centered title on white with thin line underneath
- ❌ Gradients (reads as PowerPoint, not print)
- ❌ Drop shadows on text
- ❌ More than 3 colors
- ❌ Accent color on body text
- ❌ Rounded corners except callouts (4px max)
- ❌ Card components with colored headers

### Quality Bar

A designed PDF passes if:
- Cover has clear visual identity (not "generic AI output")
- Body text readable at arm's length
- Every page belongs to same document
- No elements bleed or overlap
- Page numbers present and correct
- Accent appears < 8 times per page on average

---

## Further Reading

- **[pdf-forms.md](pdf-forms.md)** — Full step-by-step form-filling workflow (fillable and non-fillable). Read before any form task.
- **[pdf-reference.md](pdf-reference.md)** — Advanced: pypdfium2, pdf-lib (JS), pdfjs-dist, batch processing, performance, troubleshooting.
- **[pdf-layout-defaults.md](pdf-layout-defaults.md)** — Measured layout defaults from the reference thesis template.

