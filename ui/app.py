# ---------- PATH FIX (MUST BE FIRST) ----------
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))

sys.path.insert(0, PROJECT_ROOT)

# ---------- NOW SAFE TO IMPORT ----------
import streamlit as st
import requests
import json

from backend.chat.memory import get_memory
from backend.chat.orchestrator import process_chat

import streamlit as st
import requests
import json

from backend.chat.memory import get_memory
from backend.chat.orchestrator import process_chat


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Discharge Planning System",
    layout="wide"
)

st.title("🏥 AI Discharge Planning System")
st.caption(
    "Clinical decision support with conversational intake. "
    "Not a replacement for medical professionals."
)

# -------------------------------------------------
# Sidebar: Mode Selection
# -------------------------------------------------
st.sidebar.header("Navigation")

mode = st.sidebar.radio(
    "Select mode",
    ["💬 Patient Chatbot", "🧾 Discharge Dashboard"]
)

# -------------------------------------------------
# Shared session state
# -------------------------------------------------
if "memory" not in st.session_state:
    st.session_state.memory = get_memory()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_discharge_result" not in st.session_state:
    st.session_state.last_discharge_result = None

# =================================================
# MODE 1: PATIENT CHATBOT
# =================================================
if mode == "💬 Patient Chatbot":
    st.subheader("💬 Discharge Planning Assistant")

    user_input = st.chat_input(
        "Tell me about your hospital stay or discharge…"
    )

    if user_input:
        # Store user message
        st.session_state.chat_history.append(("user", user_input))

        # Process through orchestrator
        reply, discharge_result = process_chat(
            user_input,
            st.session_state.memory
        )

        # Store assistant reply
        st.session_state.chat_history.append(("assistant", reply))

        # Save discharge result if produced
        if discharge_result:
            st.session_state.last_discharge_result = discharge_result

    # Render chat messages
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    # Show discharge summary inline if available
    if st.session_state.last_discharge_result:
        st.divider()
        st.info("Discharge assessment completed. Switch to the dashboard to view details.")

# =================================================
# MODE 2: DISCHARGE DASHBOARD
# =================================================
else:
    st.subheader("🧾 Discharge Planning Dashboard")

    # -----------------------------
    # Manual JSON input (optional)
    # -----------------------------
    st.markdown("### Manual Discharge Input (Optional)")

    default_json = {
        "patient_summary": "65-year-old male admitted for heart failure exacerbation.",
        "diagnoses": ["CHF", "Hypertension"],
        "medications": ["Furosemide", "Lisinopril"],
        "social_factors": "Lives alone, limited mobility"
    }

    patient_json = st.text_area(
        "Patient JSON",
        value=json.dumps(default_json, indent=2),
        height=220
    )

    if st.button("Analyze Discharge"):
        response = requests.post(
            "http://127.0.0.1:8000/analyze_discharge",
            json=json.loads(patient_json)
        )

        if response.status_code == 200:
            st.session_state.last_discharge_result = response.json()
        else:
            st.error("Backend error")
            st.text(response.text)

    # -----------------------------
    # Show results (from chat OR manual)
    # -----------------------------
    if st.session_state.last_discharge_result:
        result = st.session_state.last_discharge_result

        st.divider()
        st.markdown("### Discharge Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Clinical Stability",
                "Yes" if result["clinical_ready"] else "No"
            )

        with col2:
            st.metric(
                "Readmission Risk",
                f"{result['risk_score']:.2f}"
            )

        with col3:
            st.metric(
                "Discharge Status",
                "SAFE" if result["discharge_safe"] else "NOT SAFE"
            )

        # -----------------------------
        # Timeline
        # -----------------------------
        st.subheader("📅 Discharge Timeline")

        for event in result.get("timeline", []):
            c1, c2, c3 = st.columns([3, 2, 7])

            with c1:
                st.write(f"**{event['step']}**")

            with c2:
                status = event["status"]
                if status in ["Completed", "Approved"]:
                    st.success(status)
                elif status == "Pending":
                    st.warning(status)
                else:
                    st.error(status)

            with c3:
                st.write(event["note"])

        # -----------------------------
        # Reasoning trace
        # -----------------------------
        st.subheader("🧠 AI Reasoning Trace")
        st.text_area(
            "",
            result["explanation"],
            height=200
        )

        # -----------------------------
        # Raw JSON
        # -----------------------------
        with st.expander("🔍 Raw Discharge Agent Output"):
            st.json(result)
    else:
        st.info("No discharge assessment available yet. Use the chatbot or manual input.")
