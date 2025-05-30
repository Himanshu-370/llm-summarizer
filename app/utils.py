import fitz 
from docx import Document as DocxDocument
import httpx
import os

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

async def summarize_text(text: str) -> str:
    api_url = os.getenv("SUMMARIZATION_API_URL")
    headers = {
        "Authorization": f"Bearer {os.getenv('SUMMARIZATION_API_KEY')}"
    }
    payload = {
        "inputs": text[:2000] 
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=payload)
        result = response.json()
        print("API result:", result)

        # Defensive handling
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        elif isinstance(result, dict) and "error" in result:
            return f"Error: {result['error']}"
        else:
            return "No summary generated."