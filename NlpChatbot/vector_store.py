import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st
import re

@st.cache_resource(show_spinner=True)
def load_embedding_model():
    with st.spinner("🔄 Loading embedding model..."):
        return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

def split_into_chunks(text, chunk_size=800):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[.*?\]", "", text)
    words = text.split()
    if len(words) <= chunk_size:
        return [' '.join(words)]
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def create_faiss_index(text):
    try:
        if isinstance(text, list):
            text = " ".join(str(item) for item in text)
        chunks = split_into_chunks(text)
        if not chunks:
            st.error("⚠️ No content found to split.")
            return [], None
        embeddings = embedding_model.encode(chunks, convert_to_numpy=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return chunks, index
    except Exception as e:
        st.error(f"❌ FAISS index creation failed: {e}")
        return [], None

def search_faiss_index(query, index, chunks, top_k=5):
    try:
        if index is None or not chunks:
            return []
        query_embedding = embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = index.search(query_embedding, top_k)
        scored_chunks = [(chunks[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
        sorted_chunks = sorted(scored_chunks, key=lambda x: x[1])
        return [chunk for chunk, _ in sorted_chunks]
    except Exception as e:
        st.error(f"❌ Search failed: {e}")
        return []
