# Word / DOCX Reference

Loaded from `office-suite`. Script paths below are relative to the skill root (`office-suite/`). Shared OOXML tooling lives in `scripts/office/`; DOCX-specific helpers live in `scripts/word/`. Set up the Python environment once with `uv sync` from the skill root, then run scripts with `uv run python ...`.

## Design Principles

Before writing any code, understand these principles — they govern every decision.

### Structure over appearance

A `.docx` is a ZIP of XML parts, not a rendered page. Styles, numbering, relationships, and references are structural — they determine whether the document stays correct after editing, saving, or opening in another editor. Always fix structure, not appearance.

### Use named styles, never direct formatting stacks

Apply named paragraph/character styles. Direct formatting (`<w:rPr>` overrides) is acceptable only for one-off exceptions. Stacking direct formatting on top of named styles creates drift when the document is edited later.

### Ask the user for design decisions; apply defaults otherwise

The following are **defaults** — apply them without asking:

| Setting | Default |
|---|---|
| Paper | A4 |
| Margins | Top 3cm · Bottom 2cm · Inner 2.5cm · Outer 2.5cm · Gutter 0.5cm |
| Header distance | 2cm |
| Footer distance | 1.75cm |
| Body line spacing | Fixed 20pt |
| Body font (Chinese) | 宋体 (SimSun) |
| Body font (English/numbers) | Times New Roman |
| Body size | 小四 (11pt) |
| H1 font | 黑体 (SimHei), 三号 (16pt), bold, centered, spacing before 24pt after 18pt |
| H2 font | 宋体 bold, 小三 (15pt), no indent, spacing before 18pt after 12pt |
| H3 font | 宋体 bold, 四号 (14pt), indent 1 char, spacing before 12pt after 6pt |
| Figure/table captions | 宋体 + Times New Roman, 五号 (10.5pt) |
| Header text | 宋体, 五号, centered |
| Page numbers (front matter) | Roman numerals, Times New Roman, 小五 (9pt), centered |
| Page numbers (body) | Arabic numerals, 宋体, 小五 (9pt), centered |
| First-line indent | 2 characters (Chinese text); no indent for English-only paragraphs |
| Heading numbering | 第一章 / 1.1 / 1.1.1; subsections as (1)(2) |
| Figure numbering | 图1.3 (chapter.seq), caption below figure |
| Table numbering | 表2.5 (chapter.seq), caption above table |
| Formula numbering | (3-32) right-aligned on same line |

**Ask the user first** for: overall document style/theme, color usage, font substitutions, non-standard layouts, or any design decision not covered above.

### Deterministic operations go to scripts

Operations with a single correct answer — unpacking, repacking, validation, adding comment scaffolding — are handled by the scripts in `scripts/`. Call them instead of writing equivalent Python inline.

Operations requiring judgment — content adjustments, style decisions, reviewing ambiguous changes — are handled by reasoning.

---

## Workflow Overview

| Task | Approach |
|---|---|
| Read / analyze content | `pandoc` or unpack for raw XML |
| Create new document | `docx-js` (JavaScript) — see **Creating Documents** |
| Create new document (Chinese-heavy) | `python-docx` — see **python-docx Alternative** |
| Edit existing document | Unpack → edit XML → repack — see **Editing Documents** |
| Convert `.doc` to `.docx` | `scripts/office/soffice.py` |
| Accept tracked changes | `scripts/word/accept_changes.py` |
| Convert to PDF / images | `soffice.py` then `pdftoppm` |

---

## Scripts Reference

All scripts live in `scripts/` relative to this skill directory. Pass absolute paths for all file arguments.

