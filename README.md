import streamlit as st
import pandas as pd
import joblib

# ==================================================
# LOAD MODEL + PREPROCESSORS
# ==================================================

model = joblib.load("phishing_detector.pkl")
pca = joblib.load("pca.pkl")
scaler = joblib.load("scaler.pkl")

# ==================================================
# LOAD DATASET
# ==================================================

df = pd.read_csv("sample_dataset.csv")

# Features (same as training)
X = df.drop(["URL", "Domain", "Title", "TLD", "label"], axis=1)

# ==================================================
# UI
# ==================================================

st.title("🔐 Phishing Detection System")

row = st.number_input(
    "Enter Row Number",
    min_value=0,
    max_value=len(df)-1,
    value=0
)

# ==================================================
# PREDICTION
# ==================================================

if st.button("Predict"):

    # select sample
    sample = X.iloc[[row]]

    # preprocessing
    sample_scaled = scaler.transform(sample)
    sample_pca = pca.transform(sample_scaled)

    # prediction
    prediction = model.predict(sample_pca)[0]
    risk_score = model.predict_proba(sample_pca)[0][1]

    # ==================================================
    # SHOW URL
    # ==================================================

    st.subheader("🌐 Selected URL")
    st.write(df.iloc[row]["URL"])

    st.markdown(
        f"[🔗 Open URL]({df.iloc[row]['URL']})"
    )

    # ==================================================
    # RESULT
    # ==================================================

    st.subheader("📊 Prediction Result")

    st.write("Risk Score:", round(risk_score * 100, 2), "%")

    if prediction == 1:
        st.error("🚨 PHISHING URL DETECTED")
        action = "BLOCK"
    else:
        st.success("✅ LEGITIMATE URL")
        action = "ALLOW"

    st.write("Recommended Action:", action)

    # ==================================================
    # BEHAVIORAL ANALYSIS
    # ==================================================

    st.subheader("🧠 Behavioral Analysis")

    behavior = []

    if "URLLength" in sample.columns:
        if sample["URLLength"].values[0] > 60:
            behavior.append("Long URL structure detected")

    if "DomainLength" in sample.columns:
        if sample["DomainLength"].values[0] > 20:
            behavior.append("Suspiciously long domain name")

    if "NoOfJS" in sample.columns:
        if sample["NoOfJS"].values[0] > 10:
            behavior.append("High JavaScript usage detected")

    if "NoOfCSS" in sample.columns:
        if sample["NoOfCSS"].values[0] > 5:
            behavior.append("High CSS resource usage")

    if len(behavior) == 0:
        st.success("No major suspicious behavior detected.")
    else:
        for b in behavior:
            st.write("•", b)

    # ==================================================
    # FEATURE VIEW
    # ==================================================

    st.subheader("📌 Feature Values")

    st.dataframe(sample.T)
