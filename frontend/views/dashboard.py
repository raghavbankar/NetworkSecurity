import pandas as pd
import streamlit as st

from api.client import get_model_info, get_prediction_stats
from utils.charts import history_bar, pie_predictions
from utils.style import metric_card


def _format_percent(value):
    if value is None:
        return "Unavailable"
    return f"{value * 100:.2f}%"


def render():
    st.markdown('<div class="section-title">Security Operations Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Persistent prediction activity and traffic risk summary from the FastAPI backend.</div>',
        unsafe_allow_html=True,
    )

    model_response = get_model_info()
    stats_response = get_prediction_stats()

    metrics = model_response.get("data", {}).get("metrics", {}) if model_response.get("ok") else {}
    accuracy = _format_percent(metrics.get("accuracy"))

    if stats_response.get("ok"):
        stats = stats_response["data"]
        summary = stats.get("summary", {"total": 0, "attacks": 0, "normal": 0, "attack_rate": 0})
        history = stats.get("analysis_history", [])
        recent = stats.get("recent_analyses", [])
    else:
        summary = {"total": 0, "attacks": 0, "normal": 0, "attack_rate": 0}
        history = []
        recent = []

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Predictions", summary["total"], "Stored by backend")
    with col2:
        metric_card("Attack Predictions", summary["attacks"], "High risk traffic")
    with col3:
        metric_card("Normal Predictions", summary["normal"], "Low risk traffic")
    with col4:
        metric_card("Model Accuracy", accuracy, "Latest validation test set")

    if not model_response.get("ok"):
        st.warning("Model metrics are unavailable because the backend metadata endpoint is not reachable.")
    if not stats_response.get("ok"):
        st.warning("Prediction history is unavailable because the backend stats endpoint is not reachable.")

    left, right = st.columns((1, 1.3))
    with left:
        st.plotly_chart(pie_predictions(summary), use_container_width=True)
    with right:
        st.plotly_chart(history_bar(history), use_container_width=True)

    if recent:
        st.dataframe(pd.DataFrame(recent), use_container_width=True, hide_index=True)
    else:
        st.info("No prediction history yet. Run a single or batch prediction to populate this dashboard.")
