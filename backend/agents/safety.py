def safety_agent(state, llm):
    safe = (
        state["clinical_ready"]
        and state["risk_score"] < 0.7
        and not state["missing_tasks"]
    )

    state["discharge_safe"] = safe
    verdict = "SAFE" if safe else "NOT SAFE"
    state["explanation"] += f"\n[Safety Verdict] {verdict}"

    state["timeline"].append({
        "step": "Final Safety Decision",
        "status": "Approved" if safe else "Not Approved",
        "note": verdict
    })

    return state
