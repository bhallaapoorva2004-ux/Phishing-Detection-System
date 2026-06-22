import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("phishing_detector.pkl")
pca = joblib.load("pca.pkl")
scaler = joblib.load("scaler.pkl")

st.title("🔐 Phishing Detection System (Live URL)")

# =========================
# USER INPUT (NEW PART)
# =========================

url = st.text_input("Enter URL to Test")

# =========================
# BUTTON
# =========================

if st.button("Predict"):

    if url == "":
        st.warning("Please enter a URL")
    else:

        # ⚠️ IMPORTANT:
        # yaha tumhe feature extraction add karni hogi
        # abhi dummy example de raha hoon

        sample = pd.DataFrame([[len(url), url.count("."), url.count("/"), url.count("?")]],
                              columns=["URLLength","DotCount","SlashCount","QueryCount"])

        # scaling + PCA
        sample_scaled = scaler.transform(sample)
        sample_pca = pca.transform(sample_scaled)

        # prediction
        prediction = model.predict(sample_pca)[0]
        risk = model.predict_proba(sample_pca)[0][1]

        st.subheader("Result")

        st.write("URL:", url)
        st.write("Risk Score:", round(risk * 100, 2), "%")

        if prediction == 1:
            st.error("🚨 PHISHING URL")
        else:
            st.success("✅ LEGITIMATE URL")
