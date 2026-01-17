from fastapi import FastAPI, HTTPException
from backend.graph import build_graph

app = FastAPI()
graph = build_graph()

@app.post("/analyze_discharge")
def analyze(patient: dict):
    try:
        state = {
            **patient,
            "clinical_ready": False,
            "risk_score": 0.0,
            "missing_tasks": [],
            "discharge_safe": False,
            "explanation": "",
            "timeline": []
        }

        return graph.invoke(state)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
