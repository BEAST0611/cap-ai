"""Reports generation and export."""

import streamlit as st

from utils.calculations import get_dashboard_kpis
from utils.charts import bank_charges_chart, fraud_trend_chart, risk_distribution_chart
from utils.exporters import to_excel_bytes, to_pdf_report, to_word_report
from utils.ui import render_header


def render():
    render_header("Reports", "Executive summaries and exportable audit findings")
    kpis = get_dashboard_kpis()

    st.markdown("### Executive Summary")
    st.markdown(
        f"""
        <div class="glass-card">
        <p><strong>Audit Period:</strong> Q4 FY2025</p>
        <p><strong>Accounts Audited:</strong> {kpis['total_accounts']:,}</p>
        <p><strong>Transactions Reviewed:</strong> {kpis['transactions_processed']:,}</p>
        <p><strong>Critical Findings:</strong> {kpis['potential_frauds']} potential fraud cases, 
        {kpis['risk_alerts']} risk alerts, ₹{kpis['interest_variance']:,} interest variance, 
        ₹{kpis['charge_variance']:,} charge variance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(risk_distribution_chart(), use_container_width=True)
    with c2:
        st.plotly_chart(fraud_trend_chart(), use_container_width=True)
    st.plotly_chart(bank_charges_chart(), use_container_width=True)

    st.markdown("### Risk Matrix")
    import pandas as pd
    matrix = pd.DataFrame({
        "Module": ["Round-Tripping", "Bank Charges", "Interest", "Idle Balance", "Signatory"],
        "Risk Level": ["Critical", "High", "Medium", "Medium", "High"],
        "Findings": [7, 12, 5, 18, 4],
        "Financial Impact (₹)": [2500000, 34500, 125000, 890000, 0],
    })
    st.dataframe(matrix, use_container_width=True)

    st.markdown("### Recommendations")
    for i, rec in enumerate([
        "Immediate investigation of 7 round-tripping cases",
        "Dispute ₹34,500 in overcharged bank fees",
        "Enable sweep on 18 idle accounts (₹8.9L opportunity loss)",
        "Update signatory master and revoke expired authorisations",
        "Schedule quarterly re-audit for high-risk accounts",
    ], 1):
        st.markdown(f"{i}. {rec}")

    st.markdown("---")
    st.markdown("### Export Report")
    sections = [
        ("Executive Summary", f"Audited {kpis['total_accounts']} accounts with {kpis['risk_alerts']} alerts."),
        ("Detailed Findings", f"{kpis['potential_frauds']} fraud cases, ₹{kpis['charge_variance']:,} charge variance."),
        ("Recommendations", "See risk matrix and action items above."),
    ]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📄 PDF Report", to_pdf_report("CAP AI Audit Report", sections, matrix), "audit_report.pdf", "application/pdf")
    with c2:
        st.download_button("📊 Excel Report", to_excel_bytes(matrix), "audit_report.xlsx", "application/vnd.ms-excel")
    with c3:
        st.download_button("📝 Word Report", to_word_report("CAP AI Audit Report", sections), "audit_report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
