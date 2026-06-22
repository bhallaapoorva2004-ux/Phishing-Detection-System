# Phishing Detection System (ML + Streamlit)

A Machine Learning based Phishing URL Detection System that classifies URLs as Phishing or Legitimate using XGBoost, PCA, and behavioral analysis. The system is deployed using Streamlit.

## Live Demo
https://your-streamlit-app-link.streamlit.app

## Project Overview
This project detects phishing URLs using machine learning. It analyzes URL structure, domain features, and behavior patterns to predict whether a URL is safe or malicious.

## Features
- Phishing / Legitimate classification
- Risk score (0–100%)
- Behavioral analysis
- URL display with clickable link
- Feature inspection

## Machine Learning Pipeline
Dataset → Preprocessing → Scaling → PCA → XGBoost Model → Prediction

## Features Used
- URL Length
- Domain Length
- NoOfJS
- NoOfCSS
- URL Similarity Index
- Special Characters
- HTTPS usage
- External references

## Project Structure
Phishing-Detection-System/
- app.py
- phishing_detector.pkl
- pca.pkl
- scaler.pkl
- sample_dataset.csv
- requirements.txt
- README.md

## How It Works
1. User selects row number
2. System extracts features
3. Data is scaled and transformed using PCA
4. XGBoost model predicts result
5. Risk score is generated
6. Behavioral analysis explains result
7. Final decision (ALLOW / BLOCK)

## Behavioral Analysis

Phishing URLs:
- Long and complex URLs
- Multiple subdomains
- High special characters
- Fake login pages
- High JavaScript usage

Legitimate URLs:
- Short and clean URLs
- Trusted domains
- HTTPS enabled
- Minimal suspicious behavior

## Output Example
URL: https://example.com/login

Prediction: PHISHING  
Risk Score: 97.3%

Behavioral Analysis:
- Long URL detected
- High JS usage
- Suspicious domain pattern

Recommended Action: BLOCK

## Tech Stack
Python, Pandas, Scikit-learn, XGBoost, Streamlit, Joblib

## Author
Apoorva Bhalla

## Future Improvements
- Real-time URL input
- Email phishing detection
- API deployment
- Advanced dashboard
