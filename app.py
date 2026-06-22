import streamlit as st
import pandas as pd
import joblib

# ==================================================
# LOAD MODEL FILES
# ==================================================

model = joblib.load("phishing_detector.pkl")
pca = joblib.load("pca.pkl")
scaler = joblib.load("scaler.pkl")

# ==================================================
# LOAD DATASET
# ==================================================

df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# ==================================================
# FEATURES
# ==================================================

X = df.drop(
    ["URL", "Domain", "Title", "TLD", "label"],
    axis=1
)

# ==================================================
# UI
# ==================================================

st.title("Phishing Detection System")

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

    sample = X.iloc[[row]]

    # Scaling
    sample_scaled = scaler.transform(sample)

    # PCA
    sample_pca = pca.transform(sample_scaled)

    # Prediction
    prediction = model.predict(sample_pca)[0]

    # Risk Score
    risk_score = model.predict_proba(sample_pca)[0][1]

    st.subheader("Prediction Results")

    st.write(
        "Risk Score:",
        round(risk_score * 100, 2),
        "%"
    )

    if prediction == 1:

        st.error("PHISHING URL DETECTED")

        action = "BLOCK"

    else:

        st.success("LEGITIMATE URL")

        action = "ALLOW"

    st.write("Recommended Action:", action)

    # ==================================================
    # BEHAVIORAL ANALYSIS
    # ==================================================

    st.subheader("Behavioral Analysis")

    behavior = []

    if "URLLength" in sample.columns:
        if sample["URLLength"].values[0] > 60:
            behavior.append(
                "Long URL structure detected"
            )

    if "DomainLength" in sample.columns:
        if sample["DomainLength"].values[0] > 20:
            behavior.append(
                "Suspiciously long domain name"
            )

    if "NoOfJS" in sample.columns:
        if sample["NoOfJS"].values[0] > 10:
            behavior.append(
                "Heavy JavaScript usage detected"
            )

    if len(behavior) == 0:

        st.success(
            "No major suspicious behavior detected."
        )

    else:

        for item in behavior:

            st.write("•", item)

    # ==================================================
    # FEATURE VALUES
    # ==================================================

    st.subheader("Selected URL Features")

    st.dataframe(sample.T)