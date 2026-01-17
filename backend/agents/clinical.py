from langchain_core.messages import HumanMessage

def clinical_agent(state, llm):
    prompt = f"""
    You are a clinical discharge reviewer.

    Patient summary:
    {state['patient_summary']}

    Answer true or false and give a short reason.
    """

    response = llm.invoke([HumanMessage(content=prompt)]).content

    clinical_ready = "true" in response.lower()
    state["clinical_ready"] = clinical_ready
    state["explanation"] += f"\n[Clinical Review] {response}"

    state["timeline"].append({
        "step": "Clinical Review",
        "status": "Completed" if clinical_ready else "Blocked",
        "note": response
    })

    return state
