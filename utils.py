import PyPDF2
import io
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_bytes):
    logger.info("Starting PDF text extraction")
    
    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_stream)
        
        text = ""
        page_count = len(reader.pages)
        logger.info(f"Processing PDF with {page_count} pages")
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                logger.warning(f"Page {i+1} returned no text")
        
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        return text
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}", exc_info=True)
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