```bash
# Unpack DOCX to editable XML tree
python scripts/office/unpack.py input.docx unpacked/
# Options: --merge-runs false  (skip run merging)

# Repack XML tree back to DOCX
python scripts/office/pack.py unpacked/ output.docx --original input.docx
# Options: --validate false  (skip schema validation)

# Validate a DOCX
python scripts/office/validate.py doc.docx

# Convert legacy .doc or export to PDF
python scripts/office/soffice.py --headless --convert-to docx input.doc
python scripts/office/soffice.py --headless --convert-to pdf doc.docx

# Accept all tracked changes
python scripts/word/accept_changes.py input.docx output.docx

# Add a comment (text must be pre-escaped XML)
python scripts/word/comment.py unpacked/ 0 "Comment text with &amp; entities"
python scripts/word/comment.py unpacked/ 1 "Reply text" --parent 0
python scripts/word/comment.py unpacked/ 0 "Text" --author "Custom Author"
```

Auto-repair (during pack) fixes: `durableId` overflow, missing `xml:space="preserve"`.
Auto-repair does NOT fix: malformed XML, invalid nesting, missing relationships.

---

## Creating Documents (docx-js)

Install once: `npm install -g docx`

### Minimal skeleton

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel,
        AlignmentType, PageOrientation, LevelFormat,
        Table, TableRow, TableCell, ImageRun,
        Header, Footer, PageNumber, PageBreak,
        ExternalHyperlink, InternalHyperlink, Bookmark,
        FootnoteReferenceRun, BorderStyle, WidthType, ShadingType,
        VerticalAlign, TableOfContents,
        PositionalTab, PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: { /* see Styles section */ },
  numbering: { /* see Lists section */ },
  footnotes: { /* optional */ },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },          // A4 in DXA
        margin: { top: 1701, right: 1418, bottom: 1134, // 3cm / 2.5cm / 2cm
                  left: 1418, gutter: 284,               // 2.5cm / 0.5cm
                  header: 1134, footer: 992 }            // 2cm / 1.75cm
      }
    },
    headers: { default: new Header({ children: [/* header content */] }) },
    footers: { default: new Footer({ children: [/* footer content */] }) },
    children: [/* document body */]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('output.docx', buf);
  console.log('Done');
});
```

**DXA conversion:** 1 inch = 1440 DXA; 1 cm ≈ 567 DXA.  
A4: 21cm × 29.7cm = 11906 × 16838 DXA.

**Landscape:** Pass portrait dimensions + `orientation: PageOrientation.LANDSCAPE` — docx-js swaps internally.

### Styles

```javascript
styles: {
  default: {
    document: { run: { font: { ascii: "Times New Roman", eastAsia: "SimSun" }, size: 22 } } // 11pt = 小四
  },
  paragraphStyles: [
    { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 32, bold: true, font: { eastAsia: "SimHei" } },                           // 16pt 黑体
      paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 480, after: 360 },
                   outlineLevel: 0 } },                                                       // outlineLevel required for TOC
    { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 30, bold: true, font: { eastAsia: "SimSun" } },                           // 15pt 宋体
      paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 1 } },
    { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 28, bold: true, font: { eastAsia: "SimSun" } },                           // 14pt 宋体
      paragraph: { indent: { firstLine: 284 }, spacing: { before: 240, after: 120 },
                   outlineLevel: 2 } },
    { id: "Caption", name: "Caption", basedOn: "Normal", quickFormat: true,
      run: { size: 21, font: { ascii: "Times New Roman", eastAsia: "SimSun" } },             // 10.5pt 五号
      paragraph: { alignment: AlignmentType.CENTER } },
  ]
}
```

> **Use exact IDs** (`"Heading1"` etc.) to override Word's built-in styles.  
> Always include `outlineLevel` on heading styles — required for TOC to work.

### Line spacing (fixed 20pt, applies to all body paragraphs)

```javascript
new Paragraph({
  spacing: { line: 400, lineRule: "exact" },  // 400 = 20pt in half-points
  children: [new TextRun("Body text")]
})
```

Apply this to every body paragraph. For headings, use the style's `spacing` instead.

### Lists

```javascript
// ❌ NEVER manually insert bullet characters or unicode
// ✅ ALWAYS use numbering config

