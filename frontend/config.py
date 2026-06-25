import os

try:
    import streamlit as st
except Exception:
    st = None


def _setting(name, default):
    if os.getenv(name):
        return os.getenv(name)
    if st is not None:
        try:
            return st.secrets.get(name, default)
        except Exception:
            return default
    return default


APP_NAME = "SentinelNet"
APP_SUBTITLE = "Network Security Detection"
BACKEND_URL = _setting("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = int(_setting("REQUEST_TIMEOUT", "30"))

MODEL_INFO = {
    "Model Name": "Network Security Phishing Detector",
    "Algorithm": "Best estimator selected from Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost",
    "Training Dataset": "Network_Data/phisingData.csv",
    "Accuracy": "Not exposed by API",
    "Precision": "Tracked in MLflow",
    "Recall": "Tracked in MLflow",
    "F1 Score": "Tracked in MLflow",
}
