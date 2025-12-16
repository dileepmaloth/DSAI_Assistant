# Agentic Assistant

This is an agentic AI assistant built as part of an assignment.

## Tech Stack
- FastAPI
- LangGraph
- Streamlit

## Features
- Text, image, PDF, and audio input
- OCR and transcription
- Multi-step agent reasoning

## How to Run
1. Start backend:
uvicorn api.main:app --reload

2. Start frontend:
streamlit run ui/app.py 

## Demo Video
See the demo video in the repository.


## Project Structure

```
agentic_app/
├── agent/
│   ├── state.py          # State definition
│   ├── planner.py        # Intent detection
│   ├── executor.py       # Task execution
│   └── graph.py          # LangGraph workflow
├── tools/
│   ├── ocr.py           # Image OCR
│   ├── pdf.py           # PDF extraction
│   ├── audio.py         # Audio transcription
│   └── youtube.py       # YouTube transcripts
├── api/
│   └── main.py          # FastAPI endpoints
├── ui/
│   └── app.py           # Streamlit interface
├── requirements.txt
└── README.md
```

