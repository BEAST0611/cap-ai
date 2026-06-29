"""Voter DD Requirement Explainer."""

import streamlit as st

from utils.ui import render_ai_insights, render_header
from utils.voter_dd_data import get_document_types, get_purposes, get_states, search_voter_dd


def render():
    render_header("Voter DD Requirement Explainer", "Plain-language due diligence guidance by state")

    search = st.text_input("🔍 Search states, purposes, or keywords", placeholder="e.g. Tamil Nadu, address proof, Form 6")
    if search:
        results = search_voter_dd(search)
        st.markdown(f"**{len(results)} result(s)** for \"{search}\"")
        for state, purpose, doc_type, info in results:
            with st.expander(f"📋 {state} · {purpose} · {doc_type}", expanded=True):
                _render_guidance(info)
        return

    c1, c2, c3 = st.columns(3)
    states = get_states()
    with c1:
        state = st.selectbox("State / UT", states)
    with c2:
        purposes = get_purposes(state)
        purpose = st.selectbox("Purpose", purposes if purposes else ["—"])
    with c3:
        doc_types = get_document_types(state, purpose) if purpose != "—" else []
        doc_type = st.selectbox("Document Type", doc_types if doc_types else ["—"])

    if doc_type and doc_type != "—":
        from utils.voter_dd_data import VOTER_DD_DATA
        info = VOTER_DD_DATA[state][purpose][doc_type]
        st.markdown("---")
        _render_guidance(info)

    st.markdown("---")
    st.markdown("#### Quick Reference — All States")
    for s in states:
        with st.expander(f"🗳 {s}"):
            for p in get_purposes(s):
                st.markdown(f"**{p}**")
                for d in get_document_types(s, p):
                    st.caption(f"  · {d}")

    render_ai_insights(
        summary="Voter DD ensures electoral roll integrity through identity and address verification per ECI guidelines.",
        risk="Incomplete DD leads to duplicate registrations, underage voting, and constituency fraud.",
        actions=["Verify all documents against ECI handbook", "Cross-check Aadhaar seeding status", "Conduct BLO field verification"],
        priority="Medium",
        next_steps=["Select state and purpose above", "Share guidance with field teams"],
    )


def _render_guidance(info: dict) -> None:
    cards = [
        ("📖 What DD Means", info.get("what_is_dd", "")),
        ("📄 Required Documents", ", ".join(info.get("required_documents", []))),
        ("❓ Why It Is Needed", info.get("why_needed", "")),
        ("✅ Accepted Proofs", ", ".join(info.get("accepted_proofs", []))),
        ("⚠️ Common Mistakes", ", ".join(info.get("common_mistakes", []))),
        ("🔀 Exceptions", ", ".join(info.get("exceptions", []))),
    ]
    for title, content in cards:
        st.markdown(
            f'<div class="glass-card"><strong>{title}</strong><p style="margin:0.5rem 0 0;color:#94a3b8;">{content}</p></div>',
            unsafe_allow_html=True,
        )
