---
name: markdown-converter
description: Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis.
---

# Markdown Converter

Convert files to Markdown using `uvx markitdown` — no installation required.

## Basic Usage

```bash
# Convert to stdout
uvx markitdown input.pdf

# Save to file
uvx markitdown input.pdf -o output.md
uvx markitdown input.docx > output.md

# From stdin
cat input.pdf | uvx markitdown
```

## Supported Formats

- **Documents**: PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls)
- **Web/Data**: HTML, CSV, JSON, XML
- **Media**: Images (EXIF + OCR), Audio (EXIF + transcription)
- **Other**: ZIP (iterates contents), YouTube URLs, EPub

## Offline vs External Service Dependencies

MarkItDown's core converters run **locally** and need no network. The following table distinguishes offline-capable conversions from those that call external services.

### ✅ Fully offline (local parsing only)

- **PDF** — local text/structure extraction
- **Word (.docx)** — local Office XML parsing
- **PowerPoint (.pptx)** — local Office XML parsing
- **Excel (.xlsx, .xls)** — local Office XML parsing
- **HTML / CSV / JSON / XML** — local text processing
- **ZIP** — local decompress + iterate
- **EPub** — local parsing
- **Images** — EXIF metadata only (no image content description)
- **Audio** — EXIF metadata only (no speech transcription)

### ❌ Requires external service

| Feature | Dependency | Notes |
|------|------|-------|
| LLM image descriptions | `llm_client` + `llm_model` (OpenAI-compatible API) | Generates text descriptions of image content. Can use a local LLM endpoint (e.g. vLLM) to stay offline. |
| OCR plugin (`markitdown-ocr`) | OpenAI-compatible vision model | Extracts text from images embedded in PDF/Office docs. Same local-LLM workaround possible. |
| Audio speech transcription | `audio-transcription` extra | Uses LLM-based transcription, not local Whisper. |
| YouTube transcription | `youtube-transcription` extra | Fetches subtitles from YouTube over the network. |
| Azure Document Intelligence | Azure cloud endpoint (`-d -e`) | Cloud layout extraction + OCR. |
| Azure Content Understanding | Azure cloud endpoint (`--use-cu`) | Cloud multimodal extraction, structured fields. |

### ⚠️ Permission gate for external services

**Before invoking any conversion that calls an external service (LLM API, Azure, YouTube, or any network endpoint), you MUST obtain explicit user permission first.**

This includes:
- Passing `llm_client` / `llm_model` for image descriptions
- Enabling the OCR plugin (`--use-plugins` with `markitdown-ocr`)
- Using `-d` (Azure Document Intelligence) or `--use-cu` (Azure Content Understanding)
- Converting YouTube URLs (network fetch)
- Audio transcription with `audio-transcription` extra

Default to offline-only conversions unless the user explicitly asks for a feature that requires external services. When in doubt, ask.

## Options

```bash
-o OUTPUT      # Output file
-x EXTENSION   # Hint file extension (for stdin)
-m MIME_TYPE   # Hint MIME type
-c CHARSET     # Hint charset (e.g., UTF-8)
-d             # Use Azure Document Intelligence
-e ENDPOINT    # Document Intelligence endpoint
--use-plugins  # Enable 3rd-party plugins
--list-plugins # Show installed plugins
```

## Examples

```bash
# Convert Word document
uvx markitdown report.docx -o report.md

# Convert Excel spreadsheet
uvx markitdown data.xlsx > data.md

# Convert PowerPoint presentation
uvx markitdown slides.pptx -o slides.md

# Convert with file type hint (for stdin)
cat document | uvx markitdown -x .pdf > output.md

# Use Azure Document Intelligence for better PDF extraction
uvx markitdown scan.pdf -d -e "https://your-resource.cognitiveservices.azure.com/"
```

## Notes

- Output preserves document structure: headings, tables, lists, links
- First run caches dependencies; subsequent runs are faster
- For complex PDFs with poor extraction, use `-d` with Azure Document Intelligence
- **Offline default**: basic format conversions (PDF, Office, HTML, CSV/JSON/XML, ZIP, EPub, EXIF metadata) work without any network
- **External services are opt-in only**: LLM image descriptions, OCR, audio transcription, YouTube, and Azure integrations all require explicit user permission before use (see "Offline vs External Service Dependencies" above)

