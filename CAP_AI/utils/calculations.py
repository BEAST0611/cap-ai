"""Audit calculation engines for all CAP AI modules."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd


# ── Round-Tripping Detection ──────────────────────────────────────────────

def detect_round_tripping(df: pd.DataFrame) -> dict:
    """Detect circular fund movements and suspicious patterns."""
    G = nx.DiGraph()
    alerts = []
    risk_scores = []

    for _, row in df.iterrows():
        src = str(row.get("account_number", ""))
        dst = str(row.get("counterparty", ""))
        amt = float(row.get("credit", 0) or row.get("debit", 0) or 0)
        if src and dst and amt > 0:
            G.add_edge(src, dst, weight=amt, date=str(row.get("date", "")))

    # Circular paths (length 3-5)
    cycles = []
    for length in range(3, 6):
        for combo in combinations(G.nodes(), length):
            sub = G.subgraph(combo)
            if nx.is_strongly_connected(sub) and len(sub.edges()) >= length:
                cycles.append(list(combo))

    for cycle in cycles[:20]:
        alerts.append({
            "type": "Circular Movement",
            "accounts": " → ".join(cycle),
            "risk_score": min(95, 60 + len(cycle) * 8),
            "severity": "Critical" if len(cycle) >= 4 else "High",
        })

    # Same amount repeated
    if "credit" in df.columns or "debit" in df.columns:
        amt_col = "credit" if "credit" in df.columns else "debit"
        amounts = df[amt_col].dropna()
        dup_amts = amounts[amounts.duplicated(keep=False)].unique()
        for amt in dup_amts[:10]:
            count = (amounts == amt).sum()
            if count >= 3:
                alerts.append({
                    "type": "Repeated Amount",
                    "accounts": f"Amount ₹{amt:,.0f} × {count}",
                    "risk_score": min(85, 40 + count * 10),
                    "severity": "High" if count >= 5 else "Medium",
                })

    # Money returning to origin
    for node in G.nodes():
        for neighbor in G.successors(node):
            if G.has_edge(neighbor, node):
                alerts.append({
                    "type": "Return to Origin",
                    "accounts": f"{node} ↔ {neighbor}",
                    "risk_score": 75,
                    "severity": "High",
                })

    pos = nx.spring_layout(G, seed=42) if G.number_of_nodes() > 0 else {}
    overall = min(100, len(alerts) * 12 + G.number_of_edges() * 2) if alerts else 15

    return {
        "graph": G,
        "positions": pos,
        "alerts": pd.DataFrame(alerts) if alerts else pd.DataFrame(columns=["type", "accounts", "risk_score", "severity"]),
        "overall_risk": overall,
        "cluster_count": len(cycles),
    }


# ── Bank Charges ──────────────────────────────────────────────────────────

CHARGE_RULES = {
    "Savings": {"atm_free": 5, "atm_charge": 21, "neft": 0, "rtgs": 0, "sms": 15, "maintenance": 0},
    "Current": {"atm_free": 0, "atm_charge": 25, "neft": 5, "rtgs": 25, "sms": 25, "maintenance": 500},
    "Premium": {"atm_free": 10, "atm_charge": 15, "neft": 0, "rtgs": 0, "sms": 0, "maintenance": 0},
}


def recompute_bank_charges(
    account_type: str,
    sanctioned: dict[str, float],
    actual: dict[str, float],
    txn_count: dict[str, int],
) -> pd.DataFrame:
    """Recalculate expected vs actual bank charges."""
    rules = CHARGE_RULES.get(account_type, CHARGE_RULES["Savings"])
    rows = []
    for charge_type in set(list(sanctioned.keys()) + list(actual.keys())):
        sanc = sanctioned.get(charge_type, rules.get(charge_type, 0))
        act = actual.get(charge_type, 0)
        count = txn_count.get(charge_type, 1)
        if charge_type == "atm_charge":
            free = rules.get("atm_free", 0)
            expected = max(0, count - free) * sanc
        else:
            expected = sanc * count if sanc < 100 else sanc
        variance = act - expected
        flag = "Overcharge" if variance > 0 else ("Undercharge" if variance < 0 else "OK")
        rows.append({
            "charge_type": charge_type,
            "expected": round(expected, 2),
            "actual": round(act, 2),
            "variance": round(variance, 2),
            "txn_count": count,
            "flag": flag,
        })
    return pd.DataFrame(rows)


# ── Interest Verification ───────────────────────────────────────────────────

def compute_emi(principal: float, rate: float, tenure_months: int) -> float:
    """Standard reducing balance EMI."""
    r = rate / 12 / 100
    if r == 0:
        return principal / tenure_months
    return principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)


def verify_interest(
    loan_amount: float,
    rate: float,
    tenure: int,
    emi: float,
    actual_interest: float,
) -> dict:
    """Verify interest calculations and build amortization."""
    expected_emi = compute_emi(loan_amount, rate, tenure)
    schedule = []
    balance = loan_amount
    r = rate / 12 / 100
    total_interest = 0.0
    for m in range(1, tenure + 1):
        interest = balance * r
        principal_part = expected_emi - interest
        balance = max(0, balance - principal_part)
        total_interest += interest
        schedule.append({
            "month": m,
            "emi": round(expected_emi, 2),
            "principal": round(principal_part, 2),
            "interest": round(interest, 2),
            "balance": round(balance, 2),
        })
    variance = actual_interest - total_interest
    return {
        "expected_emi": round(expected_emi, 2),
        "expected_total_interest": round(total_interest, 2),
        "variance": round(variance, 2),
        "variance_pct": round(abs(variance) / total_interest * 100, 2) if total_interest else 0,
        "status": "Excess Interest" if variance > 100 else ("Short Interest" if variance < -100 else "Correct"),
        "schedule": pd.DataFrame(schedule),
    }


# ── Idle Balance ──────────────────────────────────────────────────────────

def detect_idle_accounts(df: pd.DataFrame) -> pd.DataFrame:
    """Flag idle balances and sweep opportunities."""
    today = datetime.now()
    results = []
    for _, row in df.iterrows():
        balance = float(row.get("balance", 0))
        last_txn = row.get("last_transaction_date")
        min_bal = float(row.get("minimum_balance", 10000))
        sweep = str(row.get("sweep_facility", "No")).lower() in ("yes", "true", "1")

        try:
            last_date = pd.to_datetime(last_txn)
            days_idle = (today - last_date).days
        except Exception:
            days_idle = 999

        idle = days_idle > 90 and balance > min_bal * 2
        opp_loss = balance * divmod(days_idle, 365)[0] * 0.07 if idle else 0
        priority = min(100, int(days_idle / 3 + balance / 100000))

        rec = []
        if idle and not sweep:
            rec.append("Enable auto-sweep to liquid fund")
        if idle:
            rec.append("Review investment mandate")
        if days_idle > 180:
            rec.append("Escalate to treasury team")

        results.append({
            "account": row.get("account_number", ""),
            "balance": balance,
            "days_idle": days_idle,
            "is_idle": idle,
            "opportunity_loss": round(opp_loss, 2),
            "priority_score": priority,
            "recommendation": "; ".join(rec) if rec else "No action required",
        })
    return pd.DataFrame(results)


# ── Signatory Verification ────────────────────────────────────────────────

def verify_signatories(master: pd.DataFrame, approvals: pd.DataFrame) -> dict:
    """Compare approval log against authorised signatory master."""
    mismatches = []
    today = datetime.now()

    master_cols = {c.lower(): c for c in master.columns}
    appr_cols = {c.lower(): c for c in approvals.columns}

    name_col = master_cols.get("name") or master_cols.get("signatory_name") or master.columns[0]
    auth_col = master_cols.get("authorised") or master_cols.get("status")
    expiry_col = master_cols.get("expiry_date") or master_cols.get("valid_until")
    appr_by = appr_cols.get("approved_by") or appr_cols.get("approver") or approvals.columns[-1]

    authorised = set()
    expired = set()
    for _, row in master.iterrows():
        name = str(row[name_col]).strip().lower()
        if auth_col and str(row.get(auth_col, "")).lower() in ("yes", "active", "authorised"):
            if expiry_col:
                try:
                    exp = pd.to_datetime(row[expiry_col])
                    if exp < today:
                        expired.add(name)
                        continue
                except Exception:
                    pass
            authorised.add(name)

    for _, row in approvals.iterrows():
        approver = str(row[appr_by]).strip().lower()
        if approver in expired:
            mismatches.append({"approver": approver, "issue": "Expired Authorisation", "severity": "Critical"})
        elif approver not in authorised:
            mismatches.append({"approver": approver, "issue": "Not Authorised", "severity": "High"})

    dup_mask = approvals.duplicated(subset=[appr_by], keep=False)
    for approver in approvals.loc[dup_mask, appr_by].unique():
        mismatches.append({"approver": str(approver), "issue": "Duplicate Approval Pattern", "severity": "Medium"})

    mismatch_df = pd.DataFrame(mismatches) if mismatches else pd.DataFrame(columns=["approver", "issue", "severity"])
    risk = min(100, len(mismatches) * 15 + len(expired) * 10)

    return {
        "mismatches": mismatch_df,
        "expired_count": len(expired),
        "unauthorised_count": sum(1 for m in mismatches if m["issue"] == "Not Authorised"),
        "risk_score": risk,
        "authorised_count": len(authorised),
    }


# ── Dashboard KPIs ────────────────────────────────────────────────────────

def get_dashboard_kpis() -> dict[str, int | float]:
    """Sample KPI values for dashboard."""
    return {
        "total_accounts": 1247,
        "transactions_processed": 45892,
        "risk_alerts": 23,
        "potential_frauds": 7,
        "interest_variance": 125000,
        "charge_variance": 34500,
        "idle_accounts": 18,
        "signatory_mismatches": 4,
    }
