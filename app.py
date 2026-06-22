import streamlit as st
import re
from urllib.parse import urlparse
def extract_features(url):

    parsed = urlparse(url)

    features = []

    # 1. URL Length
    features.append(len(url))

    # 2. Number of dots
    features.append(url.count("."))

    # 3. Number of slashes
    features.append(url.count("/"))

    # 4. Number of special characters
    features.append(len(re.findall(r'[?&=%@]', url)))

    # 5. Has HTTPS
    features.append(1 if parsed.scheme == "https" else 0)

    # 6. Domain length
    features.append(len(parsed.netloc))

    return features
    url = st.text_input("Enter URL to check")

if st.button("Predict"):

    if url:

        # convert URL → features
        features = extract_features(url)

        sample = pd.DataFrame([features], columns=[
            "URLLength",
            "DotCount",
            "SlashCount",
            "SpecialCharCount",
            "HTTPS",
            "DomainLength"
        ])

        # scaling + PCA
        sample_scaled = scaler.transform(sample)
        sample_pca = pca.transform(sample_scaled)

        # prediction
        pred = model.predict(sample_pca)[0]
        prob = model.predict_proba(sample_pca)[0][1]

        st.write("URL:", url)
        st.write("Risk Score:", round(prob*100,2), "%")

        if pred == 1:
            st.error("PHISHING URL 🚨")
        else:
            st.success("LEGITIMATE URL ✅")
