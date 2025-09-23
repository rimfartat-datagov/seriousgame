import streamlit as st

# --------------------------
# Scenario definitions
# --------------------------
scenarios = {
    "AI for Automated Purchase Orders": [
        {
            "question": "How do you discover and integrate supplier data?",
            "options": {
                "Manual spreadsheets from procurement": {"time": -2, "cost": +1, "trust": -2, "impact": -3},
                "Enterprise data catalog with master data": {"time": +2, "cost": -1, "trust": +3, "impact": +3}
            }
        },
        {
            "question": "How do you handle metadata & context?",
            "options": {
                "Skip metadata standards": {"time": +1, "cost": +2, "trust": -4, "impact": -3},
                "Structured metadata & taxonomy": {"time": -1, "cost": -1, "trust": +4, "impact": +4}
            }
        },
        {
            "question": "When do you validate data quality?",
            "options": {
                "Validate only at deployment": {"time": 0, "cost": +3, "trust": -3, "impact": -2},
                "Real-time validation in pipelines": {"time": -2, "cost": -1, "trust": +5, "impact": +5}
            }
        },
        {
            "question": "How do you manage access?",
            "options": {
                "Broad access for speed": {"time": +1, "cost": +3, "trust": -5, "impact": -2},
                "Role-based access & audit logs": {"time": -1, "cost": -1, "trust": +4, "impact": +3}
            }
        },
        {
            "question": "How do you scale to enterprise?",
            "options": {
                "Each region builds its own solution": {"time": +2, "cost": +2, "trust": -3, "impact": -5},
                "Centralized standardized pipeline": {"time": -1, "cost": -2, "trust": +5, "impact": +6}
            }
        }
    ],

    "GenAI Chatbot for Customers": [
        {
            "question": "How do you source data?",
            "options": {
                "Directly connect to raw database": {"time": +2, "cost": +2, "trust": -4, "impact": -3},
                "Curated datasets & knowledge graph": {"time": -2, "cost": -1, "trust": +5, "impact": +5}
            }
        },
        {
            "question": "How do you provide context to the LLM?",
            "options": {
                "Full docs without classification": {"time": +1, "cost": +2, "trust": -3, "impact": -2},
                "Embeddings + metadata categories (RAG)": {"time": -1, "cost": -1, "trust": +4, "impact": +4}
            }
        },
        {
            "question": "How do you monitor bias & quality?",
            "options": {
                "Deploy without monitoring": {"time": +1, "cost": +3, "trust": -5, "impact": -3},
                "Feedback loop + validation dashboard": {"time": -2, "cost": -1, "trust": +5, "impact": +4}
            }
        },
        {
            "question": "How do you ensure compliance?",
            "options": {
                "Skip explainability & GDPR checks": {"time": +1, "cost": +4, "trust": -6, "impact": -5},
                "Legal review + explainability layer": {"time": -2, "cost": -1, "trust": +6, "impact": +5}
            }
        },
        {
            "question": "How do you scale adoption?",
            "options": {
                "POC for one product only": {"time": +2, "cost": 0, "trust": -2, "impact": -4},
                "Governed multi-product rollout": {"time": -1, "cost": -2, "trust": +4, "impact": +6}
            }
        }
    ],

    "Predictive Maintenance for Manufacturing": [
        {
            "question": "How do you ingest IoT data?",
            "options": {
                "Direct raw streams, no schema": {"time": +2, "cost": +2, "trust": -3, "impact": -2},
                "Standardized ingestion platform": {"time": -2, "cost": -1, "trust": +4, "impact": +5}
            }
        },
        {
            "question": "How do you manage data quality?",
            "options": {
                "Clean data only when anomalies appear": {"time": +1, "cost": +3, "trust": -4, "impact": -2},
                "Continuous checks & thresholds": {"time": -2, "cost": -1, "trust": +5, "impact": +5}
            }
        },
        {
            "question": "How do you handle access & security?",
            "options": {
                "All engineers access raw streams": {"time": +1, "cost": +2, "trust": -3, "impact": -2},
                "Role-based access + anonymization": {"time": -1, "cost": -1, "trust": +4, "impact": +3}
            }
        },
        {
            "question": "What about model explainability?",
            "options": {
                "Black-box deep learning only": {"time": +1, "cost": +3, "trust": -5, "impact": -3},
                "Add SHAP/LIME explanations": {"time": -2, "cost": -1, "trust": +6, "impact": +5}
            }
        },
        {
            "question": "How do you scale across plants?",
            "options": {
                "Each plant builds separate model": {"time": +2, "cost": +2, "trust": -2, "impact": -4},
                "Central platform, shared governance": {"time": -1, "cost": -2, "trust": +5, "impact": +6}
            }
        }
    ]
}

