import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner=True)
def load_qa_pipeline():
    with st.spinner("🔄 Loading QA model..."):
        return pipeline("question-answering", model="deepset/roberta-base-squad2")

qa_pipeline = load_qa_pipeline()

def answer_question(question, context_chunks, max_context_length=2000):
    if not question.strip():
        return "⚠️ Missing question."
    if not context_chunks:
        return "⚠️ No relevant content found."

    combined_context = " ".join(chunk.strip() for chunk in context_chunks if chunk and chunk.strip())
    if len(combined_context) > max_context_length:
        combined_context = combined_context[:max_context_length]

    if not combined_context.strip():
        return "⚠️ Context is empty after combining chunks."

    try:
        st.text_area("🧠 Context Passed to Model", combined_context[:1000], height=200)
        result = qa_pipeline(question=question, context=combined_context.strip())
        return result.get("answer", "🤔 No answer found.")
    except Exception as e:
        st.exception(e)
        return "⚠️ QA engine failed due to an exception."
