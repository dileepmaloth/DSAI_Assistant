from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from agent.graph import agent
from tools.ocr import ocr_image
from tools.pdf import extract_pdf
from tools.audio import transcribe_audio
import os
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DSAI_API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/run")
async def run_agent(
    text: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None)
):
    """
    Main endpoint for agent processing
    
    Accepts text and/or file uploads, processes them, and returns result
    """
    try:
        state = {
            "raw_input": text or "",
            "extracted_text": None,
            "input_type": "text",
            "file_path": None,
            "intent": None,
            "constraints": {},
            "ambiguity": False,
            "result": None,
            "logs": [],
            "ocr_confidence": None,
            "duration": None
        }
        
        if file:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            
            
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            state["file_path"] = file_path
            file_ext = os.path.splitext(file.filename)[1].lower()
            
            logger.info(f"Processing file: {file.filename}")
            
            
            if file_ext in ['.jpg', '.jpeg', '.png']:
                state["input_type"] = "image"
                extracted, confidence = ocr_image(file_path)
                state["extracted_text"] = extracted
                state["ocr_confidence"] = confidence
                state["logs"].append(f"OCR extracted text with {confidence:.2%} confidence")
                
            elif file_ext == '.pdf':
                state["input_type"] = "pdf"
                extracted, confidence = extract_pdf(file_path)
                state["extracted_text"] = extracted
                if confidence:
                    state["ocr_confidence"] = confidence
                    state["logs"].append(f"PDF processed with OCR (confidence: {confidence:.2%})")
                else:
                    state["logs"].append("PDF text extracted directly")
                    
            elif file_ext in ['.mp3', '.wav', '.m4a']:
                state["input_type"] = "audio"
                extracted, duration = transcribe_audio(file_path)
                state["extracted_text"] = extracted
                state["duration"] = duration
                state["logs"].append(f"Audio transcribed ({duration:.1f}s)")
                
            else:
                return {
                    "error": f"Unsupported file type: {file_ext}",
                    "logs": ["File type not supported"]
                }
            
         
            try:
                os.remove(file_path)
            except:
                pass
        
      
        logger.info("Running agent...")
        result_state = agent.invoke(state)
        
  
        response = {
            "input_type": result_state.get("input_type"),
            "extracted_text": result_state.get("extracted_text"),
            "intent": result_state.get("intent"),
            "result": result_state.get("result"),
            "logs": result_state.get("logs", []),
            "ocr_confidence": result_state.get("ocr_confidence"),
            "duration": result_state.get("duration")
        }
        
        return response
        
    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        return {
            "error": str(e),
            "logs": [f"Error: {str(e)}"]
        }

@app.get("/")
async def root():
    return {"message": "DSAI_API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}