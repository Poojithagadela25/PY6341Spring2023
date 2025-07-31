import PyPDF2
import fitz  # PyMuPDF

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_type == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        return ""

def extract_text_from_txt(uploaded_file):
    try:
        content = uploaded_file.read()
        return content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[TXT ERROR] {e}")
        return ""

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        uploaded_file.seek(0)
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                content = page.get_text()
                if content:
                    text += content
    except Exception as e:
        print(f"[PyMuPDF failed] {e}")

    if text.strip():
        return text

    try:
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    except Exception as e:
        print(f"[PyPDF2 failed] {e}")
    return text