numbering: {
  config: [
    { reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "●",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbers",
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ]
}

// Usage
new Paragraph({ numbering: { reference: "bullets", level: 0 },
  children: [new TextRun("Item")] })
```

**Same reference = continues numbering; different reference = restarts.**

### Tables

```javascript
// CRITICAL rules:
// 1. Always use WidthType.DXA — never WidthType.PERCENTAGE (breaks in Google Docs)
// 2. Set width on both the table AND each cell — both must match columnWidths
// 3. Use ShadingType.CLEAR — never ShadingType.SOLID (causes black backgrounds)
// 4. Table width = sum of columnWidths exactly

const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9072, type: WidthType.DXA },  // A4 content width with default margins
  columnWidths: [4536, 4536],
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders, width: { size: 4536, type: WidthType.DXA },
          shading: { fill: "CCCCCC", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun({ text: "Header", bold: true })] })]
        }),
        // ... more cells
      ]
    }),
    // ... more rows
  ]
})
```

**Content width calculation (A4 default margins):**  
`11906 − 1418(left) − 1418(right) − 284(gutter) = 8786 DXA`  
Adjust when using non-default margins.

**Never use tables as visual dividers.** Use paragraph bottom border instead:
```javascript
new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 1 } },
  children: []
})
```

### Images

```javascript
// type is REQUIRED — specify: png | jpg | jpeg | gif | bmp | svg
new ImageRun({
  type: "png",
  data: fs.readFileSync("image.png"),
  transformation: { width: 200, height: 150 },
  altText: { title: "Figure title", description: "Description", name: "Name" }  // all three required
})
```

### Page breaks

```javascript
// PageBreak MUST be inside a Paragraph
new Paragraph({ children: [new PageBreak()] })
// or
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New section")] })
```

### Hyperlinks

```javascript
// External
new ExternalHyperlink({
  children: [new TextRun({ text: "Link text", style: "Hyperlink" })],
  link: "https://example.com"
})

// Internal (bookmark + reference)
new Bookmark({ id: "sec1", children: [new TextRun("Section Title")] })
new InternalHyperlink({ anchor: "sec1",
  children: [new TextRun({ text: "See Section 1", style: "Hyperlink" })] })
```

### Table of Contents

```javascript
// Headings must use HeadingLevel — no custom styles
new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" })
```

### Headers and Footers

```javascript
// Header with centered text (page-level style)
new Header({ children: [new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { line: 400, lineRule: "exact" },
  children: [new TextRun({ text: "Document Title", font: { eastAsia: "SimSun" }, size: 21 })]
})] })

// Footer with page numbers
new Footer({ children: [new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ children: [PageNumber.CURRENT], font: { eastAsia: "SimSun" }, size: 18 })]
})] })
```

### Tab stops (for TOC-style lines or dual-column headers)

```javascript
new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
  children: [new TextRun("Left text"), new TextRun("\tRight text")]
})
```

### Footnotes

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Footnote text")] }
  },
  sections: [{ children: [
    new Paragraph({ children: [
      new TextRun("Body text"),
      new FootnoteReferenceRun(1),
    ]})
  ]}]
})
```

### Validation

After generating, always validate:
```bash
python scripts/office/validate.py output.docx
```
If validation fails: unpack → inspect XML → fix → repack.

---

## Editing Documents (OOXML)

Follow these three steps in order. Never skip validation.

### Step 1 — Unpack

```bash
python scripts/office/unpack.py document.docx unpacked/
```

Extracts XML, pretty-prints it, merges adjacent runs, and converts smart quotes to XML entities so they survive string editing.

Edit files in `unpacked/word/`. The main file is `word/document.xml`. Styles are in `word/styles.xml`.

### Step 2 — Edit XML

**Use the Edit tool for string replacement. Do not write Python scripts for this.**

**Author name for tracked changes and comments:** Use a sensible default author name (e.g. `"Reviewer"`) unless the user specifies otherwise.

**Smart quotes in new content:**
```xml
<w:t>Here&#x2019;s a &#x201C;quoted&#x201D; term</w:t>
```

