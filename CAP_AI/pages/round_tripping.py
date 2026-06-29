"""Fund Round-Tripping Detection module."""

import streamlit as st
import pandas as pd
import networkx as nx

from utils.calculations import detect_round_tripping
from utils.charts import network_graph_plotly
from utils.data_table import render_data_table
from utils.ui import render_ai_insights, render_header
from utils.validators import auto_map_columns, validate_transaction_columns


def render():
    render_header("Fund Round-Tripping Detection", "Identify circular money movement and suspicious clusters")

    df = st.session_state.get("uploaded_data")
    use_sample = st.checkbox("Use sample transaction data", value=df is None)

    if use_sample:
        sample = __import__("pathlib").Path(__file__).resolve().parent.parent / "assets" / "sample_data" / "transactions_sample.csv"
        if sample.exists():
            df = pd.read_csv(sample)
        else:
            df = _generate_sample()

    if df is None:
        st.warning("Upload transaction data via Upload Excel page, or enable sample data.")
        return

    mapping = auto_map_columns(df)
    std_df = pd.DataFrame()
    for std, col in mapping.items():
        if col:
            std_df[std] = df[col]
    for c in ["account_number", "transaction_id", "debit", "credit", "date", "counterparty", "reference_number"]:
        if c not in std_df.columns:
            std_df[c] = df.iloc[:, 0] if len(df.columns) else ""

    validation = validate_transaction_columns(std_df)
    if not validation.get("valid"):
        st.warning("Some columns could not be mapped. Results may be limited.")

    if st.button("🔍 Run Detection Analysis", type="primary"):
        with st.spinner("Analyzing transaction graph..."):
            result = detect_round_tripping(std_df)

        st.metric("Overall Risk Score", f"{result['overall_risk']}/100")
        st.metric("Suspicious Clusters", result["cluster_count"])

        if not result["alerts"].empty:
            st.markdown("### 🚨 Red Alerts")
            render_data_table(result["alerts"], key="rt_alerts", height=300)

        G = result["graph"]
        if G.number_of_nodes() > 0:
            st.markdown("### 🔗 Transaction Relationship Graph")
            pos = result["positions"]
            st.plotly_chart(network_graph_plotly(G, pos), use_container_width=True)

            st.markdown("### Network Statistics")
            c1, c2, c3 = st.columns(3)
            c1.metric("Nodes (Accounts)", G.number_of_nodes())
            c2.metric("Edges (Transfers)", G.number_of_edges())
            c3.metric("Density", f"{nx.density(G):.3f}" if G.number_of_nodes() > 1 else "N/A")

        priority = "High" if result["overall_risk"] > 60 else "Medium"
        render_ai_insights(
            summary=f"Analysis of {len(std_df)} transactions found {len(result['alerts'])} suspicious patterns.",
            risk=f"Overall risk score: {result['overall_risk']}/100. Circular movements indicate potential round-tripping.",
            actions=["Freeze flagged account clusters", "Request counterparty KYC", "Escalate to compliance team"],
            priority=priority,
            next_steps=["Export alert table", "Cross-reference with signatory approvals"],
        )


def _generate_sample() -> pd.DataFrame:
    return pd.DataFrame([
        {"account_number": "ACC001", "transaction_id": "T1", "debit": 0, "credit": 500000, "date": "2025-01-05", "counterparty": "ACC002", "reference_number": "REF001"},
        {"account_number": "ACC002", "transaction_id": "T2", "debit": 0, "credit": 500000, "date": "2025-01-06", "counterparty": "ACC003", "reference_number": "REF002"},
        {"account_number": "ACC003", "transaction_id": "T3", "debit": 0, "credit": 500000, "date": "2025-01-07", "counterparty": "ACC001", "reference_number": "REF003"},
        {"account_number": "ACC001", "transaction_id": "T4", "debit": 0, "credit": 100000, "date": "2025-02-01", "counterparty": "ACC004", "reference_number": "REF004"},
        {"account_number": "ACC004", "transaction_id": "T5", "debit": 0, "credit": 100000, "date": "2025-02-02", "counterparty": "ACC001", "reference_number": "REF005"},
    ])
