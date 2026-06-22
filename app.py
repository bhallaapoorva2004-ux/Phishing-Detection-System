import streamlit as st
import pandas as pd
import joblib
import re
from urllib.parse import urlparse

# LOAD MODELS
model = joblib.load("phishing_detector.pkl")
pca = joblib.load("pca.pkl")
scaler = joblib.load("scaler.pkl")

st.title("🔐 Phishing Detection System")

# ======================
# INPUT BOX (IMPORTANT)
# ======================

url = st.text_input("Enter URL to check")

# ======================
# BUTTON
# ======================

if st.button("Predict"):

    if url == "":
        st.warning("Please enter a URL first")

    else:

        # Feature extraction
        parsed = urlparse(url)

        features = [
            len(url),
            url.count("."),
            url.count("/"),
            len(re.findall(r'[?&=%@]', url)),
            1 if parsed.scheme == "https" else 0,
            len(parsed.netloc)
        ]

        sample = pd.DataFrame([features], columns=[
            "URLLength",
            "DotCount",
            "SlashCount",
            "SpecialCharCount",
            "HTTPS",
            "DomainLength"
        ])

        # Prediction pipeline
        sample_scaled = scaler.transform(sample)
        sample_pca = pca.transform(sample_scaled)

        pred = model.predict(sample_pca)[0]
        prob = model.predict_proba(sample_pca)[0][1]

        # OUTPUT
        st.subheader("Result")

        st.write("URL:", url)
        st.write("Risk Score:", round(prob * 100, 2), "%")

        if pred == 1:
            st.error("🚨 PHISHING URL")
        else:
            st.success("✅ LEGITIMATE URL")
