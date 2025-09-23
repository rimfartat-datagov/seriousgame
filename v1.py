import streamlit as st

# ------------------------
# Scenario definitions
# ------------------------
scenarios = {
    "AI Purchase Order Assistant": [
        {
            "question": "You need supplier data. Do you...",
            "options": {
                "Manually collect spreadsheets from teams": {"time": 2, "cost": 2, "trust": -2, "impact": -2},
                "Invest in a governed supplier data catalog": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "Data shows inconsistencies in supplier IDs. Do you...",
            "options": {
                "Let developers fix them case by case": {"time": 2, "cost": 2, "trust": -1, "impact": -2},
                "Set up data quality validation rules": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "Procurement asks about AI explainability. Do you...",
            "options": {
                "Deliver a black-box model": {"time": -1, "cost": -1, "trust": -2, "impact": -2},
                "Provide explainable ML with governance policies": {"time": 1, "cost": 1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "Scaling to multiple regions. Do you...",
            "options": {
                "Copy-paste local pipelines": {"time": 2, "cost": 2, "trust": -1, "impact": -2},
                "Standardize with metadata lineage & access controls": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "External supplier datasets available. Do you...",
            "options": {
                "Ingest without compliance review": {"time": 1, "cost": 3, "trust": -2, "impact": -2},
                "Review external data for compliance & quality": {"time": -1, "cost": -1, "trust": 2, "impact": 2}
            }
        }
    ],
    "GenAI Customer Chatbot": [
        {
            "question": "You need product info for chatbot answers. Do you...",
            "options": {
                "Scrape PDFs without metadata": {"time": 1, "cost": 2, "trust": -2, "impact": -2},
                "Build knowledge base with metadata management": {"time": -1, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "LLM hallucinations appear. Do you...",
            "options": {
                "Ignore and launch anyway": {"time": -1, "cost": 2, "trust": -2, "impact": -2},
                "Add data validation & retrieval-augmented generation": {"time": 1, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "Legal team mentions AI Act constraints. Do you...",
            "options": {
                "Hope compliance won’t be checked": {"time": -1, "cost": 3, "trust": -3, "impact": -2},
                "Document model lineage & explainability": {"time": 1, "cost": -1, "trust": 3, "impact": 2}
            }
        },
        {
            "question": "Scaling chatbot to multiple languages. Do you...",
            "options": {
                "Use ad hoc translation tools": {"time": 1, "cost": 1, "trust": -1, "impact": -2},
                "Centralize multilingual metadata & access policies": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "You want to add third-party market data. Do you...",
            "options": {
                "Ingest without license review": {"time": 1, "cost": 3, "trust": -2, "impact": -2},
                "Check compliance & integrate via governed pipeline": {"time": -1, "cost": -1, "trust": 2, "impact": 2}
            }
        }
    ],
    "Predictive Maintenance AI": [
        {
            "question": "IoT sensors produce raw data. Do you...",
            "options": {
                "Let engineers store locally": {"time": 1, "cost": 1, "trust": -1, "impact": -2},
                "Ingest into governed data lake with catalog": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "You detect missing sensor values. Do you...",
            "options": {
                "Patch manually when alerts fail": {"time": 2, "cost": 2, "trust": -1, "impact": -2},
                "Set automated data quality rules": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "Maintenance team wants explainability. Do you...",
            "options": {
                "Give them probability scores only": {"time": -1, "cost": -1, "trust": -2, "impact": -2},
                "Provide transparent rules & lineage": {"time": 1, "cost": 1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "Scaling to global factories. Do you...",
            "options": {
                "Let each factory design pipelines": {"time": 2, "cost": 2, "trust": -1, "impact": -2},
                "Standardize tools with access/security governance": {"time": -2, "cost": -1, "trust": 2, "impact": 2}
            }
        },
        {
            "question": "External benchmark datasets are available. Do you...",
            "options": {
                "Import without checks": {"time": 1, "cost": 3, "trust": -2, "impact": -2},
                "Review external data for compliance & quality": {"time": -1, "cost": -1, "trust": 2, "impact": 2}
            }
        }
    ]
}

# ------------------------
# Interpretation functions
# ------------------------
def interpret_time(score):
    if score <= -3:
        return "🐌 Lost days: Lack of governance duplicated efforts and slowed time-to-market."
    elif -2 <= score <= 2:
        return "⚖️ Balanced: Average delivery speed, some rework still required."
    else:
        return "🚀 Accelerated Delivery: Governance enabled automation and reuse, reducing delays."

def interpret_cost(score):
    if score <= -3:
        return "💸 High Risk: Exposed to fines, overruns, and low ROI due to weak governance."
    elif -2 <= score <= 2:
        return "⚖️ Average: Some costs controlled, but risks remain."
    else:
        return "💰 Optimized ROI: Controlled risks, maximized value of AI."

def interpret_trust(score):
    if score >= 3:
        return "✅ High Trust: Strong explainability, compliance, and reliable data."
    elif -2 <= score <= 2:
        return "⚖️ Medium Trust: Some adoption, but doubts remain on transparency or quality."
    else:
        return "❌ Low Trust: Stakeholders reject solutions due to black-box models, poor quality, or compliance gaps."

def interpret_impact(score):
    if score >= 3:
        return "🌍 Enterprise Impact: Governance choices enabled scaling across domains."
    elif -2 <= score <= 2:
        return "⚖️ Limited Impact: Success at local/POC level, struggles to scale broadly."
    else:
        return "🛑 Blocked Impact: Lack of governance prevented transformation and scaling."

# ------------------------
# Streamlit app
# ------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}

# Intro page
if st.session_state.page == "intro":
    st.title("🎮 Data Governance Serious Game")
    st.write("""
    Welcome!  
    Each scenario represents an AI project.  
    Every decision you make will impact four key **dimensions of data governance**:
    
    - ⏳ **Time**: Delivery speed (accelerated vs delayed).  
    - 💸 **Cost Risk**: ROI and risk exposure (fines, overruns, wasted spend).  
    - 🔒 **Trust**: Stakeholder confidence, explainability, compliance.  
    - 📈 **Business Impact**: Ability to scale and transform enterprise-wide.  
    
    Your goal: make choices that maximize governance, adoption, and enterprise impact!
    """)

    st.subheader("Choose your scenario:")
    for s in scenarios.keys():
        if st.button(s):
            st.session_state.scenario = s
            st.session_state.page = "game"
            st.session_state.question_index = 0
            st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}
            st.rerun()

# Game page
elif st.session_state.page == "game":
    scenario = scenarios[st.session_state.scenario]
    q_idx = st.session_state.question_index
    question_data = scenario[q_idx]

    st.header(f"Scenario: {st.session_state.scenario}")
    st.subheader(f"Step {q_idx+1}: {question_data['question']}")

    for option, effects in question_data["options"].items():
        label = (
            f"{option}\n"
            f"⏳ {effects['time']} | 💸 {effects['cost']} | 🔒 {effects['trust']} | 📈 {effects['impact']}"
        )
        if st.button(label):
            for k in st.session_state.scores:
                st.session_state.scores[k] += effects[k]
            if q_idx + 1 < len(scenario):
                st.session_state.question_index += 1
            else:
                st.session_state.page = "results"
            st.rerun()

    # Scoreboard
    st.sidebar.subheader("📊 Current Scores")
    for k, v in st.session_state.scores.items():
        st.sidebar.write(f"{k.capitalize()}: {v}")

# Results page
elif st.session_state.page == "results":
    scores = st.session_state.scores
    st.title("🏁 Results")

    st.write("Here’s how your governance choices played out:")

    st.write(f"⏳ Time: {scores['time']} → {interpret_time(scores['time'])}")
    st.write(f"💸 Cost Risk: {scores['cost']} → {interpret_cost(scores['cost'])}")
    st.write(f"🔒 Trust: {scores['trust']} → {interpret_trust(scores['trust'])}")
    st.write(f"📈 Business Impact: {scores['impact']} → {interpret_impact(scores['impact'])}")

    st.subheader("📚 Key Learnings")
    st.write("""
    - Lack of governance induces delays and roadblocks later.  
    - Metadata, lineage & access are enablers for scaling AI.  
    - Governance drives adoption, trust, and enterprise impact.  
    """)

    st.subheader("🔄 Try another scenario")
    if st.button("Back to intro"):
        st.session_state.page = "intro"
        st.rerun()
