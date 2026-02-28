---
title: Distill AI Research Assistant
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "6.6.0"
app_file: main.py
pinned: false
---

# Distill 🔍

> Chat with anything. URLs, PDFs, Word docs, and YouTube videos — all in one place.

Distill is a lightweight **semantic RAG (Retrieval-Augmented Generation)** research assistant that lets you load multiple sources and have grounded conversations with them.

Paste a webpage url, upload a document, or drop a YouTube link — then ask questions and get answers backed by your content.

🔗 **Live Demo:**  
https://kishensjain-distill-ai-research-assistant.hf.space/

---

## ✨ Features

- 🌐 **URL ingestion** — paste any webpage and chat with its content  
- 📄 **PDF & Word support** — upload `.pdf` and `.docx` files  
- 🎥 **YouTube transcripts** — paste a link and chat with the video (via Supadata API)  
- 🔎 **Semantic search** — retrieval powered by vector embeddings (not keyword matching)  
- 🧠 **Smart chunking** — content split into overlapping chunks (~1000 chars)  
- ⚡ **Streaming responses** — real-time answer generation  
- 📝 **Auto summarization** — sources summarized when loaded  
- 💬 **Multi-turn memory** — conversation history preserved  
- 🖥️ **Gradio web UI** — clean browser-based interface

---

## 🏗 Architecture

Distill implements semantic RAG from scratch — without any external RAG framework.

**Pipeline:**

1. **Ingest** — Fetch and clean content from URLs, PDFs, Word docs, or YouTube transcripts  
2. **Chunk** — Split content into overlapping text chunks  
3. **Embed** — Convert chunks into vector embeddings using `gemini-embedding-001`  
4. **Retrieve** — Compute cosine similarity between query and stored embeddings  
5. **Generate** — Send top-K relevant chunks + conversation history to the LLM  
6. **Stream** — Return the response in real time  

---

## Tech Stack

- **Gradio** — Web UI  
- **Gemini API** — Embeddings (`gemini-embedding-001`)  
- **Ollama Cloud** — LLM generation (OpenAI-compatible client)  
- **NumPy** — Cosine similarity computation  
- **BeautifulSoup4** — Web scraping  
- **pypdf** — PDF extraction  
- **python-docx** — Word document extraction  
- **Supadata API** — YouTube transcripts  
- **uv** — Package management  

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/distill-AI-research-assistant.git
cd distill-AI-research-assistant
```

### 2. Install dependencies(make sure you have uv installed)

```bash
uv sync
```

### 3. Set up your API key

Create a `.env` file in the root:

```
OLLAMA_API_KEY=your_key_here
SUPADATA_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

Or if using a different provider, update the client in `src/ui.py` accordingly.

### 4. Run the app

```bash
uv run main.py
```


---

## Project Structure

```
distill/
├── main.py          # Entry point
├── src/
    |── cosine_similarity.py # Cosine similarity
│   ├── ingestion.py # URL, file, and YouTube loading
│   ├── chunker.py   # Text splitting and relevance scoring
│   └── ui.py        # Gradio interface and LLM chat logic
├── .env             # API keys (not committed)
├── pyproject.toml
└── README.md
```

---

## How It Works

1. **Ingest** — content is fetched and cleaned from your sources
2. **Chunk** — content is split into overlapping chunks of ~1000 characters
3. **Retrieve** — when you ask a question, the most relevant chunks are selected using keyword matching
4. **Generate** — selected chunks are sent to the LLM along with your question and conversation history
5. **Stream** — the response streams back in real time

This is a lightweight implementation of **RAG (Retrieval-Augmented Generation)** built from scratch without any RAG framework.

---

## License

MIT