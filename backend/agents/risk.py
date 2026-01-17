from backend.models.readmission import predict_readmission

def risk_agent(state, llm):
    feature_vector = {
        "time_in_hospital": 5,
        "num_lab_procedures": 40,
        "num_procedures": 1,
        "num_medications": len(state["medications"]),
        "number_outpatient": 0,
        "number_emergency": 1,
        "number_inpatient": 1,
        "number_diagnoses": len(state["diagnoses"]),
        "change": 1,
        "diabetesMed": 1,
    }

    score = predict_readmission(feature_vector)

    state["risk_score"] = score
    state["explanation"] += (
        f"\n[ML Readmission Model] Predicted 30-day readmission risk = {score:.2f}"
    )

    state["timeline"].append({
        "step": "Readmission Risk Assessment",
        "status": "Completed",
        "note": f"ML-predicted risk = {score:.2f}"
    })

    return state
