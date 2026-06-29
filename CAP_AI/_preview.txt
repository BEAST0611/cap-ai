"""
CAP AI — Professional AI-Powered Banking & Voter DD Audit Platform
Main application entry point with login, navigation, and session management.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from utils.auth import authenticate, has_permission, init_session_state, logout, log_audit
from utils.ui import load_css, render_logo

try:
    from streamlit_option_menu import option_menu
except ImportError:
    option_menu = None

PAGES = {
    "Dashboard": ("dashboard", "🏠"),
    "Upload Excel": ("upload", "📁"),
    "Voter DD Requirement Explainer": ("voter_dd", "🗳"),
    "Fund Round-Tripping Detection": ("round_tripping", "🔍"),
    "Bank Charges Verification": ("bank_charges", "🏦"),
    "Interest Verification": ("interest", "💰"),
    "Idle Balance Detection": ("idle_balance", "📊"),
    "Authorised Signatory Verification": ("signatory", "👤"),
    "Reports": ("reports", "📈"),
    "Settings": ("settings", "⚙"),
}


def configure_page():
    st.set_page_config(
        page_title="CAP AI — Audit Platform",
        page_icon=str(ROOT / "assets" / "logo.png") if (ROOT / "assets" / "logo.png").exists() else "🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_login():
    load_css()
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<p class="login-title">CAP AI</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center;color:#94a3b8;margin-bottom:1.5rem;">'
            "Banking & Voter DD Audit Platform</p>",
            unsafe_allow_html=True,
        )
        render_logo(160)
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        if st.button("Sign In", use_container_width=True, type="primary"):
            if authenticate(username, password):
                st.rerun()
            else:
                st.error("Invalid credentials. Try admin / admin123")
        st.markdown(
            '<p style="text-align:center;color:#64748b;font-size:0.75rem;margin-top:1rem;">'
            "Demo: admin · auditor · viewer</p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar() -> str:
    with st.sidebar:
        render_logo(150)
        st.markdown("---")
        st.markdown(
            f"**{st.session_state.get('user_name', 'User')}**  \n"
            f"<span style='color:#94a3b8;font-size:0.85rem;'>{st.session_state.get('user_role', '')}</span>",
            unsafe_allow_html=True,
        )

        search = st.text_input("🔍 Global Search", placeholder="Search modules...", key="global_search_input")
        if search:
            st.session_state.global_search = search

        labels = list(PAGES.keys())
        icon_map = {
            "Dashboard": "speedometer2",
            "Upload Excel": "cloud-upload",
            "Voter DD Requirement Explainer": "book",
            "Fund Round-Tripping Detection": "search",
            "Bank Charges Verification": "bank",
            "Interest Verification": "currency-rupee",
            "Idle Balance Detection": "bar-chart",
            "Authorised Signatory Verification": "person-check",
            "Reports": "file-earmark-bar-graph",
            "Settings": "gear",
        }
        menu_icons = [icon_map.get(k, "circle") for k in labels]
        current = st.session_state.get("current_page", "Dashboard")
        default_idx = labels.index(current) if current in labels else 0

        if option_menu:
            selected = option_menu(
                menu_title=None,
                options=labels,
                icons=menu_icons,
                default_index=default_idx,
                styles={
                    "container": {"padding": "0", "background-color": "transparent"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "2px 0"},
                    "nav-link-selected": {"background-color": "#0ea5e9", "border-radius": "8px"},
                },
            )
        else:
            selected = st.radio("Navigation", labels, index=default_idx, label_visibility="collapsed")

        st.markdown("---")
        notifs = st.session_state.get("notifications", [])
        with st.expander(f"🔔 Notifications ({len(notifs)})", expanded=False):
            for n in notifs[:5]:
                st.caption(f"{n.get('time', '')} — {n.get('message', '')}")

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

    return selected


def load_page(name: str):
    key = PAGES.get(name, ("dashboard", ""))[0]
    if not has_permission(key):
        st.warning("You do not have permission to access this page.")
        return
    log_audit("NAVIGATE", f"Opened {name}")
    module = __import__(f"pages.{key}", fromlist=["render"])
    module.render()


def main():
    configure_page()
    init_session_state()

    if not st.session_state.get("authenticated"):
        render_login()
        return

    load_css()
    selected = render_sidebar()
    st.session_state.current_page = selected

    gs = st.session_state.get("global_search", "")
    if gs:
        st.info(f"Global search: **{gs}** — filter results within each module.")

    load_page(selected)


if __name__ == "__main__":
    main()
