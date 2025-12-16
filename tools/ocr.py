import easyocr
import logging

logger = logging.getLogger(__name__)

reader = easyocr.Reader(['en'], gpu=False)

def ocr_image(image_path: str) -> tuple[str, float]:
    """
    Text from image using EasyOCR
    
    Args:
        image_path: Path to image file
        
    Returns:
        tuple: (extracted_text, confidence_score)
    """
    try:
        results = reader.readtext(image_path, detail=1)
        
        if not results:
            return "", 0.0
        
        text_parts = [result[1] for result in results]
        confidences = [result[2] for result in results]
        
        combined_text = " ".join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        logger.info(f"OCR extracted {len(text_parts)} text blocks with avg confidence {avg_confidence:.2f}")
        
        return combined_text.strip(), avg_confidence
        
    except Exception as e:
        logger.error(f"OCR error: {str(e)}")
        return "", 0.0