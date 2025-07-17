import streamlit as st
import fitz  # PyMuPDF
import docx
from io import BytesIO

st.set_page_config(page_title="Page Extractor",page_icon="✂️")

def extract_text_from_pdf(file, page_ranges):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    output = fitz.open()  # empty PDF

    for start, end in page_ranges:
        for i in range(start - 1, end):
            output.insert_pdf(doc, from_page=i, to_page=i)
    buffer = BytesIO()
    output.save(buffer)
    buffer.seek(0)
    return buffer

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text

def parse_ranges(ranges_str):
    ranges = []
    for part in ranges_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            num = int(part)
            ranges.append((num, num))
    return ranges

# Streamlit App UI
st.title("📄 PDF & DOCX Page Extractor")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
ranges_input = st.text_input("Enter page ranges (e.g. 1-5,8-10)")

if uploaded_file and ranges_input:
    page_ranges = parse_ranges(ranges_input)

    if uploaded_file.type == "application/pdf":
        result_pdf = extract_text_from_pdf(uploaded_file, page_ranges)
        st.success("✅ Pages Extracted Successfully!")
        st.download_button("📥 Download Extracted PDF", result_pdf, file_name="extracted_pages.pdf")
        
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        st.info("📃 DOCX detected - showing full content (page range feature not supported for Word files)")
        text = extract_text_from_docx(uploaded_file)
        st.text_area("DOCX Content", text, height=300)