# --------------------------
# Score interpretations
# --------------------------
def interpret_score(dimension, value):
    if dimension == "time":
        if value <= -3: return "🚀 Accelerated Delivery"
        elif -2 <= value <= 2: return "⚖️ Balanced speed"
        else: return "🐌 Slowed down delivery"
    if dimension == "cost":
        if value <= -3: return "💰 Optimized ROI & low risk"
        elif -2 <= value <= 2: return "⚖️ Average cost control"
        else: return "💸 High financial/regulatory risk"
    if dimension == "trust":
        if value >= 3: return "✅ High stakeholder trust"
        elif -2 <= value <= 2: return "⚖️ Medium trust"
        else: return "❌ Low trust, poor adoption"
    if dimension == "impact":
        if value >= 3: return "🌍 Enterprise transformation"
        elif -2 <= value <= 2: return "⚖️ Limited impact"
        else: return "🛑 Blocked scaling & adoption"

# --------------------------
# Session state initialization
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}

# --------------------------
# Helper functions
# --------------------------
def restart_game():
    st.session_state.page = "intro"
    st.session_state.scenario = None
    st.session_state.step = 0
    st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}

def show_scores():
    st.sidebar.markdown("### 📊 Scoreboard")
    st.sidebar.write(f"⏳ Time: {st.session_state.scores['time']}")
    st.sidebar.write(f"💸 Cost Risk: {st.session_state.scores['cost']}")
    st.sidebar.write(f"🔒 Trust: {st.session_state.scores['trust']}")
    st.sidebar.write(f"📈 Business Impact: {st.session_state.scores['impact']}")

def format_effects(effects):
    return f"(⏳ {effects['time']} | 💸 {effects['cost']} | 🔒 {effects['trust']} | 📈 {effects['impact']})"

# --------------------------
# Pages
# --------------------------
if st.session_state.page == "intro":
    st.title("🎮 Data Governance Serious Game")
    st.write("Welcome! In this game, you will make governance decisions while scaling AI use cases.")
    st.write("Each choice impacts **Time, Cost Risk, Trust, and Business Impact**:")
    st.markdown("""
    - ⏳ **Time**: Accelerate or delay delivery (hidden rework, data fixes).  
    - 💸 **Cost Risk**: ROI efficiency and regulatory/financial risks.  
    - 🔒 **Trust**: Stakeholder confidence, compliance, explainability.  
    - 📈 **Business Impact**: Ability to scale and transform at enterprise level.  
    """)
    st.write("Pick a scenario to start:")

    choice = st.selectbox("Choose your scenario", list(scenarios.keys()))
    if st.button("Start Scenario"):
        st.session_state.scenario = choice
        st.session_state.page = "scenario"

elif st.session_state.page == "scenario":
    show_scores()
    scenario = scenarios[st.session_state.scenario]
    step = st.session_state.step

    if step < len(scenario):
        st.subheader(f"Step {step+1}: {scenario[step]['question']}")
        for option, effects in scenario[step]["options"].items():
            label = f"{option} {format_effects(effects)}"
            if st.button(label):
                for dim, val in effects.items():
                    st.session_state.scores[dim] += val
                st.session_state.step += 1
                st.rerun()
    else:
        st.session_state.page = "end"
        st.rerun()

elif st.session_state.page == "end":
    st.title("🏁 Scenario Complete!")
    show_scores()
    scores = st.session_state.scores

    st.subheader("Your Results & Interpretations")
    st.write(f"⏳ **Time**: {scores['time']} → {interpret_score('time', scores['time'])}")
    st.write(f"💸 **Cost Risk**: {scores['cost']} → {interpret_score('cost', scores['cost'])}")
    st.write(f"🔒 **Trust**: {scores['trust']} → {interpret_score('trust', scores['trust'])}")
    st.write(f"📈 **Business Impact**: {scores['impact']} → {interpret_score('impact', scores['impact'])}")

    st.subheader("🔑 Key Learnings")
    st.markdown("""
    - Lack of governance often induces **delays and rework** later.  
    - **Metadata, lineage and access controls** are enablers for scaling AI.  
    - Governance ensures **trust, compliance, and adoption** of AI products.  
    """)

    if st.button("🔄 Play Another Scenario"):
        restart_game()
        st.rerun()
