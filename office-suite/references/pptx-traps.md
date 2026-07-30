# Common Traps

These are known, real failure modes. Check this list before declaring the deck finished.

---

## Template & Structure

- **Placeholder text survives template reuse** if not explicitly replaced. Run `grep -iE "xxxx|lorem|ipsum"` on markitdown output before delivery.
- **Placeholder/layout indexes are not portable.** What's index 1 in one deck is index 3 in another. Always inspect the actual XML — never assume.
- **Master and layout settings override direct slide edits.** If a slide-level change isn't working, the real source is in the master or layout definition.
- **Combining or duplicating slides without normalizing themes/masters** creates subtle per-slide inconsistency — fonts, colors, and spacing can drift slide by slide.
- **Aspect-ratio mismatch** (16:9 vs 4:3) shifts every placement decision even when individual slides look locally reasonable.
- **Never manually copy slide files.** Use `add_slide.py`. Manual copying breaks notes references, `Content_Types.xml`, and relationship IDs.

## Content & Layout

- **Template item count ≠ source item count.** If the template has 4 members but you have 3, delete the 4th member's entire shape group (image + all text boxes). Just clearing text leaves orphaned visuals.
- **Forcing content into the wrong layout.** Count your actual items/columns/images *before* picking a layout. Choosing a 3-column layout for 2 items leaves an empty placeholder; choosing a dense text layout for a chart wastes the visual.
- **Charts break silently when category counts or series lengths don't match the data.**
- **Text overflow** from longer-than-expected replacements is only visible after rendering — can't catch it in XML.

## Editing

- **"Use Edit tool, not sed or Python scripts"** — the Edit tool forces specificity about what to replace; scripts tend to overmatch or corrupt XML structure.
- **Concatenating multi-item content into one `<a:t>` string** instead of separate `<a:p>` elements breaks list formatting and line spacing.
- **`xml.etree.ElementTree` corrupts namespaces** in OOXML. Use `defusedxml.minidom`.
- **Font substitution** shifts line breaks and can wreck careful spacing — always test with visual QA when fonts may not be installed.
- **Smart quotes in new text**: the Edit tool converts them to ASCII. Use XML entities (`&#x201C;`, `&#x201D;`, `&#x2018;`, `&#x2019;`).

## Visual QA

- **A deck can pass text extraction and still fail visually** — overlap, clipping, wrong theme inheritance, or broken notes are invisible to markitdown.
- **One fix often creates another problem.** Always re-check affected slides after each fix cycle.
- **Thumbnail grid is for layout selection only.** Use soffice + pdftoppm for QA — thumbnail resolution is too low to catch layout bugs.
- **Speaker notes, comments, and linked media** can stay broken even when the visible slide looks fine. QA them separately.

## ⚠️ Script Generation Timeout (Session-Level Trap)

**Symptom**: Response times out before the tool call is even made, when generating a large PptxGenJS script in a single turn.

**Root cause**: Generating a complete multi-slide deck script in one model response (e.g. 12 slides with many shapes, coordinates, colors) produces thousands of tokens. If the session `timeoutSeconds` is tight, the response is cut off before finishing — no tool call is made, no file is written.

**Prevention — mandatory for any deck with 6+ slides:**

1. **Split the script into chunks** using `cat >> /tmp/make_ppt.js << 'CHUNKn'` heredoc blocks (each ≤ ~80 lines / ≤ 3 slides)
2. Append all chunks first, then run `node /tmp/make_ppt.js` once at the end
3. Never attempt to generate the full script in a single code block or single exec call

```bash
# Pattern (repeat for each chunk)
cat >> /tmp/make_ppt.js << 'CHUNK1'
// slides 1-3 ...
CHUNK1

cat >> /tmp/make_ppt.js << 'CHUNK2'
// slides 4-6 ...
CHUNK2

# Only run after all chunks are written
node /tmp/make_ppt.js
```

**Alternative**: Delegate script generation to OpenCode entirely; the main session only defines requirements and does QA.

---

## PptxGenJS-Specific

See [pptx-pptxgenjs.md](pptx-pptxgenjs.md) **Common Pitfalls** section — in particular:
- Never use `#` in hex colors (file corruption)
- Never encode opacity in 8-char hex strings (file corruption)
- Never reuse option objects across `addShape`/`addText` calls (PptxGenJS mutates objects in-place)
- Negative shadow offset corrupts the file — use `angle: 270` with positive offset for upward shadows

## Video Embedding (OOXML zip surgery)

When splicing a video slide from one pptx into another via zip manipulation:

- **Every `r:link`, `r:embed`, `r:id` in the slide XML must resolve to a relationship in the slide's `.rels` file** — if any rId is dangling, PowerPoint silently deletes the shape on "repair"
- **Do not patch rIds with regex substitution across different pptx files** — IDs from the source file have no guaranteed correspondence to IDs in the target file; always build the new `.rels` from scratch with explicit, verified mappings
- **The safest approach**: take the source slide XML as-is, only remap the layout (rId→slideLayout) and notes (rId→notesSlide) entries to the target deck's actual paths; leave all media rIds unchanged and add matching entries in the new `.rels`
- **Verify after assembly**: check that every `r:(link|embed|id)="rIdN"` in the slide XML has a corresponding `Id="rIdN"` entry in `.rels` pointing to a real file in the zip
- **LibreOffice PDF conversion is not a reliable validator for video** — it can render the PDF successfully while the video relationship is still broken for PowerPoint; always check the rId mapping explicitly in code
