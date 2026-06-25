import streamlit as st

from api.client import check_health
from config import BACKEND_URL


def render():
    st.markdown('<div class="section-title">API Status</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Backend availability and endpoint response information.</div>',
        unsafe_allow_html=True,
    )

    health = check_health()
    status = "Healthy" if health["ok"] else "Unavailable"
    css_class = "risk-low" if health["ok"] else "risk-high"

    st.markdown(
        f"""
        <div class="status-card {css_class}">
            <div class="metric-label">Backend Status</div>
            <div class="metric-value">{status}</div>
            <div>Base URL: {BACKEND_URL}</div>
            <div>Response Time: {health.get("elapsed_ms", 0)} ms</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Endpoint Availability")
    endpoints = [
        {"Endpoint": "GET /health", "Status": "Available" if health["ok"] else "Unavailable"},
        {"Endpoint": "GET /model_info", "Status": "Configured"},
        {"Endpoint": "POST /predict", "Status": "Configured"},
        {"Endpoint": "POST /predict_batch", "Status": "Configured"},
    ]
    st.dataframe(endpoints, use_container_width=True, hide_index=True)

    if health["ok"]:
        st.json(health.get("data", {}))
    else:
        st.error(health.get("error", "Backend health check failed."))


