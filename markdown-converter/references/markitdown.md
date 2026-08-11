# MarkItDown usage reference

Use MarkItDown for HTML, JSON/XML, ZIP archives, Outlook messages, image or audio metadata, and supported formats outside anydoc's scope. It can also serve as a fallback parser for text PDFs and modern office files.

## Local conversion

```python
from pathlib import Path
from markitdown import MarkItDown

source = Path("page.html")
converter = MarkItDown(enable_plugins=False)
result = converter.convert_local(source)
markdown = result.text_content
```

For local streams:

```python
with source.open("rb") as stream:
    result = converter.convert_stream(stream, file_extension=source.suffix)
```

Use `convert_local` or `convert_stream` for ordinary local-file work. Keep plugins disabled unless a specific plugin is needed and its behavior has been checked.

## External and optional features

MarkItDown can work with remote resources, YouTube, Azure services, model clients, OCR/transcription integrations, and third-party plugins. Before using a feature that may contact an external service:

1. identify the destination and purpose;
2. explain what content or metadata may be transmitted;
3. mention credentials and possible charges when relevant;
4. obtain explicit user consent for that operation.

Do not pass a remote URL to the general `convert()` API before obtaining consent. Configured credentials or a previous network operation do not imply consent for a new call.

## Plugins

Plugins may invoke a model, external service, executable, or remote resource. Inspect the selected plugin first. If external contact is possible, complete the consent steps before enabling it.

## Images and OCR

Without an image-description model, image handling primarily yields metadata. For semantic image description or OCR, use a known local model or local OCR workflow. A remote vision or OCR endpoint requires explicit consent.

## Audio and YouTube

Audio metadata can be processed locally. Transcription depends on the selected backend and available codecs or models. A remote transcription backend requires explicit consent.

YouTube subtitle or media retrieval always uses the network and requires explicit consent before access.

## Azure integrations

Azure Document Intelligence and Azure Content Understanding require endpoints, credentials, network access, and may incur charges. Explain what will be uploaded and obtain explicit consent before use.

## Selection summary

Choose MarkItDown for HTML, JSON, XML, ZIP, Outlook, media metadata, an understood plugin, an approved external integration, or fallback parsing. Choose firecrawl-anydoc first for office documents, OpenDocument, RTF, EPUB, CSV, and text-based PDFs.
