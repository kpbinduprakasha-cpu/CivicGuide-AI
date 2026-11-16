import os
import re
from pypdf import PdfReader

def extract_text_from_file(file_path):
    """Extract clean text from PDF, TXT or Markdown files."""
    if not os.path.exists(file_path):
        return ""
    
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.pdf':
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
    else: # txt, md, etc.
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, chunk_size=400, overlap=50):
    """Split text into overlapping word chunks for vector retrieval."""
    if not text:
        return []
    
    words = text.split()
    if len(words) <= chunk_size:
        return [" ".join(words)]
    
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        if len(chunk.strip()) > 30: # Only meaningful chunks
            chunks.append(chunk)
        if end >= len(words):
            break
        start += (chunk_size - overlap)
        
    return chunks
