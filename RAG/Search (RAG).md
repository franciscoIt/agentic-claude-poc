---
tags: []
created: 2026-06-02
---

# Search (RAG)

voyageAI is the claude partner.

## The Ingestion Phase (Voyage AI's First Role)

Before Claude can read your documents, your documents need to be made searchable.

- **The Problem:** Computers search by comparing numbers, not words.

- **Voyage AI's Part:** You pass your raw text (PDFs, wikis, code) through **Voyage AI's embedding models** (like `voyage-large-2` or `voyage-code-2`). Voyage AI translates your text into high-quality mathematical vectors (embeddings) that capture the semantic meaning of the text.

- These vectors are then stored in a Vector Database (like Pinecone, Milvus, or pgvector).

## Managed Cloud APIs (Drop-in Replacements)

If you want a managed service where you just send text to an API and get vectors or rank scores back, these are the top contenders:

- **Cohere (Embed v4 & Rerank 4 Pro):** The most direct alternative to Voyage. Cohere dominates **multilingual retrieval** (supporting 100+ languages) and native compression (int8/binary quantization). Its **Rerank 4 Pro** model is highly optimized for semi-structured data like JSON, CRM records, and tables.

- **OpenAI (text-embedding-3-large):** The standard "safest default." It features **Matryoshka dim reduction**, allowing you to cut vector sizes significantly to save database costs. However, OpenAI does _not_ offer a dedicated reranking endpoint, so you'd have to pair it with another provider.

- **Google Gemini (Gemini Embedding 2):** A powerful choice if you are handling **multimodal RAG** (text, image, audio, video, and PDFs combined). It boasts superb long-context retrieval but requires Vertex AI or Google AI Studio integration.

## Then

**Claude's Part:** The RAG system takes the top-ranked text chunks provided by Voyage AI and sends them to Claude (e.g., Claude 3.5 Sonnet) alongside the user's original prompt.

Claude reads the provided context, applies its advanced reasoning, and generates a fluent, accurate, and helpful answer for the user based _only_ on those retrieved documents.

## BM25 Lexical Search

Algorithms are applied to fine tune rags. IMplemeneted manually.

![[Pasted image 20260602110011.png]]

![[Pasted image 20260602110335.png]]

## Multiple Index

![[Pasted image 20260602111626.png]]
