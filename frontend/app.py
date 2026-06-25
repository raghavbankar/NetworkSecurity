import streamlit as st

from config import APP_NAME, APP_SUBTITLE, BACKEND_URL
from views import api_status, batch_analysis, dashboard, model_information, single_prediction
from utils.style import apply_theme


st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    page_icon=":material/security:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

for key, default in {
    "all_predictions": [],
    "analysis_history": [],
    "recent_analyses": [],
}.items():
    st.session_state.setdefault(key, default)

PAGES = {
    ":material/dashboard: Dashboard": dashboard.render,
    ":material/radar: Single Prediction": single_prediction.render,
    ":material/upload_file: Batch Analysis": batch_analysis.render,
    ":material/model_training: Model Information": model_information.render,
    ":material/monitor_heart: API Status": api_status.render,
}


with st.sidebar:
    st.markdown(f'<div class="app-logo">{APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-caption">{APP_SUBTITLE}</div>', unsafe_allow_html=True)
    selected_page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("Backend")
    st.code(BACKEND_URL, language=None)
    st.caption("Set `BACKEND_URL` in Streamlit secrets or environment variables for deployment.")

PAGES[selected_page]()

