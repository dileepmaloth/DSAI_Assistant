from langchain_openai import ChatOpenAI
import json
import logging
import re

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    openai_api_key="********************************************************************ADD YOURS*****************************************************************",
    model="amazon/nova-2-lite-v1:free",
    temperature=0.7
)


def plan(state):
    """
    Returns updated state with intent and ambiguity flag
    """
    raw_input = state.get("raw_input", "")
    extracted_text = state.get("extracted_text")
    input_type = state.get("input_type", "text")
    
    context = f"Input Type: {input_type}\n"
    if extracted_text:
        context += f"Extracted Content: {extracted_text[:500]}...\n"
    context += f"User Input: {raw_input}\n"
    
    prompt = f"""You are a planner agent that determines user intent.

Context:
{context}

Available Tasks:
1. youtube_transcript - Fetch YouTube video transcript
2. summarization - Provide 1-line, 3 bullets, and 5-sentence summary
3. sentiment - Analyze sentiment with label, confidence, justification
4. code_explanation - Explain code, detect bugs, mention complexity
5. audio_summary - Transcribe and summarize audio
6. text_extraction - Just extract and return text from image/PDF
7. conversational - Answer general questions

Rules:
- If user's goal is UNCLEAR or multiple tasks are equally valid, return "AMBIGUOUS"
- YouTube URLs should always be "youtube_transcript"
- If user asks "what should I do?" or doesn't specify action, return "AMBIGUOUS"
- Be strict: only return a task if you're confident about the user's intent

Return ONLY valid JSON:
{{
  "intent": "task_name or AMBIGUOUS",
  "constraints": {{"key": "value"}}
}}"""

    try:
        response = llm.invoke(prompt).content
        
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
        else:
            data = {"intent": "AMBIGUOUS", "constraints": {}}
        
        if data.get("intent") == "AMBIGUOUS":
            logger.info("Planner: Intent is ambiguous")
            return {
                **state,
                "ambiguity": True,
                "logs": state["logs"] + ["Planner: intent ambiguous - need clarification"]
            }
        
        logger.info(f"Planner: Identified intent as {data['intent']}")
        return {
            **state,
            "intent": data["intent"],
            "constraints": data.get("constraints", {}),
            "ambiguity": False,
            "logs": state["logs"] + [f"Planner chose intent: {data['intent']}"]
        }
        
    except Exception as e:
        logger.error(f"Planner error: {str(e)}")
        return {
            **state,
            "ambiguity": True,
            "logs": state["logs"] + [f"Planner error: {str(e)}"]
        }