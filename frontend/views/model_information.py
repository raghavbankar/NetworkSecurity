import streamlit as st

from api.client import get_model_info
from utils.charts import feature_importance_chart


def _format_percent(value):
    if value is None:
        return "Unavailable"
    return f"{value * 100:.2f}%"


def render():
    st.markdown('<div class="section-title">Model Information</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Live validation metrics, feature coverage, and model artifact details from the FastAPI backend.</div>',
        unsafe_allow_html=True,
    )

    response = get_model_info()
    if not response.get("ok"):
        st.error(f"Model information is unavailable: {response.get('error', 'backend request failed')}")
        st.info("Restart the FastAPI server after the backend changes, then refresh this page.")
        return

    info = response["data"]
    metrics = info.get("metrics", {})

    metric_items = [
        ("Features", info.get("feature_count", "Unavailable")),
        ("Accuracy", _format_percent(metrics.get("accuracy"))),
        ("Precision", _format_percent(metrics.get("precision"))),
        ("Recall", _format_percent(metrics.get("recall"))),
        ("F1 Score", _format_percent(metrics.get("f1_score"))),
    ]

    cols = st.columns(5)
    for index, (label, value) in enumerate(metric_items):
        with cols[index]:
            st.metric(label, value)

    st.subheader("Feature Importance")
    feature_importance = info.get("feature_importance", [])
    if feature_importance:
        st.plotly_chart(feature_importance_chart(feature_importance), use_container_width=True)
    else:
        st.info("This estimator does not expose feature importance or coefficients.")
        st.plotly_chart(feature_importance_chart(), use_container_width=True)

    st.subheader("Model Artifact")
    st.write(f"Model path: `{info.get('model_path', 'Unavailable')}`")
    st.write(f"Validation data: `{info.get('test_data_path') or 'Unavailable'}`")

    st.subheader("Model Description")
    st.write(info.get("description", "The backend serves the serialized training pipeline model."))

    st.subheader("Architecture")
    st.write(
        "Streamlit sends validated feature records to FastAPI. FastAPI loads the latest `Model.pkl`, validates the "
        "feature vector against the expected 30 columns, runs preprocessing, and returns binary predictions."
    )
