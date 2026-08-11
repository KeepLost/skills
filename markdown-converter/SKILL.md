---
name: "markdown-converter"
description: "Convert documents and files to Markdown using available tools. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis."
---

# Markdown Converter

Convert supported files to Markdown with the skill-local Python environment. Prefer `firecrawl-anydoc` for office documents. Use MarkItDown for web and data formats, archives, messages, media, and fallback conversion.

## Prepare the environment

From the directory containing this `SKILL.md`, install the declared dependencies:

```bash
uv sync
```

Use the resulting interpreter:

```text
<skill-directory>/.venv/bin/python
```

Confirm both backends are available:

```bash
<skill-directory>/.venv/bin/python -c 'import anydoc, markitdown; print("ready")'
```

## Choose the backend

| Input or situation | Use |
|---|---|
| DOC, DOCX, DOCM | firecrawl-anydoc |
| PPT, PPTX, PPS, POT and related presentation formats | firecrawl-anydoc |
| XLS, XLSX, XLSM, XLSB | firecrawl-anydoc |
| ODT, ODS, ODP, RTF | firecrawl-anydoc |
| EPUB, CSV | firecrawl-anydoc |
| Text-based PDF | firecrawl-anydoc first; MarkItDown if incomplete |
| HTML, JSON, XML | MarkItDown |
| ZIP, Outlook messages | MarkItDown |
| Image or audio metadata | MarkItDown |
| Scanned or image-only PDF | local OCR workflow |
| Remote URL, YouTube, hosted OCR, cloud conversion, or external model/API | explain the network operation and obtain explicit user consent first |

## Convert with firecrawl-anydoc

Use it for office documents, OpenDocument files, RTF, EPUB, CSV, and text-based PDFs.

```python
from pathlib import Path
import anydoc

source = Path("report.docx")
target = Path("report.md")
markdown = anydoc.to_markdown(source)
target.write_text(markdown, encoding="utf-8")
```

For in-memory data:

```python
markdown = anydoc.to_markdown_bytes(data)
csv_markdown = anydoc.to_markdown_bytes(data, "csv")
```

Use `anydoc.to_document(data)` when embedded assets must be inspected or saved separately. PDF conversion returns Markdown directly and does not expose the shared document model.

Relevant failures include `UnsupportedError`, `MalformedError`, `EncryptedError`, `ResourceLimitError`, and `MissingPartError`. If a text PDF fails or produces incomplete output, try MarkItDown. If both backends return little or no text, route it to local OCR.

See [references/anydoc.md](references/anydoc.md).

## Convert with MarkItDown

Use it for HTML, JSON/XML, ZIP, Outlook messages, media metadata, and formats outside anydoc's scope. It can also act as a second parser for text PDFs and modern office files.

```python
from pathlib import Path
from markitdown import MarkItDown

source = Path("page.html")
target = Path("page.md")
converter = MarkItDown(enable_plugins=False)
result = converter.convert_local(source)
target.write_text(result.text_content, encoding="utf-8")
```

For a local stream:

```python
with source.open("rb") as stream:
    result = converter.convert_stream(stream, file_extension=source.suffix)
```

Keep plugins disabled unless a specific plugin is needed and its behavior is understood.

See [references/markitdown.md](references/markitdown.md).

## Network consent

Before any conversion step that may contact an external service:

1. identify the service or endpoint and explain why it is needed;
2. state what file content or metadata may leave the machine;
3. mention required credentials and possible charges when relevant;
4. obtain the user's explicit consent for that operation.

This applies to remote URLs, YouTube retrieval, hosted OCR or conversion, Azure integrations, external LLM/vision/transcription endpoints, and plugins that may use the network. Do not infer consent from configured credentials, previous consent, or a general request to convert a file.

Local file conversion with `anydoc`, `convert_local`, or `convert_stream` does not require this consent step when no plugin or external endpoint is involved.

## PDF workflow

1. Convert with `anydoc.to_markdown(path)`.
2. Check that expected body text and page order are present.
3. If the result is incomplete, convert the same file with local MarkItDown and compare.
4. If both results contain little or no text, use local OCR.
5. Use hosted OCR or vision only after completing the network-consent steps.

## Verify the result

- confirm the Markdown file exists and is non-empty;
- inspect the beginning and end;
- spot-check headings, lists, tables, and ordering;
- for PDFs, verify expected passages from different pages;
- report the selected backend, any fallback used, and the output path.

For large documents, write the full result to a file and inspect only representative sections.
