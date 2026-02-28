import gradio as gr
import os
from openai import OpenAI, APIConnectionError
from dotenv import load_dotenv
from src.chunker import retrieve_relevant_chunks, chunk_text, get_embedding
from src.ingestion import load_text, load_file

load_dotenv()

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.getenv("OLLAMA_API_KEY")
)

MODEL = "gpt-oss:120b"

def build_system_prompt(relevant_content: str) -> str:
    return f"""You are a helpful research assistant.
Answer the user's question based on the following relevant excerpts from their research material.
If the answer isn't present, say so honestly.

--- CONTENT START ---
{relevant_content}
--- CONTENT END ---"""


def load_sources(sources_text: str, files):
    sources = [s.strip()
               for s in sources_text.strip().splitlines() if s.strip()]

    all_content = []
    log = []

    for source in sources:
        try:
            content = load_text(source)
            all_content.append(content)
            log.append(
                f"✅ Loaded {len(content)} characters from: {source[:60]}")
        except Exception as e:
            log.append(f"❌ Failed: {source[:60]} — {e}")

    if files:
        for file in files:
            try:
                content = load_file(file.name)
                all_content.append(content)
                log.append(
                    f"✅ Loaded {len(content)} characters from: {file.name.split('/')[-1]}")
            except Exception as e:
                log.append(f"❌ Failed to load file: {e}")

    if not all_content:
        return "No sources provided.", [], "No sources loaded."

    combined = "\n\n---\n\n".join(all_content)
    chunks = chunk_text(combined)
    chunk_embeddings =[]

    for chunk in chunks:
        emb = get_embedding(chunk)
        chunk_embeddings.append(emb)

    log.append(
        f"\n📦 Total: {len(combined)} characters split into {len(chunks)} chunks.")

    # Auto summary
    preview = combined[:6000]
    summary_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Summarize the following content in 5-6 sentences so the user knows what they are working with."},
            {"role": "user", "content": preview}
        ]
    )
    summary = summary_response.choices[0].message.content

    return "\n".join(log), (chunks, chunk_embeddings), summary


def respond(user_message: str, history: list, chunk_data: tuple):
    if not chunk_data:
        history.append({"role": "user", "content": user_message})
        history.append(
            {"role": "assistant", "content": "⚠️ Please load some sources first."})
        yield history
        return
    
    chunks, chunk_embeddings = chunk_data
    
    relevant_content = retrieve_relevant_chunks(user_message, chunks, chunk_embeddings)

    messages = [
        {"role": "system", "content": build_system_prompt(relevant_content)},
        *history,
        {"role": "user", "content": user_message}
    ]

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ""})

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            history[-1]["content"] += delta
            yield history

    except APIConnectionError:
        history[-1]["content"] = "❌ Could not connect to Ollama. Run: ollama serve"
        yield history
    except Exception as e:
        history[-1]["content"] = f"❌ Unexpected error: {e}"
        yield history


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Distill - AI Research Assistant") as demo:
        gr.Markdown(
            "# 🔍 Distill - AI Research Assistant by Kishen\nLoad URLs, PDFs, Word docs, or YouTube videos — then ask questions about them.")

        chunks_state = gr.State([])

        with gr.Row():
            with gr.Column(scale=1):
                sources_input = gr.Textbox(
                    label="Sources",
                    placeholder="Enter one URL or text block per line...",
                    lines=5
                )
                file_input = gr.File(
                    label="Or upload PDF / Word files",
                    file_types=[".pdf", ".docx"],
                    file_count="multiple",
                )
                load_btn = gr.Button("Load Sources", variant="primary")
                load_output = gr.Textbox(
                    label="Load Status", lines=5, interactive=False)
                summary_output = gr.Textbox(
                    label="📝 Auto Summary",
                    lines=5,
                    interactive=False
                )

            with gr.Column(scale=3):
                chatbot = gr.Chatbot(label="Chat", height=480)
                user_input = gr.Textbox(
                    label="Your question",
                    placeholder="Ask something about your sources...",
                )
                send_btn = gr.Button("Send", variant="primary")

            load_btn.click(
                fn=load_sources,
                inputs=[sources_input, file_input],
                outputs=[load_output, chunks_state, summary_output]
            )

            send_btn.click(
                fn=respond,
                inputs=[user_input, chatbot, chunks_state],
                outputs=[chatbot]
            ).then(lambda: "", outputs=[user_input])

            user_input.submit(
                fn=respond,
                inputs=[user_input, chatbot, chunks_state],
                outputs=[chatbot]
            ).then(lambda: "", outputs=[user_input])

    return demo
