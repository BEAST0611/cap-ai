"""AgGrid table wrapper with sorting, filtering, export."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from utils.exporters import to_csv_bytes, to_excel_bytes, simple_pdf_table


def render_data_table(
    df: pd.DataFrame,
    key: str = "grid",
    height: int = 400,
    enable_export: bool = True,
) -> pd.DataFrame | None:
    """Render interactive AgGrid with export buttons."""
    if df is None or df.empty:
        st.info("No data to display.")
        return None

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        filterable=True,
        sortable=True,
        resizable=True,
        editable=False,
        wrapText=True,
        autoHeight=True,
    )
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_side_bar(filters_panel=True, columns_panel=True)
    gb.configure_selection("multiple", use_checkbox=True)
    grid_options = gb.build()

    response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme="streamlit",
        height=height,
        key=key,
    )

    if enable_export:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📥 Excel", to_excel_bytes(df), "export.xlsx", "application/vnd.ms-excel", key=f"xlsx_{key}")
        with c2:
            st.download_button("📥 CSV", to_csv_bytes(df), "export.csv", "text/csv", key=f"csv_{key}")
        with c3:
            try:
                st.download_button("📥 PDF", simple_pdf_table("Export", df), "export.pdf", "application/pdf", key=f"pdf_{key}")
            except Exception:
                st.caption("PDF export unavailable")

    selected = response.get("selected_rows")
    if selected is not None and len(selected) > 0:
        return pd.DataFrame(selected)
    return df
