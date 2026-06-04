---
tags: [moc]
created: 2026-06-04
---

# MOC – Prompt Engineering & RAG

Designing effective prompts and grounding Claude in retrieved knowledge — the two primary levers for improving output quality.

## Writing Prompts

[[Prompt Engineering]] — Core strategies (be clear and direct, be specific, provide examples with ideal outputs) and the full evaluation cycle: Draft → Create Eval Dataset → Feed Through Claude → Grade → Iterate. Covers Code, Model, and Human graders.

[[Script Generation Prompts by Genre]] — Concrete prompt templates mapped to video genres (Entertainment, Educational, Comedy, Personal vlog, Reviews, Storytelling) — useful as a pattern reference.

## System-Level Prompting

[[System prompt]] — Role and persona definition at the API level. *(Primary cluster: [[MOC – Claude API]])*

## Retrieval-Augmented Generation

[[Search (RAG)]] — End-to-end RAG pipeline: Voyage AI embeddings → vector DB ingestion → hybrid search combining Semantic (embeddings) and Lexical (BM25) retrieval → Multiple Index fusion with RRF scoring. Also covers managed cloud alternatives (Cohere, OpenAI, Google Gemini).

---

*See also: [[MOC – Data & Inputs]] for file ingestion into RAG · [[MOC – Claude API]]*
