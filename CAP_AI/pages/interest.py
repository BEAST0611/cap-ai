"""Interest Verification module."""

import streamlit as st

from utils.calculations import verify_interest
from utils.charts import amortization_chart
from utils.data_table import render_data_table
from utils.ui import render_ai_insights, render_header


def render():
    render_header("Interest Verification", "Validate loan interest calculations and EMI")

    c1, c2 = st.columns(2)
    with c1:
        loan_amount = st.number_input("Loan Amount (₹)", value=5000000, step=100000)
        rate = st.number_input("Interest Rate (% p.a.)", value=8.5, step=0.1)
    with c2:
        tenure = st.number_input("Tenure (months)", value=240, step=12)
        emi = st.number_input("Declared EMI (₹)", value=43391, step=100)
        actual_interest = st.number_input("Actual Interest Paid (₹)", value=5415000, step=10000)

    if st.button("📊 Verify Interest", type="primary"):
        result = verify_interest(loan_amount, rate, tenure, emi, actual_interest)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Expected EMI", f"₹{result['expected_emi']:,.2f}")
        c2.metric("Expected Total Interest", f"₹{result['expected_total_interest']:,.2f}")
        c3.metric("Variance", f"₹{result['variance']:,.2f}")
        c4.metric("Status", result["status"])

        if result["status"] != "Correct":
            st.warning(f"⚠️ {result['status']}: Variance of ₹{abs(result['variance']):,.2f} ({result['variance_pct']}%)")

        st.plotly_chart(amortization_chart(result["schedule"]), use_container_width=True)
        st.markdown("### Amortization Schedule")
        render_data_table(result["schedule"], key="amort", height=350)

        render_ai_insights(
            summary=f"Loan verification for ₹{loan_amount:,.0f} at {rate}% over {tenure} months.",
            risk=f"Interest {result['status'].lower()}. Variance: ₹{result['variance']:,.2f}.",
            actions=["Request revised amortization from bank", "Compare with RBI fair practice code", "Escalate if excess exceeds 1%"],
            priority="High" if abs(result["variance"]) > 50000 else "Low",
        )
