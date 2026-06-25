import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #07111f;
            --panel: rgba(15, 23, 42, 0.78);
            --panel-border: rgba(148, 163, 184, 0.18);
            --text: #e5edf7;
            --muted: #94a3b8;
            --blue: #38bdf8;
            --green: #22c55e;
            --red: #ef4444;
            --amber: #f59e0b;
        }
        .stApp {
            background:
                radial-gradient(circle at 18% 8%, rgba(56, 189, 248, 0.12), transparent 26%),
                linear-gradient(135deg, #07111f 0%, #101827 45%, #07111f 100%);
            color: var(--text);
        }
        [data-testid="stSidebar"] {
            background: rgba(3, 7, 18, 0.9);
            border-right: 1px solid var(--panel-border);
        }
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }
        .section-title {
            font-size: 1.45rem;
            font-weight: 700;
            margin: 0.4rem 0 0.2rem;
            color: #f8fafc;
        }
        .section-subtitle {
            color: var(--muted);
            margin-bottom: 1.1rem;
        }
        .metric-card, .result-card, .status-card {
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.26);
        }
        .metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0;
        }
        .metric-value {
            font-size: 1.85rem;
            font-weight: 750;
            margin-top: 0.25rem;
        }
        .risk-low { border-left: 4px solid var(--green); }
        .risk-high { border-left: 4px solid var(--red); }
        .risk-medium { border-left: 4px solid var(--amber); }
        .app-logo {
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 0.1rem;
        }
        .app-caption {
            color: var(--muted);
            font-size: 0.85rem;
            margin-bottom: 1.2rem;
        }
        .stButton > button, .stDownloadButton > button {
            border-radius: 8px;
            border: 1px solid rgba(56, 189, 248, 0.36);
            background: linear-gradient(135deg, #0ea5e9, #2563eb);
            color: #f8fafc;
            font-weight: 700;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: rgba(125, 211, 252, 0.8);
            color: #ffffff;
        }
        div[data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, helper=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="section-subtitle">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

