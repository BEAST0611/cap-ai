"""Idle Balance Detection module."""

import streamlit as st
import pandas as pd
from pathlib import Path

from utils.calculations import detect_idle_accounts
from utils.data_table import render_data_table
from utils.ui import render_ai_insights, render_header


def render():
    render_header("Idle Balance Detection", "Identify idle funds and sweep opportunities")

    sample = Path(__file__).resolve().parent.parent / "assets" / "sample_data" / "idle_accounts_sample.csv"
    use_sample = st.checkbox("Use sample idle account data", value=True)

    if use_sample and sample.exists():
        df = pd.read_csv(sample)
    else:
        st.markdown("#### Manual Entry")
        df = pd.DataFrame([{
            "account_number": st.text_input("Account", "ACC1001"),
            "balance": st.number_input("Balance", value=2500000),
            "last_transaction_date": st.text_input("Last Txn Date", "2024-06-15"),
            "minimum_balance": st.number_input("Min Balance", value=100000),
            "sweep_facility": st.selectbox("Sweep", ["No", "Yes"]),
        }])

    if st.button("🔍 Detect Idle Accounts", type="primary"):
        results = detect_idle_accounts(df)
        idle = results[results["is_idle"]]

        c1, c2, c3 = st.columns(3)
        c1.metric("Idle Accounts", len(idle))
        c2.metric("Total Opportunity Loss", f"₹{results['opportunity_loss'].sum():,.0f}")
        c3.metric("Highest Priority", results["priority_score"].max())

        render_data_table(results.sort_values("priority_score", ascending=False), key="idle_result")

        if not idle.empty:
            st.warning(f"⚠️ {len(idle)} account(s) with significant idle balances")

        render_ai_insights(
            summary=f"Analyzed {len(df)} accounts. {len(idle)} require action.",
            risk=f"Estimated opportunity loss: ₹{results['opportunity_loss'].sum():,.0f} from uninvested idle funds.",
            actions=["Enable auto-sweep facility", "Review treasury investment policy", "Notify relationship managers"],
            priority="Medium" if len(idle) > 0 else "Low",
        )