| Entity | Character |
|---|---|
| `&#x2018;` | ' (left single) |
| `&#x2019;` | ' (right single / apostrophe) |
| `&#x201C;` | " (left double) |
| `&#x201D;` | " (right double) |

**Element order inside `<w:pPr>`:** `<w:pStyle>` → `<w:numPr>` → `<w:spacing>` → `<w:ind>` → `<w:jc>` → `<w:rPr>` (last).

**Whitespace:** Add `xml:space="preserve"` to `<w:t>` with leading or trailing spaces.

**RSIDs:** Must be 8-digit hex, e.g. `00AB1234`.

### Step 3 — Repack

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

---

## Tracked Changes (XML)

**Make minimal replacements.** Only mark the changed span — never rewrite whole paragraphs.

```xml
<!-- Insertion -->
<w:ins w:id="1" w:author="Cristina" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>

<!-- Deletion -->
<w:del w:id="2" w:author="Cristina" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>

<!-- Replacing "30" with "60" — minimal form -->
<w:r><w:t xml:space="preserve">The term is </w:t></w:r>
<w:del w:id="1" w:author="Cristina" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Cristina" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t xml:space="preserve"> days.</w:t></w:r>
```

**Deleting an entire paragraph/list item** — also mark the paragraph mark as deleted, or accepting leaves an empty line:

```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>
    <w:rPr>
      <w:del w:id="1" w:author="Cristina" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Cristina" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content</w:delText></w:r>
  </w:del>
</w:p>
```

**Always copy `<w:rPr>` from original run** into the tracked-change run to preserve bold, size, etc.

---

## Comments (XML)

Use `comment.py` to generate comment scaffolding, then manually insert anchor markers in `document.xml`.

```bash
python scripts/word/comment.py unpacked/ 0 "Your comment here"
python scripts/word/comment.py unpacked/ 1 "Reply" --parent 0
```

Then in `document.xml`:

```xml
<!-- CRITICAL: commentRangeStart/End are siblings of <w:r>, NEVER inside <w:r> -->
<w:commentRangeStart w:id="0"/>
<w:r><w:t>annotated text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r>
  <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
  <w:commentReference w:id="0"/>
</w:r>
```

---

## Images (XML editing)

1. Copy image file to `unpacked/word/media/`
2. Add relationship in `unpacked/word/_rels/document.xml.rels`:
   ```xml
   <Relationship Id="rId99" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image.png"/>
   ```
3. Add content type in `[Content_Types].xml` if extension not already declared:
   ```xml
   <Default Extension="png" ContentType="image/png"/>
   ```
4. Insert in `document.xml` (1 inch = 914400 EMU):
   ```xml
   <w:drawing>
     <wp:inline>
       <wp:extent cx="5486400" cy="3429000"/>
       <a:graphic>
         <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
           <pic:pic>
             <pic:blipFill><a:blip r:embed="rId99"/></pic:blipFill>
           </pic:pic>
         </a:graphicData>
       </a:graphic>
     </wp:inline>
   </w:drawing>
   ```

---

## Common Pitfalls (do not repeat these)

