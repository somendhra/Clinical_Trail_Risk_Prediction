import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import datetime

# ======================================================
# THEME + FONT
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Roboto+Slab:wght@300;400;600&display=swap');

html, body, [class*="css"], label, div, span, p {
    font-family: 'Roboto Slab', serif !important;
}

h1, h2, h3, h4 {
    font-family: 'Montserrat', sans-serif !important;
    letter-spacing: 0.6px;
}

.stApp {
    background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #134E5E, #71B280);
}

.card {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    backdrop-filter: blur(14px);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATABASE SETUP
# ======================================================
def init_db():
    conn = sqlite3.connect("trial_predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phase INTEGER,
        patients INTEGER,
        duration_months INTEGER,
        duration_days INTEGER,
        age_group TEXT,
        region TEXT,
        comorbidity TEXT,
        probability REAL,
        risk_level TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_prediction(phase, patients, duration_months, duration_days,
                    age_group, region, comorbidity, probability, risk_level):
    conn = sqlite3.connect("trial_predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO predictions (
        phase, patients, duration_months, duration_days,
        age_group, region, comorbidity,
        probability, risk_level, timestamp
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        phase, patients, duration_months, duration_days,
        age_group, region, comorbidity,
        probability, risk_level,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

init_db()

# ======================================================
# LOAD MODEL
# ======================================================
model = joblib.load("trial_risk_model.pkl")
train_df = pd.read_csv("final_trial_risk_dataset.csv")
features = train_df.drop("Outcome", axis=1).columns.tolist()

# ======================================================
# PAGE SETTINGS
# ======================================================
st.set_page_config(
    page_title="Clinical Trial Risk Predictor",
    page_icon="🧪",
    layout="wide"
)

# ======================================================
# HEADER
# ======================================================
st.markdown("""
<div class="card" style="text-align:center;">
<h1 style="font-size:46px;">🧪 Clinical Trial Risk Prediction System</h1>
<p style="font-size:20px; opacity:0.9;">
AI-Based Decision Support for Healthcare & Pharma
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# TABS (PAGES)
# ======================================================
tab1, tab2 = st.tabs(["🧪 Trial Prediction", "📊 Experiment Database"])

# ======================================================
# PAGE 1 — PREDICTION
# ======================================================
with tab1:

    st.sidebar.header("📋 Trial Parameters")

    phase = st.sidebar.selectbox("Trial Phase", [1, 2, 3, 4])

    patients = st.sidebar.number_input(
        "Participants",
        min_value=1,
        max_value=10000,
        value=250
    )

    duration_months = st.sidebar.number_input(
        "Trial Duration (Months)",
        min_value=1,
        max_value=60,
        value=12,
        help="1 month ≈ 30 days"
    )

    duration_days = duration_months * 30

    age_group = st.sidebar.radio("Age Group", ["Young", "Middle", "Old"])

    region = st.sidebar.selectbox(
        "Region",
        ["India", "USA", "Europe", "Asia", "Other"]
    )

    comorbidity = st.sidebar.selectbox(
        "Comorbidity",
        ["None", "Diabetes", "Heart", "Lung", "BP"]
    )

    predict_btn = st.sidebar.button("🧠 Predict Trial Risk")

    left, right = st.columns(2)

    # ---------- INPUT SUMMARY ----------
    with left:
        st.markdown("""
        <div class="card">
        <h2>📊 Trial Summary</h2>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="font-size:18px; line-height:1.8;">
        <b>Phase:</b> {phase}<br>
        <b>Participants:</b> {patients}<br>
        <b>Duration:</b> {duration_months} months 
        <span style="opacity:0.85;">(~{duration_days} days)</span><br><br>
        <b>Age Group:</b> {age_group}<br>
        <b>Region:</b> {region}<br>
        <b>Comorbidity:</b> {comorbidity}
        </p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- RESULT ----------
    with right:
        st.markdown("""
        <div class="card">
        <h2>📈 Risk Assessment</h2>
        """, unsafe_allow_html=True)

        if predict_btn:
            input_data = {col: 0 for col in features}
            input_data["Phase"] = phase
            input_data["Patients"] = patients
            input_data["Duration"] = duration_days
            input_data[f"AgeGroup_{age_group}"] = 1
            input_data[f"Region_{region}"] = 1
            input_data[f"Comorbidity_{comorbidity}"] = 1

            data = pd.DataFrame([input_data])[features]
            prob = model.predict_proba(data)[0][1]
            prob_percent = round(prob * 100, 2)

            if prob > 0.7:
                risk = "LOW"
            elif prob > 0.4:
                risk = "MEDIUM"
            else:
                risk = "HIGH"

            save_prediction(
                phase, patients,
                duration_months, duration_days,
                age_group, region, comorbidity,
                prob_percent, risk
            )

            st.markdown(f"""
            <div style="text-align:center;
            font-size:70px;
            font-weight:800;
            color:#F9C74F;
            font-family:'Montserrat', sans-serif;">
            {prob_percent} %
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                "<h3 style='text-align:center;'>Probability of Successful Completion</h3>",
                unsafe_allow_html=True
            )

            st.progress(prob)
            st.markdown("<br>", unsafe_allow_html=True)

            if risk == "LOW":
                st.success("🟢 LOW RISK — Trial conditions are favorable.")
            elif risk == "MEDIUM":
                st.warning("🟡 MEDIUM RISK — Moderate uncertainty detected.")
            else:
                st.error("🔴 HIGH RISK — Immediate intervention required.")

        else:
            st.info("⬅️ Enter trial details and click **Predict Trial Risk**")

        st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# PAGE 2 — DATABASE
# ======================================================
with tab2:
    st.markdown("""
    <div class="card">
    <h2>📊 Experiment Database</h2>
    <p>Saved prediction history</p>
    </div>
    """, unsafe_allow_html=True)

    conn = sqlite3.connect("trial_predictions.db")
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC", conn
    )
    conn.close()

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ======================================================
# FOOTER
# ======================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-size:14px; opacity:0.85;">
Clinical Decision Support System • Machine Learning • Streamlit
</div>
""", unsafe_allow_html=True)