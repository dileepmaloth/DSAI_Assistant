import fitz  
import logging
from tools.ocr import ocr_image
import os
from typing import Optional

logger = logging.getLogger(__name__)

def extract_pdf(pdf_path: str) -> tuple[str, Optional[float]]:
    """
    Extract text from PDF, with OCR fallback for scanned PDFs
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        tuple: (extracted_text, ocr_confidence or None)
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_parts.append(text)
        
        combined_text = "\n".join(text_parts).strip()
        
        if not combined_text or len(combined_text) < 50:
            logger.info("No text found, attempting OCR on PDF pages")
            
            page = doc[0]
            pix = page.get_pixmap(dpi=300)
            img_path = pdf_path.replace('.pdf', '_temp.png')
            pix.save(img_path)
            
            text, confidence = ocr_image(img_path)
            
            if os.path.exists(img_path):
                os.remove(img_path)
            
            doc.close()
            return text, confidence
        
        doc.close()
        logger.info(f"Extracted {len(combined_text)} characters from PDF")
        return combined_text, None
        
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        return "", None