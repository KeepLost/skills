# Excel / XLSX Reference

Loaded from `office-suite`. All script paths below are relative to the skill root (`office-suite/`).

## When to Use

Use when the main artifact is a Microsoft Excel workbook or spreadsheet file, especially when formulas, dates, formatting, merged cells, workbook structure, or cross-platform behavior matter. Also use for financial models with color-coded conventions or any task requiring formula recalculation.

---

## Tool Selection

- **pandas**: Data analysis, reshaping, bulk operations, CSV-like tasks.
- **openpyxl**: Formulas, styles, sheets, comments, merged cells, workbook preservation.
- Do not use pandas for format-sensitive writes; do not use openpyxl for heavy numerical analysis.

---

## Core Rules

### 1. Keep calculations in Excel, not Python

Write formulas into cells instead of computing in Python and hardcoding results. Use references to assumption cells instead of magic numbers.

```python
# ❌ Wrong – hardcodes Python result
sheet['B10'] = df['Sales'].sum()

# ✅ Correct – Excel formula stays live
sheet['B10'] = '=SUM(B2:B9)'
```

Verify all formulas: check absolute vs. relative references, off-by-one row/column indices, cross-sheet reference syntax (`Sheet1!A1`), and division-by-zero denominators before delivery. A workbook ships with **zero** formula errors — no `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A` left for the user to fix.

### 2. Recalculate with the script — mandatory when formulas are present

`openpyxl` writes formula strings but does not evaluate them. After every write that includes formulas, run:

```bash
uv run python scripts/xlsx/recalc.py <excel_file> [timeout_seconds]
```

The script:
- Sets up the LibreOffice macro on first run (handles sandboxed AF_UNIX restrictions automatically via `scripts/office/soffice.py`)
- Recalculates all formulas across all sheets
- Scans every cell for Excel errors
- Returns JSON:

```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {}
}
```

If `status` is `errors_found`, read `error_summary` for error types and cell locations, fix them, and recalculate again. Do not deliver until `status` is `success`.

#### ⚠️ LibreOffice cold-start is slow — set a long timeout

On first run in a fresh environment, LibreOffice must initialise its user profile directory (`~/.config/libreoffice/`) and write the macro file. This can take **60–120 seconds**. Always pass an explicit timeout:

```bash
uv run python scripts/xlsx/recalc.py output.xlsx 90
```

Do **not** kill the process just because it appears to hang; wait for the full timeout. Subsequent runs on the same machine are much faster because the profile already exists.

#### ⚠️ Run scripts/xlsx/recalc.py via the skill environment

`recalc.py` imports `openpyxl`. Run it through the skill's own `.venv` (see "Python environment" below) so the dependency is guaranteed present:

```bash
uv run python scripts/xlsx/recalc.py output.xlsx 90
```

### 3. Protect data types

- Store long identifiers, phone numbers, ZIP codes, and leading-zero values as text.
- Excel silently truncates numeric precision past 15 digits.
- Mixed text-number columns need explicit handling on both read and write.
- Watch for silent corruption: scientific notation, auto-parsed dates, stripped leading zeros.

### 4. Dates are serial numbers with quirks

- Excel stores dates as serial day integers, not real date objects.
- The 1900 system includes a false leap-day bug; some workbooks use the 1904 system.
- Time is a fractional day. Both value conversion and number format must be correct — a numerically right date can still display wrong.

### 5. Preserve workbook structure before changing content

- Existing templates override every guideline in this skill.
- Only the top-left cell of a merged range stores a value.
- Hidden rows, hidden columns, named ranges, and external references can still drive formulas.
- Match styles for newly written cells instead of introducing a new visual system.
- Preserve sheet order, column widths, row heights, freezes, filters, print settings, validations, and conditional formats unless the task explicitly changes them.

### 6. Scale to file size

Large workbooks can fail because of memory spikes or padded empty rows. For big files:
- Use `read_only=True` when only reading.
- Target specific sheets and columns rather than loading the whole workbook.
- Use `write_only=True` for pure write passes on large new files.

---

## Financial Model Standards

Apply these standards to all financial model deliverables unless the file has an established template (template conventions always win).

### Font
Use a consistent professional font (Arial or Times New Roman) throughout.

### Color Coding

| Color | Meaning |
|---|---|
| Blue text `RGB(0,0,255)` | Hardcoded inputs — values users change for scenarios |
| Black text `RGB(0,0,0)` | All formulas and calculations |
| Green text `RGB(0,128,0)` | Links pulling from other worksheets in the same workbook |
| Red text `RGB(255,0,0)` | External links to other files |
| Yellow background `RGB(255,255,0)` | Key assumptions needing attention |

### Number Formats

