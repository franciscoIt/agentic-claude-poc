---
tags: [moc]
created: 2026-06-04
---

# MOC – Data & Inputs

How to send Claude different types of data beyond plain text — files, images, PDFs, and code execution contexts.

## Files

[[File API]] — Upload files to get a `file_id`, then reference them across requests. Entry point for all file-based workflows.

[[Code Execution with File Upload]] — Pass a `file_id` via the `container_upload` block so Claude can execute code against the file inside a Docker container and return analysis results.

## Images

[[Image handling]] — Include images in message content blocks. Covers supported formats, notice the mime type, and prompting strategies for visual inputs.

## Documents

[[pdf and Citations]] — Send PDFs directly in the API. Claude can return `CitationLocation` objects that point back to the exact source passages.

---

*See also: [[File API]] also feeds [[Search (RAG)]] for document ingestion · [[MOC – Claude API]]*
