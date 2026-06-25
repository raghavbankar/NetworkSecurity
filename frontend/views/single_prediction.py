from datetime import datetime

import streamlit as st

from api.client import ApiError, predict_single
from utils.features import DEFAULT_FEATURE_VALUES, FEATURE_GROUPS, FEATURE_OPTIONS, label_for_prediction, risk_for_prediction


def _render_feature_input(feature_name):
    options = FEATURE_OPTIONS.get(feature_name, {-1: "Suspicious", 0: "Neutral", 1: "Safe"})
    values = list(options.keys())
    default = DEFAULT_FEATURE_VALUES.get(feature_name, values[0])
    index = values.index(default) if default in values else 0
    display = st.selectbox(
        feature_name,
        values,
        index=index,
        format_func=lambda value: f"{value} - {options[value]}",
        key=f"single_{feature_name}",
    )
    return float(display)


def render():
    st.markdown('<div class="section-title">Single Traffic Prediction</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Analyze one network security record using the deployed FastAPI model.</div>',
        unsafe_allow_html=True,
    )

    with st.form("single_prediction_form"):
        features = {}
        for group_name, feature_names in FEATURE_GROUPS.items():
            st.subheader(group_name)
            columns = st.columns(3)
            for index, feature_name in enumerate(feature_names):
                with columns[index % 3]:
                    features[feature_name] = _render_feature_input(feature_name)
        submitted = st.form_submit_button("Analyze Traffic", use_container_width=True)

    if not submitted:
        return

    with st.spinner("Analyzing traffic profile..."):
        try:
            response = predict_single(features)
            prediction = response["predictions"][0]
        except (ApiError, KeyError, IndexError) as exc:
            st.error(f"Prediction failed: {exc}")
            return

    label = label_for_prediction(prediction)
    risk = risk_for_prediction(prediction)
    card_class = "risk-low" if risk == "Low" else "risk-high"
    st.markdown(
        f"""
        <div class="result-card {card_class}">
            <div class="metric-label">Prediction</div>
            <div class="metric-value">{label}</div>
            <div>Confidence Score: Not provided by current backend</div>
            <div>Risk Level: {risk}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.success("Analysis complete.")

    st.session_state.setdefault("all_predictions", []).append(int(prediction))
    st.session_state.setdefault("recent_analyses", []).append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "Single",
            "records": 1,
            "attacks": 1 if int(prediction) == 0 else 0,
            "normal": 1 if int(prediction) == 1 else 0,
        }
    )
    st.session_state.setdefault("analysis_history", []).append(
        {
            "run": f"Single {len(st.session_state['analysis_history']) + 1}",
            "attacks": 1 if int(prediction) == 0 else 0,
            "normal": 1 if int(prediction) == 1 else 0,
        }
    )

