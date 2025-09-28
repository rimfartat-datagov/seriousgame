# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ----------------------------
# Page config & visual theme
# ----------------------------
st.set_page_config(page_title="Data Governance Serious Game", page_icon="🚀", layout="wide")

# Minimal CSS to improve look
st.markdown(
    """
    <style>
    /* App background and text */
    .stApp {
        background: #f7f9fb;
        color: #0f1720;
    }
    /* Buttons */
    .stButton>button {
        background: linear-gradient(180deg,#0d6efd,#0a58ca);
        color: white;
        border-radius: 8px;
        padding: 8px 12px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.95;
    }
    /* Sidebar header */
    .css-1y0tads {  /* may vary across Streamlit versions; kept minimal */
        font-weight:700;
    }
    /* Small card */
    .card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(15,23,36,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Leaderboard file
# ----------------------------
LEADERBOARD_FILE = "leaderboard.csv"

# ----------------------------
# Interpretations (intervals specified)
# ----------------------------
def interpret_dimension(value: int, dim: str) -> str:
    if dim == "time":
        if value <= -3:
            return "🐌 Lost days: Lack of governance duplicated efforts and slowed time-to-market."
        elif -2 <= value <= 2:
            return "⚖️ Balanced: Average delivery speed, some rework still required."
        else:
            return "🚀 Accelerated Delivery: Governance enabled automation and reuse, reducing delays."
    if dim == "cost":
        if value <= -3:
            return "💸 High Risk: Exposed to fines, overruns, and low ROI due to weak governance."
        elif -2 <= value <= 2:
            return "⚖️ Average: Some costs controlled, but risks remain."
        else:
            return "💰 Optimized ROI: Controlled risks, maximized value of AI."
    if dim == "trust":
        if value <= -3:
            return "❌ Low Trust: Stakeholders reject solutions due to black-box models, poor quality, or compliance gaps."
        elif -2 <= value <= 2:
            return "⚖️ Medium Trust: Some adoption, but doubts remain on transparency or quality."
        else:
            return "✅ High Trust: Strong explainability, compliance, and reliable data."
    if dim == "impact":
        if value <= -3:
            return "🛑 Blocked Impact: Lack of governance prevented transformation and scaling."
        elif -2 <= value <= 2:
            return "⚖️ Limited Impact: Success at local/POC level, struggles to scale broadly."
        else:
            return "🌍 Enterprise Impact: Governance choices enabled scaling across domains."

# ----------------------------
# Spider (radar) plot helper
# ----------------------------
def plot_spiderchart(scores: dict):
    labels = [l.capitalize() for l in scores.keys()]
    values = [scores[k] for k in scores.keys()]

    # Normalize for visualization: shift range so center isn't negative (optional)
    # We'll display raw values but map to symmetric scale for visual balance
    max_abs = max(6, max(abs(v) for v in values))  # at least 6 for decent axes
    scaled = [v / max_abs for v in values]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    scaled += scaled[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, scaled, color="#0d6efd", linewidth=2)
    ax.fill(angles, scaled, color="#0d6efd", alpha=0.25)

    # labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    # radial ticks: show meaningful ticks based on max_abs
    ticks = [-max_abs, -max_abs/2, 0, max_abs/2, max_abs]
    tick_labels = [str(int(t)) for t in ticks]
    ax.set_yticks([t/max_abs for t in ticks])
    ax.set_yticklabels(tick_labels)
    ax.set_ylim(-1, 1)
    ax.grid(color="#e6eef8")
    plt.title("Final Scores (normalized view)", y=1.08)
    return fig

# ----------------------------
# Story-driven scenarios (sequential lifecycle)
# Each scenario contains 5 steps, options include score impacts
# We'll ensure each question follows project lifecycle
# ----------------------------
scenarios = {
    "Automated Purchase Orders": [
        {
            "question": "Step 1 — Discovery: how do you source supplier/master data for the project?",
            "options": [
                ("Collect Excel exports from procurement teams (fast, fragmented)",
                 {"time": +2, "cost": +1, "trust": -2, "impact": -1}),
                ("Expose ERP supplier APIs via IT (structured, work to integrate)",
                 {"time": -1, "cost": -1, "trust": +1, "impact": +1}),
                ("Invest in a supplier master-data platform (MDM) for reuse",
                 {"time": -3, "cost": -3, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 2 — Quality: duplicates & missing fields are discovered. What is your approach?",
            "options": [
                ("Ask users to correct records manually (ad-hoc)",
                 {"time": +2, "cost": +1, "trust": -2, "impact": -1}),
                ("Automate validation rules at ingestion (pipelines)",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Launch MDM deduplication and data stewardship program",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 3 — Metadata & lineage: AI team struggles to interpret fields. What do you do?",
            "options": [
                ("Document ad-hoc in Confluence (manual)",
                 {"time": 0, "cost": -1, "trust": +1, "impact": 0}),
                ("Create a simple data catalog with field definitions",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Deploy catalog with lineage & glossary integrated with tools",
                 {"time": -2, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 4 — Access & security: who should access supplier data and how?",
            "options": [
                ("Share spreadsheets across teams (open access)",
                 {"time": +1, "cost": +2, "trust": -3, "impact": -1}),
                ("Use SharePoint with coarse permissions",
                 {"time": 0, "cost": -1, "trust": +1, "impact": 0}),
                ("Implement RBAC & audit logging in platform",
                 {"time": -1, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 5 — Scaling: pilot succeeded — what's your roll-out strategy?",
            "options": [
                ("Leave it as a POC in one business unit",
                 {"time": +1, "cost": 0, "trust": -2, "impact": -2}),
                ("Expand step-by-step with light governance",
                 {"time": -1, "cost": -1, "trust": +1, "impact": +1}),
                ("Design enterprise roadmap with standard pipelines & cost control",
                 {"time": -3, "cost": -3, "trust": +3, "impact": +3})
            ]
        }
    ],

    "Predictive Maintenance with IoT Data": [
        {
            "question": "Step 1 — Discovery: plants log data in many formats. How do you onboard data?",
            "options": [
                ("Collect CSV exports from each plant (quick but siloed)",
                 {"time": +3, "cost": 0, "trust": -2, "impact": -2}),
                ("Connect to SCADA/edge via APIs (reliable streams)",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Centralize in an IoT data lake with schemas (future-proof)",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 2 — Quality: sensors show noise, missing values. What approach?",
            "options": [
                ("Let data scientists clean case-by-case",
                 {"time": +3, "cost": 0, "trust": -2, "impact": -2}),
                ("Implement anomaly detection and auto-corrections",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Build full validation pipelines and monitoring",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 3 — Lineage & explainability: maintenance teams ask where predictions come from. You should:",
            "options": [
                ("Rely on engineers' tacit knowledge",
                 {"time": +1, "cost": 0, "trust": -3, "impact": -1}),
                ("Document transformations in Git/Confluence",
                 {"time": 0, "cost": -1, "trust": +1, "impact": 0}),
                ("Deploy metadata catalog with lineage & dashboards",
                 {"time": -2, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 4 — Compliance (AI Act): predictive maintenance may be high risk. You:",
            "options": [
                ("Defer compliance work until after launch",
                 {"time": +1, "cost": +2, "trust": -2, "impact": -1}),
                ("Document decisions, add explainability tools",
                 {"time": -1, "cost": -1, "trust": +2, "impact": 0}),
                ("Set governance, audits and continuous controls",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +1})
            ]
        },
        {
            "question": "Step 5 — Scaling: pilot shows value. Rollout plan?",
            "options": [
                ("Keep one-off models per plant",
                 {"time": +2, "cost": +2, "trust": -2, "impact": -3}),
                ("Standardize processes and share best-practices",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Build central platform with reusable models & governance",
                 {"time": -3, "cost": -3, "trust": +3, "impact": +3})
            ]
        }
    ],

    "GenAI Chatbot for Customers": [
        {
            "question": "Step 1 — Discovery & prep: content is in many formats and links broken. What do you do?",
            "options": [
                ("Skip cleaning, rely on embeddings (fast)",
                 {"time": +3, "cost": 0, "trust": -2, "impact": -2}),
                ("Standardize formats and fix links (practical)",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Tag content with metadata and lineage in a catalog",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 2 — Context for LLM: managers ask for source visibility. You choose:",
            "options": [
                ("Deploy black-box LLM with no citations",
                 {"time": +3, "cost": 0, "trust": -3, "impact": -2}),
                ("Use RAG with source citations",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Train domain LLM + audit trail/dashboards",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 3 — Access control: some docs are sensitive. You:",
            "options": [
                ("Make bot public with no restrictions",
                 {"time": +1, "cost": 0, "trust": -3, "impact": -2}),
                ("Maintain internal & external bots separately",
                 {"time": 0, "cost": 0, "trust": +1, "impact": -1}),
                ("Integrate with SSO and RBAC for granular access",
                 {"time": -2, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 4 — Monitoring & quality: how to limit hallucinations?",
            "options": [
                ("Rely on users to report bad answers",
                 {"time": +2, "cost": 0, "trust": -3, "impact": -2}),
                ("Set up automated QA & human-in-the-loop review",
                 {"time": -1, "cost": -1, "trust": +2, "impact": +1}),
                ("Implement continuous evaluation + SLAs + retraining pipeline",
                 {"time": -3, "cost": -2, "trust": +3, "impact": +2})
            ]
        },
        {
            "question": "Step 5 — Scaling: leadership requests a company-wide rollout. You:",
            "options": [
                ("Keep it for customer support only",
                 {"time": +1, "cost": -2, "trust": -2, "impact": 0}),
                ("Extend to sales and partners with light governance",
                 {"time": -1, "cost": -1, "trust": +1, "impact": +1}),
                ("Integrate into enterprise portals with strict governance",
                 {"time": -3, "cost": -3, "trust": +3, "impact": +3})
            ]
        }
    ]
}

# ----------------------------
# Initialize session state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}
if "leaderboard" not in st.session_state:
    # load leaderboard from file if exists
    if os.path.exists(LEADERBOARD_FILE):
        try:
            st.session_state.leaderboard = pd.read_csv(LEADERBOARD_FILE)
        except Exception:
            st.session_state.leaderboard = pd.DataFrame(columns=["Timestamp","Name","Scenario","Time","Cost","Trust","Impact","Total"])
    else:
        st.session_state.leaderboard = pd.DataFrame(columns=["Timestamp","Name","Scenario","Time","Cost","Trust","Impact","Total"])

# ----------------------------
# Helper: save leaderboard persistently
# ----------------------------
def save_leaderboard_df(df: pd.DataFrame):
    df.to_csv(LEADERBOARD_FILE, index=False)

# ----------------------------
# UI: Sidebar scoreboard & navigation
# ----------------------------
def show_sidebar():
    st.sidebar.markdown("### 📊 Scoreboard")
    st.sidebar.write(f"⏳ Time: {st.session_state.scores['time']}")
    st.sidebar.write(f"💸 Cost Risk: {st.session_state.scores['cost']}")
    st.sidebar.write(f"🔒 Trust: {st.session_state.scores['trust']}")
    st.sidebar.write(f"📈 Business Impact: {st.session_state.scores['impact']}")
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Restart (choose another scenario)"):
        st.session_state.page = "intro"
        st.session_state.scenario = None
        st.session_state.step = 0
        st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}
        st.rerun()
    if st.sidebar.button("🏆 View leaderboard"):
        st.session_state.page = "leaderboard"
        st.rerun()

# ----------------------------
# Page: Intro
# ----------------------------
if st.session_state.page == "intro":
    st.title("🚀 Data Governance Serious Game")
    st.markdown(
        """
        **Role:** vous incarnez un décideur data qui doit piloter le déploiement d’un produit IA.  
        **Objectif pédagogique :** comprendre l'impact des choix de gouvernance sur le **temps**, le **coût/risque**, la **confiance** et l'**impact business**.

        **Dimensions mesurées**
        - ⏳ **Time** : accélération ou retard (réparations / rework).  
        - 💸 **Cost Risk** : exposition financière, conformité, ROI.  
        - 🔒 **Trust** : explicabilité, adoption, conformité.  
        - 📈 **Business Impact** : capacité à scaler et transformer.

        Sélectionnez un scénario pour commencer — chaque scénario suit la logique d’un cycle de projet (Discovery → Quality → Metadata/Lineage → Compliance/Access → Scaling).
        """
    )
    st.markdown("----")
    choice = st.selectbox("👉 Choisissez un scénario", list(scenarios.keys()))
    if st.button("Start scenario"):
        st.session_state.scenario = choice
        st.session_state.page = "game"
        st.session_state.step = 0
        st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}
        st.rerun()
    st.write("")
    st.write("Vous pouvez consulter le leaderboard existant :")
    if st.button("Voir le leaderboard"):
        st.session_state.page = "leaderboard"
        st.rerun()

# ----------------------------
# Page: Game (play steps)
# ----------------------------
elif st.session_state.page == "game":
    show_sidebar()
    scenario_name = st.session_state.scenario
    steps = scenarios[scenario_name]
    step_idx = st.session_state.step
    total_steps = len(steps)

    # Progress bar and remaining questions
    progress = step_idx / total_steps
    st.progress(progress)
    st.markdown(f"**Progress:** Step {step_idx+1} / {total_steps} — Remaining: {max(0, total_steps - step_idx - 1)}")

    if step_idx < total_steps:
        step = steps[step_idx]
        st.subheader(step["question"])
        st.write("")  # spacing

        # Show options with explicit score effects
        for opt_idx, (label, impacts) in enumerate(step["options"]):
            # format impacts string
            impacts_str = f"⏳ {impacts['time']:+d}  |  💸 {impacts['cost']:+d}  |  🔒 {impacts['trust']:+d}  |  📈 {impacts['impact']:+d}"
            # Use columns to layout button and explanation
            c1, c2 = st.columns([4,6])
            with c1:
                if st.button(label + "   " + impacts_str, key=f"opt_{step_idx}_{opt_idx}"):
                    # apply impacts
                    for d,k in impacts.items():
                        st.session_state.scores[d] += k
                    st.session_state.step += 1
                    st.rerun()
            with c2:
                # If the option label contains explanatory text in parentheses, show it; otherwise blank
                # Better storytelling: show concise rationale
                st.write("")  # placeholder (could add more narrative per option)
    else:
        # Completed scenario
        st.success("🎉 Scenario completed!")
        st.markdown("## Final scores")
        scores = st.session_state.scores.copy()
        # Show numeric scores and interpretations
        cols = st.columns(4)
        dims = ["time", "cost", "trust", "impact"]
        for i, dim in enumerate(dims):
            with cols[i]:
                val = scores[dim]
                st.metric(label=dim.capitalize(), value=str(val))
                st.caption(interpret_dimension := interpret_dimension if False else interpret_dimension)  # no-op to avoid linter noise
                st.write(interpret_dimension(val, dim))

        st.markdown("---")
        # Spider chart
        st.markdown("### Visual summary (radar chart)")
        fig = plot_spiderchart(scores)
        st.pyplot(fig)

        # Total score calculation
        total_score = sum(scores.values())
        st.markdown(f"### Total score: **{total_score}**  (sum of four dimensions)")

        # Save to leaderboard
        st.markdown("### Save your result to the leaderboard")
        name = st.text_input("Your name (will appear on leaderboard):", value="")
        if st.button("Save score to leaderboard") and name.strip() != "":
            timestamp = datetime.utcnow().isoformat()
            entry = {
                "Timestamp": timestamp,
                "Name": name.strip(),
                "Scenario": st.session_state.scenario,
                "Time": scores["time"],
                "Cost": scores["cost"],
                "Trust": scores["trust"],
                "Impact": scores["impact"],
                "Total": total_score,
            }
            st.session_state.leaderboard = pd.concat([st.session_state.leaderboard, pd.DataFrame([entry])], ignore_index=True)
            save_leaderboard_df(st.session_state.leaderboard)
            st.success("✅ Score saved to leaderboard!")

        st.markdown("---")
        st.markdown("### Key learnings")
        st.markdown(
            """
            - Lack of governance often induces **delays and rework** later; invest early in discovery, metadata and quality.  
            - **Metadata, lineage and access controls** are enablers for scaling and explainability.  
            - Governance drives **trust, compliance, and adoption**, which are prerequisites to realize enterprise impact.
            """
        )

        if st.button("Play another scenario"):
            st.session_state.page = "intro"
            st.session_state.scenario = None
            st.session_state.step = 0
            st.session_state.scores = {"time": 0, "cost": 0, "trust": 0, "impact": 0}
            st.rerun()

        if st.button("View leaderboard"):
            st.session_state.page = "leaderboard"
            st.rerun()

# ----------------------------
# Page: Leaderboard
# ----------------------------
elif st.session_state.page == "leaderboard":
    show_sidebar()
    st.title("🏆 Leaderboard")
    df = st.session_state.leaderboard.copy()
    if df.empty:
        st.info("No entries yet — play a scenario and save your score!")
    else:
        # Allow filtering by scenario and sorting
        st.markdown("Filter & sort leaderboard")
        scenarios_list = ["All"] + sorted(df["Scenario"].unique().tolist())
        sel = st.selectbox("Scenario filter", scenarios_list)
        if sel != "All":
            df = df[df["Scenario"] == sel].copy()
        sort_col = st.selectbox("Sort by", ["Total", "Timestamp", "Name"], index=0)
        ascending = st.checkbox("Ascending", value=False)
        df = df.sort_values(by=sort_col, ascending=ascending).reset_index(drop=True)
        # Show nicer table
        display_df = df[["Timestamp","Name","Scenario","Time","Cost","Trust","Impact","Total"]]
        st.dataframe(display_df, use_container_width=True)

        # Quick stats
        st.markdown("#### Top performers")
        top_n = st.number_input("Top N", min_value=1, max_value=20, value=5, step=1)
        top_df = df.sort_values(by="Total", ascending=False).head(top_n)
        st.table(top_df[["Name","Scenario","Total"]].reset_index(drop=True))

        # Option to clear leaderboard (careful)
        if st.button("Clear leaderboard (danger!)"):
            st.session_state.leaderboard = pd.DataFrame(columns=["Timestamp","Name","Scenario","Time","Cost","Trust","Impact","Total"])
            if os.path.exists(LEADERBOARD_FILE):
                os.remove(LEADERBOARD_FILE)
            st.success("Leaderboard cleared.")
            st.rerun()

    if st.button("Back to intro"):
        st.session_state.page = "intro"
        st.rerun()
