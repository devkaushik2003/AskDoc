
import streamlit as st
import pdfplumber
import google.generativeai as genai

# 🔑 Paste your Gemini API Key here
genai.configure(api_key="#####")

model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="Gemini Chat with PDF", layout="wide")
st.title("💬 Gemini 2.0 Flash Chat with PDF Context")

# ⬅️ Sidebar: Upload a PDF
with st.sidebar:
    st.header("📄 Upload PDF for Context")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    pdf_text = ""
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    pdf_text += page_text + "\n"
        st.success("✅ Text extracted from PDF.")

# 💬 Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 💬 Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the PDF or anything else..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Gemini call with context from PDF if available
    full_prompt = f"Use the following context from the PDF to answer the question.\n\nContext:\n{pdf_text[:12000]}\n\nQuestion:\n{prompt}" if pdf_text else prompt

    with st.chat_message("assistant"):
        full_response = ""
        response = model.generate_content(full_prompt, stream=True)
        response_container = st.empty()
        for chunk in response:
            full_response += chunk.text
            response_container.markdown(full_response + "▌")
        response_container.markdown(full_response)
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
