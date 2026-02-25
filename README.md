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

Distill is an AI-powered research assistant that lets you load multiple sources and have a conversation with them. Paste a URL, upload a document, or drop a YouTube link — then ask questions and get answers grounded in your content.

Here's the [link](https://kishensjain-distill-ai-research-assistant.hf.space/) to it

---

## Features

- 🌐 **URL ingestion** — paste any webpage URL and chat with its content
- 📄 **PDF & Word support** — upload `.pdf` and `.docx` files directly
- 🎥 **YouTube transcripts** — paste a YouTube link and chat with the video(powered by Supadata API)
- 🧠 **Smart chunking** — content is split into chunks and only the most relevant ones are sent to the model
- ⚡ **Streaming responses** — answers stream in real time
- 📝 **Auto summary** — sources are automatically summarised when loaded
- 💬 **Multi-turn memory** — the assistant remembers your conversation
- 🖥️ **Gradio web UI** — clean browser-based interface

---

## Tech Stack

- [Gradio](https://gradio.app) — web UI
- [OpenAI-compatible client](https://github.com/openai/openai-python) — LLM calls
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — web scraping
- [pypdf](https://pypdf.readthedocs.io/) — PDF extraction
- [python-docx](https://python-docx.readthedocs.io/) — Word doc extraction
- [supadata](https://api.supadata.ai/v1/youtube/transcript) — YouTube transcripts
- [uv](https://github.com/astral-sh/uv) — package management

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/distill-AI-research-assistant.git
cd distill-AI-research-assistant
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up your API key

Create a `.env` file in the root:

```
OLLAMA_API_KEY=your_key_here
SUPADATA_API_KEY=your_key_here
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