from langchain_openai import ChatOpenAI
from tools.youtube import fetch_youtube_transcript
import logging

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    openai_api_key="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",
    model="amazon/nova-2-lite-v1:free",
    temperature=0.8
)


def summarize(text: str) -> str:
    """Generate 1-line, 3 bullets, and 5-sentence summary"""
    prompt = f"""Provide a summary in exactly this format:

**One-line Summary:**
[single sentence]

**Key Points:**
• [point 1]
• [point 2]
• [point 3]

**Detailed Summary:**
[exactly 5 sentences]

Text to summarize:
{text[:]}"""
    
    return llm.invoke(prompt).content

def sentiment_analysis(text: str) -> str:
    """Analyze sentiment with label, confidence, and justification"""
    prompt = f"""Analyze the sentiment of this text.

Return in this format:
**Sentiment Label:** [Positive/Negative/Neutral/Mixed]
**Confidence:** [percentage]%
**Justification:** [one clear sentence explaining why]

Text:
{text[:]}"""
    
    return llm.invoke(prompt).content

def explain_code(text: str) -> str:
    """Explain code, detect bugs, mention time complexity"""
    prompt = f"""Analyze this code and provide:

1. **What it does:** [clear explanation]
2. **Detected Issues:** [any bugs or problems, or "None detected"]
3. **Time Complexity:** [Big O notation with brief explanation]
4. **Space Complexity:** [Big O notation]

Code:
{text}"""
    
    return llm.invoke(prompt).content

def conversational(text: str) -> str:
    """Handle general conversational queries"""
    return llm.invoke(text).content

def execute(state):
    """
    Executor agent that performs the identified task
    
    Returns updated state with result
    """
    text = state.get("extracted_text") or state.get("raw_input", "")
    intent = state.get("intent")
    
    logger.info(f"Executor: Running task '{intent}'")
    
    try:
        if intent == "youtube_transcript":
            output = fetch_youtube_transcript(text)
            
        elif intent == "summarization":
            output = summarize(text)
            
        elif intent == "sentiment":
            output = sentiment_analysis(text)
            
        elif intent == "code_explanation":
            output = explain_code(text)
            
        elif intent == "audio_summary":
            duration = state.get("duration", 0)
            summary = summarize(text)
            output = f"**Audio Duration:** {duration:.1f} seconds\n\n{summary}"
            
        elif intent == "text_extraction":
            confidence = state.get("ocr_confidence")
            if confidence:
                output = f"**Extracted Text (OCR Confidence: {confidence:.2%}):**\n\n{text}"
            else:
                output = f"**Extracted Text:**\n\n{text}"
                
        else:
            # Default to conversational
            output = conversational(text)
        
        return {
            **state,
            "result": output,
            "logs": state["logs"] + [f"Executor: Completed task '{intent}'"]
        }
        
    except Exception as e:
        logger.error(f"Executor error: {str(e)}")
        return {
            **state,
            "result": f"Error executing task: {str(e)}",
            "logs": state["logs"] + [f"Executor error: {str(e)}"]
        }