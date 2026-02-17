import PyPDF2

import PyPDF2
import io

def extract_text_from_pdf(file_bytes):

    pdf_stream = io.BytesIO(file_bytes)

    reader = PyPDF2.PdfReader(pdf_stream)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text
