"""Excel/CSV upload and data preview."""

import streamlit as st
import pandas as pd

from utils.auth import add_notification, log_audit
from utils.data_table import render_data_table
from utils.exporters import to_csv_bytes, to_excel_bytes
from utils.ui import render_ai_insights, render_header
from utils.validators import auto_map_columns, clean_dataset, detect_duplicates, detect_missing, summary_statistics


def render():
    render_header("Upload Excel", "Import and validate audit datasets")
    files = st.file_uploader(
        "Upload Excel (.xlsx) or CSV files",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True,
    )

    if not files:
        st.info("📁 Drag and drop files or use sample data from assets/sample_data/")
        sample_path = __import__("pathlib").Path(__file__).resolve().parent.parent / "assets" / "sample_data" / "transactions_sample.csv"
        if sample_path.exists():
            if st.button("Load Sample Transactions"):
                df = pd.read_csv(sample_path)
                st.session_state.uploaded_data = df
                add_notification("Sample data loaded", "success")
                st.rerun()
        return

    all_dfs = []
    for f in files:
        try:
            if f.name.endswith(".csv"):
                df = pd.read_csv(f)
            else:
                df = pd.read_excel(f)
            all_dfs.append(df)
            recent = st.session_state.get("recent_uploads", [])
            recent.insert(0, {"name": f.name, "rows": len(df), "cols": len(df.columns)})
            st.session_state.recent_uploads = recent[:10]
            log_audit("UPLOAD", f"File {f.name} — {len(df)} rows")
        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    if not all_dfs:
        return

    df = pd.concat(all_dfs, ignore_index=True) if len(all_dfs) > 1 else all_dfs[0]
    st.session_state.uploaded_data = df
    add_notification(f"Loaded {len(df)} records from {len(files)} file(s)", "success")

    st.success(f"✅ Loaded **{len(df)}** rows × **{len(df.columns)}** columns")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Preview", "Column Mapping", "Missing Values", "Duplicates", "Statistics"])

    with tab1:
        render_data_table(df.head(500), key="upload_preview")

    with tab2:
        mapping = auto_map_columns(df)
        st.json(mapping)
        st.dataframe(pd.DataFrame(list(mapping.items()), columns=["Standard Field", "Mapped Column"]))

    with tab3:
        missing = detect_missing(df)
        if missing["missing_count"].sum() == 0:
            st.success("No missing values detected.")
        else:
            st.warning(f"Found missing values in {(missing['missing_count'] > 0).sum()} columns")
            st.dataframe(missing[missing["missing_count"] > 0])

    with tab4:
        dupes = detect_duplicates(df)
        st.metric("Duplicate Rows", len(dupes))
        if len(dupes):
            render_data_table(dupes, key="dupes")

    with tab5:
        stats = summary_statistics(df)
        if not stats.empty:
            st.dataframe(stats)

    cleaned = clean_dataset(df)
    st.markdown("### Download Cleaned Dataset")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Cleaned Excel", to_excel_bytes(cleaned), "cleaned_data.xlsx", key="dl_clean_xlsx")
    with c2:
        st.download_button("📥 Cleaned CSV", to_csv_bytes(cleaned), "cleaned_data.csv", key="dl_clean_csv")

    render_ai_insights(
        summary=f"Dataset contains {len(df)} records with {len(df.columns)} fields. Quality check complete.",
        risk=f"{len(dupes)} duplicate rows and {int(missing['missing_count'].sum())} missing values detected." if not missing.empty else "Data quality is acceptable.",
        actions=["Review column mapping before analysis", "Remove duplicates if confirmed", "Proceed to audit modules"],
        priority="Medium" if len(dupes) > 0 else "Low",
    )