| Type | Format |
|---|---|
| Years | Text string — `"2024"`, not `2,024` |
| Currency | `$#,##0` — always include units in headers, e.g. `Revenue ($mm)` |
| Zeros | `$#,##0;($#,##0);-` — zeros display as `-` including percentages |
| Percentages | `0.0%` (one decimal) |
| Valuation multiples | `0.0x` |
| Negative numbers | Parentheses `(123)`, not minus `-123` |

### Assumptions and Hardcode Documentation

- Place all assumptions (growth rates, margins, multiples) in dedicated assumption cells.
- Use cell references in formulas, never inline constants: `=B5*(1+$B$6)` not `=B5*1.05`.
- Document every hardcode in a comment or adjacent cell:
  - `Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]`
  - `Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity`

---

## Common Workflows

### Python environment

This skill ships a `pyproject.toml` at its root. Create the local `.venv` once with `uv sync` (run from the `office-suite/` skill directory), then run every Python command through it:

```bash
# One-time setup, from the office-suite/ skill root
uv sync

# Run a build script
uv run python build_my_sheet.py

# Run recalc
uv run python scripts/xlsx/recalc.py output.xlsx 90
```

`uv run` auto-creates/updates `.venv` from `pyproject.toml`, so `openpyxl` and `pandas` are always present. Do not fall back to the system `python3`.

### Create a new workbook

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws['A1'] = 'Label'
ws['B1'] = '=SUM(B2:B9)'
ws['A1'].font = Font(bold=True)
ws.column_dimensions['A'].width = 20
wb.save('output.xlsx')
```

Then recalculate: `uv run python scripts/xlsx/recalc.py output.xlsx`

### Edit an existing workbook

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')  # preserves formulas and formatting
ws = wb['SheetName']
ws['A1'] = 'Updated'
ws.insert_rows(2)
wb.save('existing.xlsx')
```

Then recalculate if formulas are present.

### Read data for analysis

```python
import pandas as pd

df = pd.read_excel('file.xlsx', dtype={'id': str}, parse_dates=['date_col'])
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)
```

### Read calculated values back (after recalc)

```python
from openpyxl import load_workbook

wb = load_workbook('output.xlsx', data_only=True)
# WARNING: never save a data_only workbook — it replaces formulas with static values
```

---

## Formula Verification Checklist

Before delivering any file with formulas:

- [ ] Test 2–3 sample cell references manually before filling a whole block
- [ ] Confirm Excel column mapping (column 64 = BL, not BK — openpyxl is 1-indexed)
- [ ] Row offset: DataFrame row N = Excel row N+1 (Excel is 1-indexed)
- [ ] Check for NaN/null values with `pd.notna()` before writing
- [ ] Verify denominators before any division formula (`#DIV/0!`)
- [ ] Cross-sheet references use correct format: `Sheet1!A1`
- [ ] Absolute references (`$A$1`) where the formula will be copied
- [ ] Run `scripts/xlsx/recalc.py` and confirm `status: success`

---

## Common Traps

- Type inference on read can leave numbers as text or convert IDs into damaged numeric values.
- Column indexing varies across tools — off-by-one mistakes are common in generated formulas.
- Newlines in cells need `wrap_text=True` to display correctly.
- External references break when source files move.
- `.xlsm` can contain macros; `.xls` is a tighter legacy format.
- Google Sheets and LibreOffice may reinterpret dates, formulas, or styling differently from Excel.
- Dynamic array functions (`FILTER`, `XLOOKUP`, `SORT`, `SEQUENCE`) may fail in older viewers.
- A workbook can look correct while carrying stale cached values from a prior recalculation.
- Saving a workbook opened with `data_only=True` permanently destroys all formulas.
- Copying formulas without checking relative references can corrupt an entire block silently.
- Hidden sheets, named ranges, validations, and merged areas often carry business logic invisible in a quick skim.
- Conditional formatting, filters, print areas, and data validation often carry business meaning even when users only mention numbers.
- A workbook can be numerically correct and still fail visually because wrapped text, clipped labels, or narrow columns were never reviewed.
- Password protection in old Excel workflows is not real security.
- **`openpyxl.styles.numbers` import names differ by version** — `FORMAT_NUMBER_COMMA_SEP1` does not exist; the correct name is `FORMAT_NUMBER_COMMA_SEPARATED1`. Prefer inline format strings (e.g. `'"$"#,##0.00'`) over importing named constants to avoid version-specific breakage.
- **`uvx` rejects combining `--python` with a bare `python3` shebang** — when using `uvx --python X.Y`, invoke the script with `python` not `python3`, or omit `--python` entirely and let uv resolve the version from the project.

---

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `csv` — Plain-text tabular import and export workflows.
- `data-analysis` — Higher-level analysis that can feed workbook deliverables.

