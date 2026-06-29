"""Data validation, duplicate detection, and missing value analysis."""

from __future__ import annotations

import pandas as pd


def detect_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing value summary per column."""
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    return pd.DataFrame({"column": missing.index, "missing_count": missing.values, "missing_pct": pct.values})


def detect_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Return duplicate rows."""
    if subset:
        mask = df.duplicated(subset=subset, keep=False)
    else:
        mask = df.duplicated(keep=False)
    return df[mask].copy()


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric summary stats."""
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return pd.DataFrame()
    return numeric.describe().T.reset_index().rename(columns={"index": "column"})


def validate_transaction_columns(df: pd.DataFrame) -> dict[str, str | bool]:
    """Check required columns for round-tripping module."""
    required = ["account_number", "transaction_id", "debit", "credit", "date", "counterparty", "reference_number"]
    mapping = {}
    cols_lower = {c.lower().replace(" ", "_"): c for c in df.columns}
    for req in required:
        found = cols_lower.get(req) or cols_lower.get(req.replace("_", ""))
        mapping[req] = found if found else None
    mapping["valid"] = all(mapping[r] for r in required)
    return mapping


def auto_map_columns(df: pd.DataFrame) -> dict[str, str]:
    """Suggest column mapping from uploaded file."""
    aliases = {
        "account_number": ["account", "acct", "account_no", "account_number"],
        "transaction_id": ["txn_id", "transaction_id", "trans_id", "id"],
        "debit": ["debit", "dr", "withdrawal"],
        "credit": ["credit", "cr", "deposit"],
        "date": ["date", "txn_date", "transaction_date", "value_date"],
        "counterparty": ["counterparty", "party", "beneficiary", "payee"],
        "reference_number": ["reference", "ref", "reference_number", "utr"],
    }
    cols_norm = {c.lower().replace(" ", "_"): c for c in df.columns}
    result = {}
    for target, names in aliases.items():
        for n in names:
            if n in cols_norm:
                result[target] = cols_norm[n]
                break
    return result


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: strip strings, fill numeric NaN with 0."""
    cleaned = df.copy()
    for col in cleaned.select_dtypes(include="object").columns:
        cleaned[col] = cleaned[col].astype(str).str.strip()
    for col in cleaned.select_dtypes(include="number").columns:
        cleaned[col] = cleaned[col].fillna(0)
    return cleaned
