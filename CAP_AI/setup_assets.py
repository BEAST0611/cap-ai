from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
(ROOT / "assets" / "css").mkdir(parents=True, exist_ok=True)

css = """
.stApp { background: linear-gradient(135deg, #0a1628, #1e3a5f) !important; font-family: Inter, sans-serif !important; color: #e2e8f0 !important; }
#MainMenu, footer, header { visibility: hidden; }
.glass-card { background: rgba(15,39,68,0.65); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.kpi-card { background: linear-gradient(145deg, rgba(14,165,233,0.12), rgba(15,39,68,0.8)); border: 1px solid rgba(14,165,233,0.25); border-radius: 16px; padding: 1.25rem; text-align: center; }
.kpi-value { font-size: 2rem; font-weight: 800; color: #38bdf8; }
.kpi-label { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; }
.cap-header { background: rgba(10,22,40,0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 0.75rem 1.5rem; margin-bottom: 1.5rem; }
.login-container { max-width: 420px; margin: 2rem auto; background: rgba(15,39,68,0.65); border-radius: 24px; padding: 2rem; border: 1px solid rgba(255,255,255,0.12); }
.login-title { text-align: center; font-size: 1.75rem; font-weight: 700; color: #38bdf8; }
.ai-insight-box { background: rgba(14,165,233,0.08); border-left: 4px solid #0ea5e9; border-radius: 0 16px 16px 0; padding: 1.25rem; margin: 1rem 0; }
.priority-high { border-left-color: #ef4444 !important; }
.stButton > button { background: linear-gradient(135deg, #0ea5e9, #0284c7) !important; color: white !important; border-radius: 10px !important; }
"""
(ROOT / "assets" / "css" / "theme.css").write_text(css.strip(), encoding="utf-8")

sd = ROOT / "assets" / "sample_data"
sd.mkdir(parents=True, exist_ok=True)

pd.DataFrame([
    {"account_number": "ACC001", "transaction_id": "T1", "debit": 0, "credit": 500000, "date": "2025-01-05", "counterparty": "ACC002", "reference_number": "REF001"},
    {"account_number": "ACC002", "transaction_id": "T2", "debit": 0, "credit": 500000, "date": "2025-01-06", "counterparty": "ACC003", "reference_number": "REF002"},
    {"account_number": "ACC003", "transaction_id": "T3", "debit": 0, "credit": 500000, "date": "2025-01-07", "counterparty": "ACC001", "reference_number": "REF003"},
]).to_csv(sd / "transactions_sample.csv", index=False)

pd.DataFrame([
    {"account_number": "ACC1001", "balance": 2500000, "last_transaction_date": "2024-06-15", "minimum_balance": 100000, "sweep_facility": "No"},
    {"account_number": "ACC1003", "balance": 5200000, "last_transaction_date": "2023-11-01", "minimum_balance": 200000, "sweep_facility": "No"},
]).to_csv(sd / "idle_accounts_sample.csv", index=False)

pd.DataFrame([
    {"name": "Rajesh Kumar", "status": "Active", "expiry_date": "2026-12-31"},
    {"name": "Amit Patel", "status": "Expired", "expiry_date": "2024-01-15"},
]).to_csv(sd / "signatory_master.csv", index=False)

pd.DataFrame([
    {"txn_id": "TXN001", "amount": 500000, "approved_by": "Rajesh Kumar"},
    {"txn_id": "TXN002", "amount": 1200000, "approved_by": "Amit Patel"},
]).to_csv(sd / "approval_log.csv", index=False)

try:
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (400, 400), (10, 22, 40, 255))
    d = ImageDraw.Draw(img)
    d.ellipse([50, 50, 350, 350], outline=(14, 165, 233, 255), width=8)
    d.text((200, 170), "CAP", fill=(56, 189, 248, 255), anchor="mm")
    d.text((200, 280), "AI AUDIT", fill=(148, 163, 184, 255), anchor="mm")
    img.save(ROOT / "assets" / "logo.png")
except Exception as exc:
    print("Logo skip:", exc)

print("Assets created.")
