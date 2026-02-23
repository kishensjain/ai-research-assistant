import requests
from bs4 import BeautifulSoup
import re
import os
from pypdf import PdfReader
from docx import Document

def fetch_url(url: str) -> str:
    """Fetch a URL and return clean text content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchAssistant/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    clean_text = "\n".join(line for line in lines if line)

    return clean_text


def extract_youtube(url: str) -> str:
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if not match:
        raise ValueError("Could not extract video ID from URL")

    video_id = match.group(1)

    response = requests.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        params={"videoId": video_id, "text": True},
        headers={"x-api-key": os.getenv("SUPADATA_API_KEY")}
    )

    if response.status_code != 200:
        raise ValueError(f"Could not fetch transcript: {response.text}")

    data = response.json()
    content = data.get("content", "")
    if isinstance(content, list):
        return " ".join([item.get("text", "") for item in content])
    return content

def extract_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def extract_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()


def load_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)
    else:
        return open(file_path, "r").read()


def load_text(source: str) -> str:
    """Accept a URL, YouTube link, or raw pasted text."""
    if "youtube.com/watch" in source or "youtu.be/" in source:
        print("Fetching YouTube transcript...")
        return extract_youtube(source)
    elif source.startswith("http://") or source.startswith("https://"):
        print("Fetching URL...")
        return fetch_url(source)
    else:
        return source