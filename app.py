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

df = pd.read_csv("sample_dataset.csv")

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

st.title("🔐 Phishing Detection System")

st.subheader("📊 Dataset Source")

st.markdown(
"[Open Dataset Here](https://1drv.ms/x/c/e3b2ffe9b0de6239/IQB7jGG3gDBfSpz2jMFd_JnCAVBL6_7OBwRq6ewe3sEQjUQ?e=edtrbV)"
)

row = st.number_input(
"Enter Row Number",
min_value=0,
max_value=len(df) - 1,
value=0
)

# ==================================================

# PREDICTION

# ==================================================

if st.button("Predict"):

```
sample = X.iloc[[row]]

# ==================================================
# SHOW URL
# ==================================================

st.subheader("🌐 Selected URL")

selected_url = df.iloc[row]["URL"]

st.write(selected_url)

st.markdown(
    f"[🔗 Open URL]({selected_url})"
)

# ==================================================
# SHOW ACTUAL LABEL
# ==================================================

st.subheader("📌 Actual Dataset Label")

actual_label = df.iloc[row]["label"]

if actual_label == 1:
    st.error("Dataset Label: PHISHING")
else:
    st.success("Dataset Label: LEGITIMATE")

# ==================================================
# MODEL PREDICTION
# ==================================================

sample_scaled = scaler.transform(sample)

sample_pca = pca.transform(sample_scaled)

prediction = model.predict(sample_pca)[0]

risk_score = model.predict_proba(sample_pca)[0][1]

st.subheader("📊 Prediction Result")

st.write(
    "Risk Score:",
    round(risk_score * 100, 2),
    "%"
)

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

st.subheader("📌 Feature Values")

st.dataframe(sample.T)
```
