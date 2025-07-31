import streamlit as st

# ✅ MUST BE FIRST Streamlit command
st.set_page_config(page_title="NLP Chatbot", layout="centered")

# ✅ Now it's safe to import modules
from file_handler import extract_text_from_file
from scraper import scrape_text_from_url
from vector_store import create_faiss_index, search_faiss_index
from qa_engine import answer_question

st.title("📚 NLP FAQ Chatbot (File & Web Support)")

if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

uploaded_file = st.file_uploader("📄 Upload a PDF or TXT file", type=["pdf", "txt"])
url_input = st.text_input("🌐 Or enter a web URL to scrape content")

if st.button("Process Document"):
    text = ""
    if uploaded_file:
        text = extract_text_from_file(uploaded_file)
    elif url_input:
        text = scrape_text_from_url(url_input)
        st.text_area("🔍 Scraped Content Preview", text[:2000], height=250)
    else:
        st.warning("⚠️ Please upload a file or enter a URL.")

    if text:
        st.session_state.raw_text = text
        st.session_state.chunks, st.session_state.faiss_index = create_faiss_index(text)
        st.success("✅ Document processed and indexed successfully!")
        st.text_area("🔍 Preview Extracted Content", text[:2000], height=250)
    else:
        st.error("❌ Failed to extract text from input.")

if st.session_state.faiss_index:
    question = st.text_input("💬 Ask a question based on the content")
    if question:
        relevant_chunks = search_faiss_index(question, st.session_state.faiss_index, st.session_state.chunks)
        if not relevant_chunks:
            st.warning("⚠️ No relevant chunks found.")
        else:
            st.text_area("🧩 Chunks Retrieved", "\n\n---\n\n".join(relevant_chunks[:3]), height=200)
        answer = answer_question(question, relevant_chunks)
        st.markdown(f"**Answer:** {answer}")
