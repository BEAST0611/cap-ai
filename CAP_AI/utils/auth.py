"""Authentication, session management, and audit trail."""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

import streamlit as st

# Demo users — replace with DB in production
USERS: dict[str, dict[str, str]] = {
    "admin": {"password": "admin123", "role": "Admin", "name": "System Administrator"},
    "auditor": {"password": "audit123", "role": "Auditor", "name": "Senior Auditor"},
    "viewer": {"password": "view123", "role": "Viewer", "name": "Report Viewer"},
}

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "Admin": ["dashboard", "upload", "voter_dd", "round_tripping", "bank_charges",
              "interest", "idle_balance", "signatory", "reports", "settings"],
    "Auditor": ["dashboard", "upload", "voter_dd", "round_tripping", "bank_charges",
                "interest", "idle_balance", "signatory", "reports"],
    "Viewer": ["dashboard", "reports"],
}


def init_session_state() -> None:
    """Initialize all session state keys."""
    defaults: dict[str, Any] = {
        "authenticated": False,
        "username": None,
        "user_role": None,
        "user_name": None,
        "current_page": "Dashboard",
        "theme": "dark",
        "audit_trail": [],
        "notifications": [],
        "recent_uploads": [],
        "uploaded_data": None,
        "global_search": "",
        "custom_logo": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def authenticate(username: str, password: str) -> bool:
    """Validate credentials and set session."""
    user = USERS.get(username.lower())
    if user and user["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username.lower()
        st.session_state.user_role = user["role"]
        st.session_state.user_name = user["name"]
        log_audit("LOGIN", f"User {username} logged in")
        add_notification(f"Welcome back, {user['name']}!", "success")
        return True
    return False


def logout() -> None:
    """Clear authentication session."""
    username = st.session_state.get("username", "unknown")
    log_audit("LOGOUT", f"User {username} logged out")
    for key in ["authenticated", "username", "user_role", "user_name"]:
        st.session_state[key] = None if key != "authenticated" else False


def has_permission(page_key: str) -> bool:
    """Check if current role can access page."""
    role = st.session_state.get("user_role", "Viewer")
    return page_key in ROLE_PERMISSIONS.get(role, [])


def log_audit(action: str, detail: str) -> None:
    """Append entry to audit trail."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": st.session_state.get("username", "system"),
        "action": action,
        "detail": detail,
    }
    trail = st.session_state.get("audit_trail", [])
    trail.insert(0, entry)
    st.session_state.audit_trail = trail[:500]


def add_notification(message: str, level: str = "info") -> None:
    """Add notification to center."""
    notifs = st.session_state.get("notifications", [])
    notifs.insert(0, {
        "time": datetime.now().strftime("%H:%M"),
        "message": message,
        "level": level,
    })
    st.session_state.notifications = notifs[:50]


def hash_password(password: str) -> str:
    """Hash password for storage."""
    return hashlib.sha256(password.encode()).hexdigest()
