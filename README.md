# NLP FAQ Chatbot (File & Web Support)

##  Project Purpose

This project is an NLP-powered chatbot that allows users to:
- Upload `.pdf` or `.txt` files
- Scrape content from web URLs
- Ask questions based on uploaded/scraped content

It leverages modern language models and FAISS indexing for fast, accurate retrieval of answers from user-provided documents.

---

##  How to Run the Code

###  Requirements
- Python 3.10+
- Recommended IDE: VS Code or Jupyter
- Tools used: Streamlit, FAISS, LangChain, PyMuPDF, BeautifulSoup

---

###  Setup Instructions

#### 1. Clone the Repository:
```bash
git clone https://github.com/YOUR_USERNAME/NlpChatbot.git
cd NlpChatbot
   

2. Create a Virtual Environment:
python -m venv venv

3. Activate the Virtual Environment:
venv\Scripts\activate


4. Install Dependencies:
pip install -r requirements.txt


5. Run the App:
streamlit run app.py
