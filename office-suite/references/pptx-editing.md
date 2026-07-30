# Editing Presentations

## Template-Based Workflow

### 1. Inspect and inventory

```bash

python "scripts/pptx/thumbnail.py" template.pptx
python -m markitdown template.pptx
```

Review `thumbnails.jpg` for layouts. Review markitdown output for actual placeholder text and structure. **Answer the inventory checklist in SKILL.md before proceeding.**

### 2. Plan slide mapping

For each content section, choose a template slide that matches the content shape:

- **Match item count to layout** — if the layout has 3 columns but you have 2 items, pick a different layout
- **Vary layouts across the deck** — monotonous title+bullets is the most common failure mode
- **Content types and suitable layouts:**

| Content Type | Suitable Layout |
|---|---|
| Key points | Bullet slide |
| Team / profiles | Multi-column |
| Testimonials | Quote slide |
| Data / metrics | Stat callout or chart slide |
| Process / steps | Timeline or numbered flow |
| Section transition | Section divider |
| Evidence | Full-bleed image + overlay |

### 3. Unpack

```bash

python "scripts/office/unpack.py" template.pptx unpacked/
```

### 4. Structural changes (complete before editing content)

Do this yourself (not with subagents):

- **Delete slides**: remove from `<p:sldIdLst>` in `ppt/presentation.xml`
- **Duplicate slides**: `python "scripts/pptx/add_slide.py" unpacked/ slideN.xml`
- **Reorder slides**: rearrange `<p:sldId>` elements in `<p:sldIdLst>`
- **Never manually copy slide files** — `add_slide.py` handles notes references, `Content_Types.xml`, and relationship IDs that manual copying misses

### 5. Edit content

Use subagents if available — each slide is a separate XML file so edits can run in parallel. Include in the subagent prompt:
- Slide file path(s)
- **"Use the Edit tool for all changes"** (not sed or Python scripts — Edit forces specificity)
- The formatting rules and pitfalls below

For each slide:
1. Read the slide XML
2. Identify **all** placeholder content (text, images, charts, icons, captions)
3. Replace each placeholder with final content
4. Remove excess elements entirely when source has fewer items than the template — don't just clear text

### 6. Clean and pack

```bash
python "scripts/pptx/clean.py" unpacked/
python "scripts/office/pack.py" unpacked/ output.pptx --original template.pptx
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/office/unpack.py` | Extract and pretty-print PPTX XML |
| `scripts/pptx/add_slide.py` | Duplicate slide or create from layout |
| `scripts/pptx/clean.py` | Remove orphaned slides/media/rels |
| `scripts/office/pack.py` | Repack with validation |
| `scripts/pptx/thumbnail.py` | Visual grid of slide thumbnails |
| `scripts/office/soffice.py` | LibreOffice wrapper (auto-configured) |

---

## XML Formatting Rules

- **Bold headers and inline labels**: `b="1"` on `<a:rPr>` — applies to slide titles, section headers, inline labels like "Status:", "Note:"
- **No unicode bullets**: use `<a:buChar>` or `<a:buAutoNum>`, not `•`
- **Bullet style**: let bullets inherit from the layout; only specify `<a:buChar>` or `<a:buNone>` when you need to override
- **Multi-item content**: separate `<a:p>` elements per item, never concatenate into one string

**✅ Correct — separate paragraphs:**
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>Do the first thing.</a:t></a:r>
</a:p>
```

**❌ Wrong — all items in one string:**
```xml
<a:r><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
```

Copy `<a:pPr>` from the original paragraph to preserve line spacing.

### Smart Quotes

Handled automatically by unpack/pack. When the Edit tool adds new text with quotes, use XML entities:

| Character | Entity |
|-----------|--------|
| `"` left | `&#x201C;` |
| `"` right | `&#x201D;` |
| `'` left | `&#x2018;` |
| `'` right | `&#x2019;` |

### Other

- **Leading/trailing spaces**: `xml:space="preserve"` on `<a:t>`
- **XML parsing**: use `defusedxml.minidom`, not `xml.etree.ElementTree` (corrupts namespaces)

---

## Common Pitfalls

See [pptx-traps.md](pptx-traps.md) for the full list. Highest-impact ones for template editing:

- **Template slots ≠ source item count**: if template has 4 team members but you have 3, delete the 4th member's entire shape group (image + text boxes), not just the text
- **Master/layout overrides**: if a direct slide edit isn't showing up, the real source of truth is in the master or layout definition
- **Font substitution**: can shift line breaks and wreck spacing — test with visual QA
- **Content/item count mismatch with charts**: category counts and data series lengths must match or charts break
