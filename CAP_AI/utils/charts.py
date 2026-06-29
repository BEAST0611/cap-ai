"""Plotly chart builders for CAP AI dashboard and modules."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="Inter"),
    margin=dict(l=40, r=40, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

COLORS = ["#0ea5e9", "#38bdf8", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"]


def apply_layout(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(**CHART_LAYOUT, title=dict(text=title, font=dict(size=16)))
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def transaction_volume_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty or "date" not in df.columns:
        dates = pd.date_range("2025-01-01", periods=12, freq="ME")
        vol = [1200, 1450, 1380, 1620, 1890, 2100, 1950, 2200, 2400, 2150, 2300, 2500]
        df = pd.DataFrame({"date": dates, "volume": vol})
    fig = px.area(df, x="date", y="volume", color_discrete_sequence=[COLORS[0]])
    return apply_layout(fig, "Transaction Volume")


def risk_distribution_chart() -> go.Figure:
    labels = ["Critical", "High", "Medium", "Low", "Info"]
    values = [8, 15, 32, 45, 20]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.45, marker_colors=COLORS[:5])])
    return apply_layout(fig, "Risk Distribution")


def fraud_trend_chart() -> go.Figure:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    detected = [3, 5, 4, 7, 6, 9, 8, 11, 10, 7, 6, 5]
    prevented = [8, 10, 12, 15, 14, 18, 16, 20, 19, 17, 15, 14]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=detected, name="Detected", line=dict(color=COLORS[4], width=3)))
    fig.add_trace(go.Scatter(x=months, y=prevented, name="Prevented", line=dict(color=COLORS[2], width=3)))
    return apply_layout(fig, "Monthly Fraud Trend")


def bank_charges_chart() -> go.Figure:
    categories = ["ATM", "NEFT", "RTGS", "SMS", "Maintenance", "Cheque"]
    expected = [1200, 800, 500, 300, 1500, 600]
    actual = [1350, 820, 480, 350, 1800, 720]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Expected", x=categories, y=expected, marker_color=COLORS[0]))
    fig.add_trace(go.Bar(name="Actual", x=categories, y=actual, marker_color=COLORS[4]))
    fig.update_layout(barmode="group")
    return apply_layout(fig, "Bank Charges Analysis")


def interest_comparison_chart() -> go.Figure:
    months = [f"M{i}" for i in range(1, 13)]
    expected = [45000, 44500, 44000, 43500, 43000, 42500, 42000, 41500, 41000, 40500, 40000, 39500]
    actual = [45200, 44800, 44200, 43800, 43200, 42800, 42300, 41800, 41200, 40800, 40200, 39800]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=expected, name="Expected Interest", fill="tozeroy", line=dict(color=COLORS[0])))
    fig.add_trace(go.Scatter(x=months, y=actual, name="Actual Interest", fill="tozeroy", line=dict(color=COLORS[1])))
    return apply_layout(fig, "Interest Comparison")


def network_graph_plotly(G, pos: dict) -> go.Figure:
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color="#38bdf8"), hoverinfo="none", mode="lines")
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    node_text = list(G.nodes())
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=node_text,
        textposition="top center", hoverinfo="text",
        marker=dict(size=18, color=COLORS[0], line=dict(width=2, color="white")),
    )
    fig = go.Figure(data=[edge_trace, node_trace])
    return apply_layout(fig, "Transaction Relationship Graph")


def amortization_chart(schedule: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=schedule["month"], y=schedule["principal"], name="Principal", marker_color=COLORS[0]))
    fig.add_trace(go.Bar(x=schedule["month"], y=schedule["interest"], name="Interest", marker_color=COLORS[4]))
    fig.update_layout(barmode="stack")
    return apply_layout(fig, "Amortization Schedule")


def risk_heatmap() -> go.Figure:
    categories = ["Round-Tripping", "Charges", "Interest", "Idle Balance", "Signatory"]
    severity = ["Critical", "High", "Medium", "Low"]
    import numpy as np
    z = np.array([[3, 5, 2, 1], [4, 3, 6, 2], [2, 4, 3, 5], [1, 2, 4, 3], [5, 3, 2, 4]])
    fig = go.Figure(data=go.Heatmap(z=z, x=severity, y=categories, colorscale="RdYlGn_r", showscale=True))
    return apply_layout(fig, "Risk Heatmap")
