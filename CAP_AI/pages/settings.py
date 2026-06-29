"""Settings — theme, logo, profile, notifications."""

import streamlit as st
from pathlib import Path

from utils.auth import log_audit
from utils.ui import render_header


def render():
    render_header("Settings", "Configure platform preferences")

    tab1, tab2, tab3, tab4 = st.tabs(["Theme", "Logo", "Profile", "Notifications & Audit"])

    with tab1:
        theme = st.radio("Theme", ["dark", "light", "blue"], horizontal=True, index=["dark", "light", "blue"].index(st.session_state.get("theme", "dark")))
        if theme != st.session_state.get("theme"):
            st.session_state.theme = theme
            log_audit("SETTINGS", f"Theme changed to {theme}")
            st.rerun()
        st.success(f"Active theme: **{theme}**")

    with tab2:
        st.markdown("Upload your CAP AI logo (PNG/JPG/SVG)")
        logo_file = st.file_uploader("Logo", type=["png", "jpg", "jpeg", "svg"])
        if logo_file:
            dest = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
            dest.write_bytes(logo_file.read())
            st.session_state.custom_logo = str(dest)
            st.success("Logo updated successfully!")
            st.image(str(dest), width=200)

    with tab3:
        st.markdown(f"**Username:** {st.session_state.get('username', '—')}")
        st.markdown(f"**Name:** {st.session_state.get('user_name', '—')}")
        st.markdown(f"**Role:** {st.session_state.get('user_role', '—')}")
        st.info("Demo accounts: admin/admin123 · auditor/audit123 · viewer/view123")

    with tab4:
        notifs = st.session_state.get("notifications", [])
        st.markdown(f"#### Notifications ({len(notifs)})")
        for n in notifs[:10]:
            icon = {"success": "✅", "warning": "⚠️", "error": "❌"}.get(n.get("level", "info"), "ℹ️")
            st.markdown(f"{icon} **{n.get('time', '')}** — {n.get('message', '')}")

        st.markdown("#### Audit Trail")
        trail = st.session_state.get("audit_trail", [])
        if trail:
            import pandas as pd
            st.dataframe(pd.DataFrame(trail), use_container_width=True, height=300)
        else:
            st.caption("No audit events yet.")

        st.markdown("#### Recent Uploads")
        uploads = st.session_state.get("recent_uploads", [])
        if uploads:
            import pandas as pd
            st.dataframe(pd.DataFrame(uploads), use_container_width=True)
        else:
            st.caption("No recent uploads.")
