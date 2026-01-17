import requests
from backend.chat.intent_extractor import extract_intent_and_slots

DISCHARGE_API = "http://127.0.0.1:8000/analyze_discharge"

def process_chat(user_message: str, memory):
    # ✅ Add user message
    memory.add_user_message(user_message)

    # ✅ Build conversation text
    conversation_text = "\n".join(
        msg.content for msg in memory.messages
    )

    extracted = extract_intent_and_slots(conversation_text)

    if extracted["intent"] != "discharge_planning":
        reply = (
            "I can help with your hospital discharge. "
            "Could you tell me why you were admitted?"
        )
        memory.add_ai_message(reply)
        return reply, None

    if not all([
        extracted["patient_summary"],
        extracted["diagnoses"],
        extracted["medications"],
        extracted["social_factors"],
    ]):
        reply = (
            "Thanks. I still need details about your diagnosis, "
            "medications, and home situation."
        )
        memory.add_ai_message(reply)
        return reply, None

    payload = {
        "patient_summary": extracted["patient_summary"],
        "diagnoses": extracted["diagnoses"],
        "medications": extracted["medications"],
        "social_factors": extracted["social_factors"],
    }

    result = requests.post(DISCHARGE_API, json=payload).json()

    reply = (
        f"Here’s what I found:\n\n"
        f"- Discharge safe: {result['discharge_safe']}\n"
        f"- Readmission risk: {result['risk_score']:.2f}\n\n"
        f"I’ll guide you through the next steps."
    )

    memory.add_ai_message(reply)

    return reply, result
