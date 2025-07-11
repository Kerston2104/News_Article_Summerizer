import streamlit as st
from txtai.pipeline import Summary, Textractor
from PyPDF2 import PdfReader
import nltk
from textblob import TextBlob
from newspaper import Article

st.set_page_config(layout="wide")

@st.cache_resource
def text_summary(text, maxlength=None):
    summary = Summary()
    text = (text)
    result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text



choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document","URL to Summarize"])

if choice == "Summarize Text":
    st.subheader("Summarize Text using txtai")
    input_text = st.text_area("Enter your text here")
    if input_text is not None:
        if st.button("Summarize Text"):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summary Result**")
                result = text_summary(input_text)
                st.success(result)

elif choice == "Summarize Document":
    st.subheader("Summarize Document using txtai")
    input_file = st.file_uploader("Upload your document here", type=['pdf'])
    if input_file is not None:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())
            col1, col2 = st.columns([1,1])
            with col1:
                st.info("File uploaded successfully")
                extracted_text = extract_text_from_pdf("doc_file.pdf")
                st.markdown("**Extracted Text is Below:**")
                st.info(extracted_text)
            with col2:
                st.markdown("**Summary Result**")
                text = extract_text_from_pdf("doc_file.pdf")
                doc_summary = text_summary(text)
                st.success(doc_summary)
              
def author():
    return "KERSTON ANTO SINGH A";
                
elif choice == "URL to Summarize":
    nltk.download('punkt')
    st.subheader("Summarize Text using txtai")
    url = st.text_area('Enter you URL here', height=1)

    if st.button('Summarize'):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        st.markdown(f'**Title:** {article.title}')
        st.markdown(f'**Author:** {article.authors}')
        st.markdown(f'**Publishing Date:** {article.publish_date}')
        st.markdown(f'**Summary:** {article.summary}')

        analysis = TextBlob(article.text)
        sentiment_text = f'Polarity: {analysis.polarity}, \nSentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}'
        st.markdown(f'**Sentiment Analysis:** {sentiment_text}')
