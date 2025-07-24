import streamlit as st
import joblib
import numpy as np
import pandas as pd

model_ckd = joblib.load("Rf_Model_CKD_Status.pkl")
model_dialysis = joblib.load("Rf_Model_Dialysis_Needed.pkl")

st.title("🧬 Kidney Health Risk Prediction")

st.markdown("Predict the risk of **Chronic Kidney Disease (CKD)** and the potential **need for dialysis** based on patient clinical data.")

st.header("📋 Enter Patient Information")

age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.1, max_value=20.0, value=1.2, step=0.1)
bun = st.number_input("BUN (mg/dL)", min_value=1.0, max_value=200.0, value=20.0, step=1.0)
diabetes = st.radio("Diabetes", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
hypertension = st.radio("Hypertension", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
gfr = st.number_input("GFR (ml/min/1.73m²)", min_value=1.0, max_value=200.0, value=90.0, step=1.0)
urine_output = st.number_input("Urine Output (ml/day)", min_value=1.0, max_value=10000.0, value=1500.0, step=10.0)

X_input = pd.DataFrame([[
    age, creatinine, bun, diabetes, hypertension, gfr, urine_output
]], columns=[
    "Age", "Creatinine_Level", "BUN", "Diabetes", "Hypertension", "GFR", "Urine_Output"
])

if st.button("🔍 Predict"):

    pred_ckd = model_ckd.predict(X_input)[0]
    proba_ckd = model_ckd.predict_proba(X_input)[0][1]

    st.subheader("📊 CKD Prediction")
    if pred_ckd == 1:
        st.error("☠️ High risk of Chronic Kidney Disease detected.")
    else:
        st.success("✅ No signs of CKD detected at this time.")

    st.write(f"CKD Probability: **{proba_ckd:.2%}**")

    pred_dialysis = model_dialysis.predict(X_input)[0]
    proba_dialysis = model_dialysis.predict_proba(X_input)[0][1]

    st.subheader("💉 Dialysis Risk Prediction")
    if pred_dialysis == 1:
        st.warning("⚠️ Patient is at high risk of requiring dialysis based on current indicators.")
    else:
        st.info("💧 No immediate indication of dialysis need.")

    st.write(f"Dialysis Probability: **{proba_dialysis:.2%}**")