- **`\n` in TextRun** — invalid; use separate Paragraph elements.
- **Unicode bullets** — never; use LevelFormat.BULLET with numbering config.
- **PageBreak outside Paragraph** — creates invalid XML.
- **ImageRun without `type`** — always specify png/jpg/etc.
- **WidthType.PERCENTAGE** — breaks in Google Docs; always use DXA.
- **Table without dual widths** — set `columnWidths` on Table AND `width` on each cell.
- **ShadingType.SOLID for color fill** — causes black backgrounds; use CLEAR.
- **Tables as visual dividers** — use paragraph bottom border instead.
- **TOC with custom heading styles** — must use built-in HeadingLevel.
- **Heading styles without `outlineLevel`** — TOC breaks.
- **Overriding built-in styles** — use exact IDs: `"Heading1"`, `"Heading2"`, etc.
- **Copy-paste between documents** — imports foreign styles and numbering definitions silently.
- **Header/footer image relationship IDs** — part-specific; reusing IDs across parts breaks images.
- **Empty paragraphs as spacing** — use `spacing` in paragraph properties instead.
- **Broad paragraph rewrites in review docs** — make minimal replacements to preserve review quality.
- **Missing `<w:del/>` in `<w:pPr><w:rPr>`** when deleting full paragraphs — leaves empty lines after accepting.
- **A4 vs Letter default** — docx-js defaults to A4 already; confirm and set explicitly regardless.
- **Image paragraph with fixed line spacing** — NEVER apply `lineRule: "exact"` / `WD_LINE_SPACING.EXACTLY` to a paragraph containing an image. Fixed line spacing locks the paragraph height to that value, causing text on the next line to overlap the image completely. Always use `SINGLE` or `AUTO` for image paragraphs.
- **docx-js with Chinese-heavy content** — ASCII double-quote `"` used as JS string delimiter conflicts with Chinese quotation marks `"…"` that render as the same codepoint (U+0022) after encoding. If content contains Chinese-style quotation marks or other characters that collide with JS string delimiters, switch to `python-docx` instead of fighting escaping.

---

## Dependencies

| Tool | Purpose | Install |
|---|---|---|
| `docx` (npm) | Create new documents (JS) | `npm install -g docx` |
| `python-docx` (pip) | Create new documents (Python, preferred for Chinese content) | `uv sync` (in `pyproject.toml`) |
| `pillow` (pip) | Generate images / charts for embedding | `uv sync` (in `pyproject.toml`) |
| `pandoc` | Text extraction | system package |
| LibreOffice | PDF export, `.doc` conversion | auto-configured via `scripts/office/soffice.py` |
| `pdftoppm` (Poppler) | PDF to image | system package |

Python dependencies come from the skill's `pyproject.toml` — run `uv sync` once from the skill root, then invoke scripts with `uv run python ...`. The `docx` npm package is a separate Node dependency.

---

## python-docx Alternative

Prefer `python-docx` over `docx-js` when:
- Document content is Chinese-heavy (Chinese quotation marks `"…"` / `'…'` collide with JS string delimiters and cause hard-to-debug `SyntaxError`)
- You're already working in Python (e.g., generating images with Pillow in the same script)

```python
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()
section = doc.sections[0]
section.page_width    = Cm(21)
section.page_height   = Cm(29.7)
section.top_margin    = Cm(3);  section.bottom_margin = Cm(2)
section.left_margin   = Cm(2.5); section.right_margin  = Cm(2.5)
section.header_distance = Cm(2); section.footer_distance = Cm(1.75)

# East Asia font helper (required — python-docx font.name only sets Latin font)
def set_east_asia_font(run, font_name):
    rpr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), font_name)
    rpr.insert(0, rFonts)

# Body paragraph (fixed 20pt line spacing, 2-char first-line indent)
def body_para(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(20)
    pf.space_before = Pt(0); pf.space_after = Pt(0)
    pf.first_line_indent = Cm(0.74)   # ≈ 2 Chinese chars at 11pt
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    set_east_asia_font(run, "SimSun")
    return p

# Image paragraph — MUST use SINGLE or AUTO line spacing, never EXACTLY
def image_para(doc, img_path, width_cm):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE   # ← critical: not EXACTLY
    pf.space_before = Pt(8); pf.space_after = Pt(6)
    run = p.add_run()
    run.add_picture(img_path, width=Cm(width_cm))
    return p

doc.save("output.docx")
```

**Critical rule for image paragraphs:**  
`WD_LINE_SPACING.EXACTLY` (固定值) locks the paragraph height to a fixed pt value. If that value is smaller than the image height (e.g., 20pt for a 7cm image), the image is clipped and subsequent text visually overlaps it. Always use `SINGLE` or omit `line_spacing_rule` for paragraphs that contain images.

