def coordination_agent(state, llm):
    tasks = []

    if not state["clinical_ready"]:
        tasks.append("Stabilize patient clinically")

    if state["risk_score"] > 0.5:
        tasks.append("Schedule early follow-up")

    if "lives alone" in state["social_factors"].lower():
        tasks.append("Arrange home health services")

    state["missing_tasks"] = tasks
    state["explanation"] += f"\n[Care Coordination] {tasks or 'No pending tasks'}"

    state["timeline"].append({
        "step": "Care Coordination",
        "status": "Pending" if tasks else "Completed",
        "note": ", ".join(tasks) if tasks else "All tasks completed"
    })

    return state
