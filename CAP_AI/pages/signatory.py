"""Authorised Signatory Verification module."""

import streamlit as st
import pandas as pd
from pathlib import Path

from utils.calculations import verify_signatories
from utils.data_table import render_data_table
from utils.ui import render_ai_insights, render_header


def render():
    render_header("Authorised Signatory Verification", "Compare approvals against signatory master")

    base = Path(__file__).resolve().parent.parent / "assets" / "sample_data"
    use_sample = st.checkbox("Use sample signatory data", value=True)

    if use_sample:
        master = pd.read_csv(base / "signatory_master.csv") if (base / "signatory_master.csv").exists() else _default_master()
        approvals = pd.read_csv(base / "approval_log.csv") if (base / "approval_log.csv").exists() else _default_approvals()
    else:
        f1 = st.file_uploader("Authorised Signatory Master", type=["csv", "xlsx"], key="sig_master")
        f2 = st.file_uploader("Transaction Approval Log", type=["csv", "xlsx"], key="sig_appr")
        if not f1 or not f2:
            st.info("Upload both files or use sample data.")
            return
        master = pd.read_csv(f1) if f1.name.endswith(".csv") else pd.read_excel(f1)
        approvals = pd.read_csv(f2) if f2.name.endswith(".csv") else pd.read_excel(f2)

    st.markdown("#### Signatory Master Preview")
    render_data_table(master, key="master_preview", height=200, enable_export=False)

    if st.button("✅ Verify Signatories", type="primary"):
        result = verify_signatories(master, approvals)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Risk Score", f"{result['risk_score']}/100")
        c2.metric("Authorised", result["authorised_count"])
        c3.metric("Expired", result["expired_count"])
        c4.metric("Unauthorised", result["unauthorised_count"])

        if not result["mismatches"].empty:
            st.error("🚨 Mismatch Report")
            render_data_table(result["mismatches"], key="sig_mismatch")
        else:
            st.success("All approvals verified against authorised signatory list.")

        st.markdown("#### Approval Matrix")
        matrix = pd.crosstab(approvals.iloc[:, -1], columns="count") if len(approvals) else pd.DataFrame()
        if matrix.empty:
            appr_col = approvals.columns[-1]
            counts = approvals[appr_col].value_counts().reset_index()
            counts.columns = ["Approver", "Approval Count"]
            render_data_table(counts, key="appr_matrix")

        render_ai_insights(
            summary=f"Verified {len(approvals)} approvals against {result['authorised_count']} authorised signatories.",
            risk=f"{len(result['mismatches'])} mismatch(es). Risk score: {result['risk_score']}/100.",
            actions=["Revoke expired authorisations", "Block unauthorised approvers", "Update signatory master"],
            priority="High" if result["risk_score"] > 50 else "Medium",
        )


def _default_master() -> pd.DataFrame:
    return pd.DataFrame([
        {"name": "Rajesh Kumar", "status": "Active", "expiry_date": "2026-12-31"},
        {"name": "Priya Sharma", "status": "Active", "expiry_date": "2026-06-30"},
        {"name": "Amit Patel", "status": "Expired", "expiry_date": "2024-01-15"},
    ])


def _default_approvals() -> pd.DataFrame:
    return pd.DataFrame([
        {"txn_id": "TXN001", "amount": 500000, "approved_by": "Rajesh Kumar"},
        {"txn_id": "TXN002", "amount": 1200000, "approved_by": "Amit Patel"},
        {"txn_id": "TXN003", "amount": 750000, "approved_by": "Unknown Person"},
        {"txn_id": "TXN004", "amount": 300000, "approved_by": "Priya Sharma"},
        {"txn_id": "TXN005", "amount": 900000, "approved_by": "Priya Sharma"},
    ])
