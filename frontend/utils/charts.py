import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CHART_TEMPLATE = "plotly_dark"
COLOR_MAP = {"Attack": "#ef4444", "Normal": "#22c55e", "High": "#ef4444", "Low": "#22c55e"}


def pie_predictions(summary):
    frame = pd.DataFrame(
        {"Class": ["Attack", "Normal"], "Count": [summary.get("attacks", 0), summary.get("normal", 0)]}
    )
    fig = px.pie(
        frame,
        values="Count",
        names="Class",
        color="Class",
        color_discrete_map=COLOR_MAP,
        hole=0.55,
        template=CHART_TEMPLATE,
    )
    fig.update_layout(showlegend=True, margin=dict(l=10, r=10, t=20, b=10), height=300)
    return fig


def history_bar(history):
    if not history:
        frame = pd.DataFrame({"run": ["No analyses"], "attacks": [0], "normal": [0]})
    else:
        frame = pd.DataFrame(history)
    fig = px.bar(
        frame,
        x="run",
        y=["attacks", "normal"],
        template=CHART_TEMPLATE,
        color_discrete_sequence=["#ef4444", "#22c55e"],
    )
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=320, legend_title_text="")
    return fig


def risk_histogram(results_frame):
    if results_frame.empty or "Risk Level" not in results_frame:
        return go.Figure()
    fig = px.histogram(
        results_frame,
        x="Risk Level",
        color="Risk Level",
        color_discrete_map=COLOR_MAP,
        template=CHART_TEMPLATE,
    )
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=280, showlegend=False)
    return fig


def feature_importance_chart(feature_importance=None):
    if feature_importance:
        frame = pd.DataFrame(feature_importance).rename(columns={"feature": "Feature", "importance": "Importance"}).head(12)
    else:
        frame = pd.DataFrame(
            {
                "Feature": [
                    "SSLfinal_State",
                    "URL_of_Anchor",
                    "web_traffic",
                    "having_Sub_Domain",
                    "Prefix_Suffix",
                    "Request_URL",
                    "Google_Index",
                ],
                "Importance": [0.18, 0.16, 0.14, 0.12, 0.1, 0.08, 0.07],
            }
        )
    fig = px.bar(
        frame,
        x="Importance",
        y="Feature",
        orientation="h",
        template=CHART_TEMPLATE,
        color="Importance",
        color_continuous_scale=["#38bdf8", "#2563eb"],
    )
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=340, coloraxis_showscale=False)
    return fig



