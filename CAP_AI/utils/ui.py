"""UI components, theme, CSS, and shared widgets."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CSS_PATH = ASSETS / "css" / "theme.css"


def load_css() -> None:
    """Inject custom CSS theme."""
    if CSS_PATH.exists():
        css = CSS_PATH.read_text(encoding="utf-8")
    else:
        css = _fallback_css()
    theme = st.session_state.get("theme", "dark")
    st.markdown(
        f'<div data-theme="{theme}"></div>'
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


def _fallback_css() -> str:
    return """
    .stApp { background: linear-gradient(135deg, #0a1628, #1e3a5f) !important; }
    """


def get_logo_path() -> Path:
    """Return active logo path (custom upload or default)."""
    custom = st.session_state.get("custom_logo")
    if custom and Path(custom).exists():
        return Path(custom)
    for name in ("logo.png", "logo.jpg", "logo.jpeg", "logo.svg"):
        p = ASSETS / name
        if p.exists():
            return p
    return ASSETS / "logo.png"


def logo_base64() -> str:
    """Encode logo as base64 for HTML embedding."""
    path = get_logo_path()
    if not path.exists():
        return ""
    suffix = path.suffix.lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "svg": "image/svg+xml"}
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:{mime.get(suffix.lstrip('.'), 'image/png')};base64,{b64}"


def render_logo(width: int = 180) -> None:
    """Display logo in sidebar or login."""
    path = get_logo_path()
    if path.exists():
        st.image(str(path), width=width)
    else:
        st.markdown(
            '<div style="text-align:center;font-size:2rem;font-weight:800;'
            'background:linear-gradient(135deg,#38bdf8,#0ea5e9);'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CAP AI</div>',
            unsafe_allow_html=True,
        )


def render_header(title: str, subtitle: str = "") -> None:
    """Sticky page header."""
    user = st.session_state.get("user_name", "User")
    role = st.session_state.get("user_role", "")
    notif_count = len(st.session_state.get("notifications", []))
    st.markdown(
        f"""
        <div class="cap-header">
            <div>
                <h2 style="margin:0;color:#e2e8f0;font-weight:700;">{title}</h2>
                <p style="margin:0;color:#94a3b8;font-size:0.85rem;">{subtitle}</p>
            </div>
            <div style="text-align:right;color:#94a3b8;font-size:0.85rem;">
                👤 {user} · {role}
                {' · <span class="notif-badge">' + str(notif_count) + '</span> 🔔' if notif_count else ''}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str | int | float, icon: str = "📊", delay: int = 0) -> str:
    """Return HTML for animated KPI card."""
    return f"""
    <div class="kpi-card animate-delay-{min(delay, 4)}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """


def render_kpi_row(metrics: list[tuple[str, str | int | float, str]]) -> None:
    """Render row of KPI cards."""
    cols = st.columns(len(metrics))
    for i, (label, value, icon) in enumerate(metrics):
        with cols[i]:
            st.markdown(kpi_card(label, value, icon, i), unsafe_allow_html=True)


def render_ai_insights(
    summary: str,
    risk: str,
    actions: list[str],
    priority: str = "Medium",
    next_steps: list[str] | None = None,
) -> None:
    """Render AI insight panel on each page."""
    priority_class = {"High": "priority-high", "Medium": "priority-medium", "Low": "priority-low"}.get(
        priority, "priority-medium"
    )
    actions_html = "".join(f"<li>{a}</li>" for a in actions)
    steps_html = ""
    if next_steps:
        steps_html = "<p><strong>Next Steps:</strong></p><ol>" + "".join(
            f"<li>{s}</li>" for s in next_steps
        ) + "</ol>"

    st.markdown(
        f"""
        <div class="ai-insight-box {priority_class}">
            <h4 style="margin-top:0;color:#38bdf8;">🤖 AI Insights · Priority: {priority}</h4>
            <p><strong>Summary:</strong> {summary}</p>
            <p><strong>Risk Explanation:</strong> {risk}</p>
            <p><strong>Recommended Actions:</strong></p>
            <ul>{actions_html}</ul>
            {steps_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_title(icon: str, title: str) -> None:
    """Consistent page title."""
    st.markdown(f"### {icon} {title}")


def loading_spinner(message: str = "Analyzing data...") -> Any:
    """Context manager style spinner."""
    return st.spinner(message)
