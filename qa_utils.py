import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class QAEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.doc_chunks = []
        self.embeddings = None
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

    def build_index(self, text, chunk_size=500):
        self.doc_chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
        if self.doc_chunks:
            self.embeddings = self.vectorizer.fit_transform(self.doc_chunks)
        else:
            self.embeddings = None

    def query(self, question, top_k=3):
        # Use Groq model if API key exists
        if self.client:
            context = "\n".join(self.doc_chunks[:5])  # take first few chunks as context
            prompt = f"""You are an exam assistant.
Context:
{context}

Question:
{question}

Please answer based purely on the document context."""
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        # Fallback to local TF-IDF if no API key
        if self.embeddings is None or len(self.doc_chunks) == 0:
            return "No document loaded. Please upload a PDF first."

        q_vec = self.vectorizer.transform([question])
        sims = cosine_similarity(q_vec, self.embeddings).flatten()
        idx = np.argmax(sims)
        return self.doc_chunks[idx]
