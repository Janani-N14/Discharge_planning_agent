
#  Discharge Planning Agent (Agentic AI + ML)

An **agentic AI system for hospital discharge planning** that combines:

- LLM-driven conversational intake
- Clinical reasoning via agent orchestration
- Machine-learning–based 30-day readmission risk prediction

This project demonstrates how **modern agent architectures** can assist clinicians and patients by providing **decision support**, not diagnosis.

---

##  Problem Statement

Hospital discharge planning is often:

-  Time-consuming  
-  Fragmented across systems  
-  Prone to missing social or medication-related risks  
-  A major contributor to avoidable readmissions  

Clinicians need **assistive intelligence**, not replacement.

This system acts as a **discharge planning assistant**, supporting clinical judgment with structured insights.

---

##  Project Objectives

- Build an **agentic discharge planning assistant**
- Enable **natural language patient conversations**
- Automatically extract **structured discharge information**
- Predict **30-day readmission risk**
- Provide **explainable, human-reviewable outputs**
- Maintain a **modular, production-ready architecture**

---

##  High-Level Architecture

```

User (Streamlit UI)
↓
Conversational Chatbot (LLM + Memory)
↓
Intent & Slot Extraction Agent
↓
Discharge Planning Agent (LangGraph)
↓
ML Readmission Risk Model
↓
Structured Discharge Assessment

````

---

##  Tech Stack

### Backend
- **FastAPI** – REST API
- **LangGraph** – Agent orchestration
- **LangChain Core (v0.2+)** – LLM abstractions
- **Groq LLM** – Reasoning & information extraction
- **Scikit-learn** – Readmission risk model

### Frontend
- **Streamlit** – Chat UI + visual dashboard

### Data
- **Hugging Face**: `imodels/diabetes-readmission`
- Synthetic + structured clinical features

### Storage
- In-memory chat memory  
- *(Supabase / SQL optional – future enhancement)*

---

##  Key Components

### 1️. Conversational Chatbot
- Multi-turn memory
- Patient-friendly prompts
- Incremental information gathering
- Intent detection (`discharge_planning` vs other)

---

### 2️. Intent & Slot Extraction Agent

Extracts structured JSON from free-text conversation:

```json
{
  "intent": "discharge_planning",
  "patient_summary": "",
  "diagnoses": [],
  "medications": [],
  "social_factors": ""
}
````

---

### 3️. Discharge Planning Agent (LangGraph)

* Safety checks
* Missing-information detection
* Care readiness assessment
* Hybrid **rule-based + LLM reasoning**

---

### 4️. ML Readmission Risk Model

* `RandomForestClassifier`
* Trained on 10 structured clinical features
* ROC-AUC ≈ **0.68**
* Outputs **probabilistic readmission risk**

---

### 5️. Visualization

* Discharge readiness indicators
* Readmission risk probability
* Timeline-style structured outputs

---

##  Project Structure
```
discharge-agent/
│
├── backend/                           # Backend services & agents
│   ├── __init__.py
│
│   ├── main.py                        # FastAPI entrypoint
│   ├── llm.py                         # Groq LLM factory (single source)
│   ├── graph.py                       # LangGraph discharge agent
│   ├── state.py                       # Shared agent state schema
│
│   ├── agents/                        # Core agent logic (LangGraph nodes)
│   │   ├── __init__.py
│   │   ├── clinical.py                # Clinical reasoning node
│   │   ├── coordination.py            # Agent flow control
│   │   ├── risk.py                    # ML risk integration
│   │   └── safety.py                  # Safety & rule checks
│
│   ├── chat/                          # Conversational interface
│   │   ├── __init__.py
│   │   ├── intent_extractor.py        # LLM-based slot extraction
│   │   ├── orchestrator.py            # Chat → agent controller
│   │   └── memory.py                  # LangChain memory abstraction
│
│   ├── models/                        # ML inference
│   │   ├── __init__.py
│   │   ├── readmission.py             # Prediction wrapper
│   │   └── readmission_model.joblib   # Trained RF model
│
│   └── data/                          # Backend sample data (optional)
│       └── sample_patient.json
│
├── ui/                                # Frontend (Streamlit)
│   ├── app.py                         # Chatbot + dashboard
│   └── assets/
│       └── architecture.png           # Architecture diagram (PNG)
│
├── notebooks/                         # Research & training
│   └── train_readmission.ipynb
│ 
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Installation & Setup

### 1️. Clone the Repository

```bash
git clone https://github.com/Janani-N14/Discharge_planning_agent.git
cd discharge-agent
```

---

### 2️. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

---

### 3️. Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file (never commit this):

```env
GROQ_API_KEY=your_groq_api_key
```

Use `.env.example` as reference.

---

##  Running the Application

### Start Backend

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

### Start UI

```bash
streamlit run ui/app.py
```

---

### Access Application

```
http://localhost:8501
```

---

##  Example Chat Flow

```
User: I was admitted for heart failure
Assistant: Thanks. Are you currently on any medications?
User: I take Lasix and Metoprolol
Assistant: Do you live alone or have caregiver support?
User: I live alone
```

 System triggers discharge assessment
 Predicts readmission risk
 Displays structured discharge guidance

---

##  Disclaimer

This system is a **research / proof-of-concept tool only**.

*  Not a medical device
*  Does not provide diagnosis or treatment
*  All outputs require **clinical review**

---

##  Security & Compliance Notes

* No PHI stored persistently
* Secrets protected via `.gitignore`
* Environment variables never committed
* Designed with **HIPAA-aligned architecture** (not certified)

---

##  Future Enhancements

* Persistent memory (Supabase / SQL)
* FHIR-compliant outputs
* Voice-based discharge assistant
* Clinician approval & override workflow

