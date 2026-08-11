# firecrawl-anydoc usage reference

Use `firecrawl-anydoc` for Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV, and text-based PDF files. The PyPI package is `firecrawl-anydoc`; the Python import is `anydoc`.

## Supported formats

| Family | Extensions |
|---|---|
| Word | `.doc`, `.docx`, `.docm` |
| PowerPoint | `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm` |
| Excel | `.xls`, `.xlsx`, `.xlsm`, `.xlsb` |
| OpenDocument | `.odt`, `.ods`, `.odp` |
| Other | `.rtf`, `.epub`, `.csv`, `.pdf` |

The parser normally detects formats from file contents. CSV has no content signature, so provide its extension or the explicit `csv` format when converting bytes.

## Python API

```python
from pathlib import Path
import anydoc

source = Path("report.docx")
markdown = anydoc.to_markdown(source)
binary_markdown = anydoc.to_markdown_bytes(data)
csv_markdown = anydoc.to_markdown_bytes(data, "csv")
document = anydoc.to_document(data)
```

Format inspection helpers:

```python
anydoc.format_from_bytes(data)
anydoc.format_from_extension(".pptm")
anydoc.format_from_path("report.odt")
```

## Errors

- `anydoc.UnsupportedError`
- `anydoc.MalformedError`
- `anydoc.EncryptedError`
- `anydoc.ResourceLimitError`
- `anydoc.MissingPartError`
- `OSError` for file reads

Conversion-specific exceptions inherit from `anydoc.ConvertError`.

## Embedded assets

Embedded image or object alt text appears in Markdown. When raw asset bytes and media types are needed, convert bytes with `anydoc.to_document(data)` and inspect `document.assets`.

## PDF limitation

Use anydoc for PDFs with an extractable text layer. A scanned or image-only PDF needs OCR. If conversion returns little or no body text, compare with local MarkItDown and then route to local OCR if necessary.
