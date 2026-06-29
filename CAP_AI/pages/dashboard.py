"""Dashboard page — KPIs, charts, risk heatmap."""

import streamlit as st
import pandas as pd

from utils.calculations import get_dashboard_kpis
from utils.charts import (
    bank_charges_chart,
    fraud_trend_chart,
    interest_comparison_chart,
    risk_distribution_chart,
    risk_heatmap,
    transaction_volume_chart,
)
from utils.ui import render_ai_insights, render_header, render_kpi_row


def render():
    render_header("Dashboard", "Real-time audit intelligence overview")
    kpis = get_dashboard_kpis()

    render_kpi_row([
        ("Total Accounts", f"{kpis['total_accounts']:,}", "🏦"),
        ("Transactions", f"{kpis['transactions_processed']:,}", "💳"),
        ("Risk Alerts", kpis["risk_alerts"], "⚠️"),
        ("Potential Frauds", kpis["potential_frauds"], "🚨"),
    ])
    render_kpi_row([
        ("Interest Variance", f"₹{kpis['interest_variance']:,}", "💰"),
        ("Charge Variance", f"₹{kpis['charge_variance']:,}", "📊"),
        ("Idle Accounts", kpis["idle_accounts"], "😴"),
        ("Signatory Issues", kpis["signatory_mismatches"], "👤"),
    ])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(transaction_volume_chart(pd.DataFrame()), use_container_width=True)
    with c2:
        st.plotly_chart(risk_distribution_chart(), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(fraud_trend_chart(), use_container_width=True)
    with c4:
        st.plotly_chart(bank_charges_chart(), use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(interest_comparison_chart(), use_container_width=True)
    with c6:
        st.plotly_chart(risk_heatmap(), use_container_width=True)

    render_ai_insights(
        summary="Platform monitoring 1,247 accounts with 23 active risk alerts. 7 potential fraud patterns require immediate review.",
        risk="Elevated round-tripping activity detected in 3 account clusters. Interest variance exceeds ₹1.25L threshold.",
        actions=[
            "Review 7 flagged fraud cases in Round-Tripping module",
            "Investigate charge overbilling on Current accounts",
            "Enable sweep on 18 idle accounts",
            "Resolve 4 signatory mismatches before month-end",
        ],
        priority="High",
        next_steps=["Open Reports for executive summary", "Assign auditors to critical alerts"],
    )
