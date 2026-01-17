import json
from langchain_core.messages import HumanMessage, SystemMessage
from backend.llm import get_llm   

llm = get_llm()

SYSTEM_PROMPT = """
You are a healthcare intake assistant.

Extract structured discharge planning information.

Return ONLY valid JSON:

{
  "intent": "discharge_planning" | "other",
  "patient_summary": "",
  "diagnoses": [],
  "medications": [],
  "social_factors": ""
}

Leave fields empty if missing.
"""

def extract_intent_and_slots(conversation: str) -> dict:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=conversation),
    ]

    response = llm.invoke(messages).content

    try:
        return json.loads(response)
    except Exception:
        return {
            "intent": "other",
            "patient_summary": "",
            "diagnoses": [],
            "medications": [],
            "social_factors": ""
        }
