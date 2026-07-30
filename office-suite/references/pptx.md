# PowerPoint / PPTX Reference

Loaded from `office-suite`. Script paths below are relative to the skill root (`office-suite/`). Shared OOXML tooling lives in `scripts/office/`; PPTX-specific helpers live in `scripts/pptx/`. Set up the Python environment once with `uv sync` from the skill root, then run scripts with `uv run python ...`.

## Quick Reference

| Task | Guide |
|------|-------|
| Read / inspect content | See **Inspection** below |
| Edit or create from template | Read [editing.md](pptx-editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptx-pptxgenjs.md) |
| Design guidance | Read [design.md](pptx-design.md) |
| Traps & failure modes | Read [traps.md](pptx-traps.md) |

---

## Step 0 — Choose Your Workflow

Before touching any file, pick the right path:

| Situation | Workflow |
|-----------|----------|
| Just read or extract text | Run inspection commands below. Stop. |
| Existing deck to edit | Inventory first, then [editing.md](pptx-editing.md) |
| Template to rebuild | Inventory first, then [editing.md](pptx-editing.md) |
| No source file at all | [pptxgenjs.md](pptx-pptxgenjs.md) |

**Do not skip the inventory step for template or editing work.** Placeholder indexes and layout indexes are not portable assumptions — they vary per deck.

---

## Inspection

These commands are deterministic. Run them; don't guess what's in the file.

```bash
# Full text extraction (content, notes, placeholder text)
uvx "markitdown[pptx]" presentation.pptx

# Visual layout overview (thumbnails.jpg, 3-col grid, max 12 per grid)
python scripts/pptx/thumbnail.py presentation.pptx

# Check for leftover placeholder text
uvx "markitdown[pptx]" presentation.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"

# Unpack to examine raw XML structure
python scripts/office/unpack.py presentation.pptx unpacked/
```

> **Use `thumbnail.py` for layout selection only.** For visual QA, use the full-resolution pipeline in [editing.md](pptx-editing.md).

---

## Inventory Checklist (required before editing)

Run inspection, then answer:

- [ ] How many slides? What layouts exist?
- [ ] What are the actual placeholder names/indexes on each layout?
- [ ] Are there speaker notes, comments, or linked media?
- [ ] What fonts, colors, and spacing does the theme use?
- [ ] Are master/layout settings likely to override direct slide edits?

**Never assume placeholder or layout indexes. Always read the actual XML.**

---

## QA — Required, Not Optional

Every deck gets two separate QA passes:

### 1. Content QA
```bash
uvx "markitdown[pptx]" output.pptx
uvx "markitdown[pptx]" output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```
Check for missing content, wrong order, leftover placeholders.

### 2. Visual QA
Convert to images first:
```bash
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
# Result: slide-01.jpg, slide-02.jpg, ...

# Re-render specific slides after fixes:
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

Then inspect with a subagent. **Batch no more than 3–4 slides per subagent call** to avoid timeout. Use this prompt per batch:
```
Visually inspect these presentation slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words)
- Text overflow or cut off at edges/box boundaries
- Decorative lines sized for single-line titles that wrapped to two lines
- Footers or citations colliding with content above
- Elements too close (< 0.3" gaps) or nearly touching
- Uneven spacing (large gap one side, cramped the other)
- Insufficient margin from slide edges (< 0.5")
- Misaligned columns or similar elements
- Low-contrast text or icons against the background
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list all issues including minor ones:
1. /path/to/slide-01.jpg (Expected: title slide)
2. /path/to/slide-02.jpg (Expected: timeline)
...
```

> ⚠️ **Batch size matters**: spawning a subagent with 10+ slides at once risks timeout before output is produced. Split into batches of 3–4 slides and set `runTimeoutSeconds` to at least 180.

### Verification Loop

1. Generate → convert to images → inspect (in batches)
2. List issues found (if none found, look harder)
3. Fix → re-inspect affected slides
4. Repeat until a full pass finds nothing new

**Do not declare success before completing at least one fix-and-verify cycle.**

---

## Dependencies

```bash
# Python deps (Pillow etc.) come from the skill's pyproject.toml:
uv sync                       # run once from the office-suite/ skill root
# markitdown for text extraction (isolated, no project dep needed):
uvx "markitdown[pptx]" presentation.pptx
# Node dep for creating decks from scratch:
npm install -g pptxgenjs
# LibreOffice (soffice) — handled by scripts/office/soffice.py
# Poppler (pdftoppm) — for PDF-to-image conversion
```

