from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    raw_input: str
    extracted_text: Optional[str]
    input_type: Optional[str]
    file_path: Optional[str]
    intent: Optional[str]
    constraints: Dict[str, Any]
    ambiguity: bool
    result: Optional[str]
    logs: List[str]
    ocr_confidence: Optional[float]
    duration: Optional[float]  # For audio files