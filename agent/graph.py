from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.planner import plan
from agent.executor import execute

def followup(state):
    extracted = state.get("extracted_text", "")
    raw = state.get("raw_input", "")
    
    if extracted and not raw:
        question = "I've extracted the text. What would you like me to do with it? (summarize, analyze sentiment, explain if it's code, etc.)"
    elif "code" in extracted.lower() or "def " in extracted or "function" in extracted.lower():
        question = "I see this looks like code. Would you like me to explain it or check for bugs?"
    else:
        question = "Could you clarify what you'd like me to do? (summarize, sentiment analysis, explain, etc.)"
    
    return {
        **state,
        "result": f"**Clarification Needed:**\n\n{question}",
        "logs": state["logs"] + ["Follow-up question asked"]
    }


def create_agent():
    graph = StateGraph(AgentState)
    
    graph.add_node("plan", plan)
    graph.add_node("execute", execute)
    graph.add_node("followup", followup)
    
    graph.set_entry_point("plan")
    
    def route_after_plan(state):
        if state.get("ambiguity"):
            return "followup"
        return "execute"
    
    graph.add_conditional_edges(
        "plan",
        route_after_plan,
        {
            "followup": "followup",
            "execute": "execute"
        }
    )
    
    graph.add_edge("execute", END)
    graph.add_edge("followup", END)
    
    return graph.compile()


agent = create_agent()