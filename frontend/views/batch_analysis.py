from datetime import datetime

import pandas as pd
import streamlit as st

from api.client import ApiError, predict_batch
from utils.charts import pie_predictions, risk_histogram
from utils.data import attach_predictions, frame_to_instances, make_report_csv, prediction_summary, validate_input_frame
from utils.style import metric_card


def render():
    st.markdown('<div class="section-title">Batch Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Upload a CSV, validate its feature schema, and analyze every record through FastAPI.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload network traffic CSV", type=["csv"], accept_multiple_files=False)
    if uploaded_file is None:
        st.info("Upload a CSV with the 30 model feature columns. A `Result` column is allowed and ignored.")
        return

    try:
        frame = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        return

    valid, message = validate_input_frame(frame)
    if valid:
        st.success(message)
    else:
        st.error(message)
        return

    st.dataframe(frame.head(20), use_container_width=True)

    if not st.button("Analyze Batch", use_container_width=True):
        return

    with st.spinner("Sending records to prediction API..."):
        try:
            instances = frame_to_instances(frame)
            response = predict_batch(instances)
            predictions = response["predictions"]
        except (ApiError, ValueError, KeyError) as exc:
            st.error(f"Batch analysis failed: {exc}")
            return

    results = attach_predictions(frame, predictions)
    st.session_state["last_batch_results"] = results
    st.session_state.setdefault("all_predictions", []).extend([int(value) for value in predictions])

    summary = prediction_summary(predictions)
    st.session_state.setdefault("recent_analyses", []).append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "Batch",
            "records": summary["total"],
            "attacks": summary["attacks"],
            "normal": summary["normal"],
        }
    )
    st.session_state.setdefault("analysis_history", []).append(
        {
            "run": f"Batch {len(st.session_state['analysis_history']) + 1}",
            "attacks": summary["attacks"],
            "normal": summary["normal"],
        }
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Records", summary["total"])
    with col2:
        metric_card("Attacks Detected", summary["attacks"])
    with col3:
        metric_card("Normal Traffic", summary["normal"])
    with col4:
        metric_card("Attack Percentage", f"{summary['attack_rate']}%")

    chart_col, hist_col = st.columns(2)
    with chart_col:
        st.plotly_chart(pie_predictions(summary), use_container_width=True)
    with hist_col:
        st.plotly_chart(risk_histogram(results), use_container_width=True)

    breakdown = results["Prediction"].value_counts().rename_axis("Prediction").reset_index(name="Records")
    st.bar_chart(breakdown, x="Prediction", y="Records", use_container_width=True)

    st.dataframe(results, use_container_width=True, hide_index=True)
    report_csv = make_report_csv(results)
    st.download_button(
        "Download Results CSV",
        data=report_csv,
        file_name="network_security_predictions.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.download_button(
        "Generate Security Report",
        data=_make_security_report(summary),
        file_name="security_analysis_report.md",
        mime="text/markdown",
        use_container_width=True,
    )


def _make_security_report(summary):
    return f"""# Security Analysis Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total records analyzed: {summary["total"]}
Attack predictions: {summary["attacks"]}
Normal predictions: {summary["normal"]}
Attack percentage: {summary["attack_rate"]}%

Recommended action:
- Review high-risk records before allowing traffic.
- Enrich suspicious records with domain, DNS, and threat intelligence context.
- Monitor repeated suspicious feature patterns across future uploads.
"""

