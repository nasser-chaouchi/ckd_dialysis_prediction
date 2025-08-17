import streamlit as st
import joblib
import pandas as pd


st.set_page_config(
    page_title="Kidney Health Risk Prediction",
    page_icon=None,
    layout="wide"
)

CUSTOM_CSS = """
<style>
/* Typography */
html, body, [class*="css"]  {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif;
}
/* Cards */
.card {
    background: #ffffff;
    border: 1px solid #EAECF0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.06);
    margin-bottom: 16px;
}
.card-title {
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 8px;
    color: #111827;
}
.subtle {
    color: #6B7280;
}
.badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.9rem;
}
.badge-positive { background: #E8FAF1; color: #067647; border: 1px solid #C6F6D9; }
.badge-negative { background: #FEF3F2; color: #B42318; border: 1px solid #FEE4E2; }
.badge-warning { background: #FFF4E5; color: #B45309; border: 1px solid #FED7AA; }
.confbar {
    height: 10px;
    background: #F3F4F6;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 8px;
}
.confbar-fill {
    height: 100%;
    background: #2563EB;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


model_ckd = joblib.load("Rf_Model_CKD_Status.pkl")
model_dialysis = joblib.load("Rf_Model_Dialysis_Needed.pkl")


st.title("Kidney Health Risk Prediction")
st.markdown(
    "This tool provides predictions for **Chronic Kidney Disease (CKD)** risk "
    "and the potential **need for dialysis**, based on patient clinical indicators."
)

st.header("Patient Information")

age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.1, max_value=20.0, value=1.2, step=0.1)
bun = st.number_input("BUN (mg/dL)", min_value=1.0, max_value=200.0, value=20.0, step=1.0)
diabetes = st.radio("Diabetes", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
hypertension = st.radio("Hypertension", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
gfr = st.number_input("GFR (ml/min/1.73m²)", min_value=1.0, max_value=200.0, value=90.0, step=1.0)
urine_output = st.number_input("Urine Output (ml/day)", min_value=1.0, max_value=10000.0, value=1500.0, step=10.0)

X_input = pd.DataFrame([[age, creatinine, bun, diabetes, hypertension, gfr, urine_output]],
                       columns=["Age", "Creatinine_Level", "BUN", "Diabetes", "Hypertension", "GFR", "Urine_Output"])


if st.button("Run Prediction"):
    pred_ckd = model_ckd.predict(X_input)[0]
    proba_ckd = model_ckd.predict_proba(X_input)[0][1]

    st.markdown('<div class="card"><div class="card-title">Chronic Kidney Disease (CKD)</div>', unsafe_allow_html=True)
    if pred_ckd == 1:
        st.markdown('<span class="badge badge-negative">High risk of CKD</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-positive">Low risk of CKD</span>', unsafe_allow_html=True)

    st.markdown(f"**Probability:** {proba_ckd:.2%}")
    st.markdown(f'<div class="confbar"><div class="confbar-fill" style="width:{proba_ckd*100:.1f}%"></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    pred_dialysis = model_dialysis.predict(X_input)[0]
    proba_dialysis = model_dialysis.predict_proba(X_input)[0][1]

    st.markdown('<div class="card"><div class="card-title">Dialysis Risk</div>', unsafe_allow_html=True)
    if pred_dialysis == 1:
        st.markdown('<span class="badge badge-warning">High risk of requiring dialysis</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-positive">No immediate indication for dialysis</span>', unsafe_allow_html=True)

    st.markdown(f"**Probability:** {proba_dialysis:.2%}")
    st.markdown(f'<div class="confbar"><div class="confbar-fill" style="width:{proba_dialysis*100:.1f}%"></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

DISCLAIMER_CSS = """
<style>
.disclaimer {
    font-size: 0.85rem;
    color: #6B7280; /* gris clair */
    font-style: italic;
    margin-top: 1rem;
}
</style>
"""
st.markdown(DISCLAIMER_CSS, unsafe_allow_html=True)

st.markdown(
    """
<div class="disclaimer">
⚠️ This model has been trained on a clinical dataset for educational and research purposes only.  
It should not be used as a substitute for professional medical advice, diagnosis, or treatment.
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
    ---
    **Author: Nasser Chaouchi**  
    [LinkedIn](https://www.linkedin.com/in/nasser-chaouchi/) | [GitHub](https://github.com/nasser-chaouchi)
    """,
    unsafe_allow_html=True
)
