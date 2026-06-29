"""Bank Charges Verification module."""

import streamlit as st
import pandas as pd

from utils.calculations import recompute_bank_charges
from utils.data_table import render_data_table
from utils.ui import render_ai_insights, render_header


def render():
    render_header("Bank Charges Verification", "Recalculate expected charges and detect overbilling")

    account_type = st.selectbox("Account Type", ["Savings", "Current", "Premium"])
    st.markdown("#### Sanctioned vs Actual Charges")

    charge_types = ["atm_charge", "neft", "rtgs", "sms", "maintenance"]
    sanctioned, actual, txn_count = {}, {}, {}

    cols = st.columns(3)
    for i, ct in enumerate(charge_types):
        with cols[i % 3]:
            st.markdown(f"**{ct.replace('_', ' ').title()}**")
            sanctioned[ct] = st.number_input(f"Sanctioned ₹", value=21.0 if ct == "atm_charge" else 15.0, key=f"s_{ct}")
            actual[ct] = st.number_input(f"Actual ₹", value=25.0 if ct == "atm_charge" else 18.0, key=f"a_{ct}")
            txn_count[ct] = st.number_input("Txn Count", value=12 if ct == "atm_charge" else 5, key=f"t_{ct}")

    if st.button("🔄 Recompute Charges", type="primary"):
        result = recompute_bank_charges(account_type, sanctioned, actual, txn_count)
        total_var = result["variance"].sum()
        over = (result["flag"] == "Overcharge").sum()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Variance", f"₹{total_var:,.2f}")
        c2.metric("Overcharge Items", over)
        c3.metric("Risk Flag", "HIGH" if total_var > 500 else "LOW")

        st.markdown("### Difference Table")
        render_data_table(result, key="charges_result")

        flags = result[result["flag"] != "OK"]
        if not flags.empty:
            st.error(f"⚠️ {len(flags)} charge type(s) with variance detected")

        render_ai_insights(
            summary=f"{account_type} account charge analysis complete. Total variance: ₹{total_var:,.2f}.",
            risk=f"{over} overcharge instances detected." if over else "Charges within acceptable limits.",
            actions=["Dispute overcharged items with bank", "Update sanctioned charge schedule", "Request refund for excess charges"],
            priority="High" if total_var > 1000 else "Medium",
        )
