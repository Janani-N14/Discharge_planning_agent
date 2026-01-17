from langgraph.graph import StateGraph
from backend.state import DischargeState
from backend.llm import get_llm
from backend.agents.clinical import clinical_agent
from backend.agents.risk import risk_agent
from backend.agents.coordination import coordination_agent
from backend.agents.safety import safety_agent

llm = get_llm()

def build_graph():
    graph = StateGraph(DischargeState)

    graph.add_node("clinical", lambda s: clinical_agent(s, llm))
    graph.add_node("risk", lambda s: risk_agent(s, llm))
    graph.add_node("coordination", lambda s: coordination_agent(s, llm))
    graph.add_node("safety", lambda s: safety_agent(s, llm))

    graph.set_entry_point("clinical")
    graph.add_edge("clinical", "risk")
    graph.add_edge("risk", "coordination")
    graph.add_edge("coordination", "safety")
    graph.set_finish_point("safety")

    return graph.compile()
