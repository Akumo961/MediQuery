"""MediQuery's intentionally small Streamlit client for the authenticated report workflow."""

import os

import requests
import streamlit as st


API_URL = os.getenv("MEDIQUERY_API_URL", "http://localhost:8000")

st.set_page_config(page_title="MediQuery", page_icon="🩺", layout="wide")
st.markdown(
    """<style>
    .block-container {max-width: 1120px; padding-top: 3rem;}
    .mq-card {padding: 1.2rem; border: 1px solid #d9e3ea; border-radius: .75rem; background: #fff;}
    </style>""",
    unsafe_allow_html=True,
)


def api(method: str, path: str, **kwargs):
    headers = kwargs.pop("headers", {})
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.request(
        method, f"{API_URL}{path}", headers=headers, timeout=30, **kwargs
    )


def request_auth(mode: str, email: str, password: str, acknowledged: bool) -> None:
    try:
        response = api(
            "POST",
            f"/api/auth/{mode}",
            json={
                "email": email,
                "password": password,
                "acknowledge_medical_limitations": acknowledged,
            },
        )
        if response.ok:
            st.session_state.access_token = response.json()["access_token"]
            st.rerun()
        st.error(response.json().get("detail", "We could not complete that request."))
    except requests.RequestException:
        st.error("MediQuery is unavailable. Please try again shortly.")


def signed_out_view() -> None:
    st.title("Understand the facts in your lab report")
    st.subheader(
        "A private, evidence-first way to organize extracted report values before "
        "discussing them with a qualified clinician."
    )
    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown(
            """### How it works
        1. Upload a text-based PDF report.
        2. MediQuery preserves detectable values, units, ranges, and source page
           evidence.
        3. Review the original report and speak with a qualified health professional for medical advice.

        MediQuery is not a diagnostic service and does not replace professional medical
        advice, diagnosis, or treatment."""
        )
    with right:
        st.markdown('<div class="mq-card">', unsafe_allow_html=True)
        mode = st.radio("Account", ["Log in", "Create account"], horizontal=True)
        email = st.text_input("Email", autocomplete="email")
        password = st.text_input(
            "Password", type="password", help="Use at least 12 characters."
        )
        acknowledged = st.checkbox(
            "I understand MediQuery is not medical advice or a diagnostic service.",
            disabled=mode == "Log in",
        )
        if st.button(mode, type="primary", use_container_width=True):
            request_auth(
                "login" if mode == "Log in" else "signup",
                email,
                password,
                acknowledged or mode == "Log in",
            )
        st.caption(
            "Password reset and email verification are planned before public launch."
        )
        st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    first, second, third = st.columns(3)
    with first:
        st.markdown("### Evidence first")
        st.write(
            "Review each detected candidate beside its original report evidence and page."
        )
    with second:
        st.markdown("### Private by design")
        st.write(
            "Reports are owner-scoped and are not published through a public upload URL."
        )
    with third:
        st.markdown("### Simple plans")
        st.write(
            "The Free plan has a configurable report allowance. Pro billing is planned, not active."
        )
    st.markdown("### Frequently asked questions")
    with st.expander("Can MediQuery diagnose me?"):
        st.write(
            "No. It is an educational report-organizing tool. Consult a qualified "
            "health professional for medical decisions."
        )
    with st.expander("What reports can I upload?"):
        st.write(
            "Text-based PDF reports up to the configured limit. Scanned PDFs may not "
            "contain selectable text and OCR is not enabled yet."
        )
    with st.expander("How do I delete my information?"):
        st.write(
            "You can delete each report in the dashboard. Account deletion is "
            "available through the authenticated API; a self-service UI control is planned."
        )
    st.caption(
        "Privacy note: Reports are sensitive. Do not upload a report unless you are "
        "authorized to do so. Production deployment requires approved private storage "
        "and legal/privacy review."
    )


def dashboard() -> None:
    st.sidebar.title("MediQuery")
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()
    st.sidebar.caption("Educational report organization—not diagnosis.")
    with st.sidebar.expander("Account settings"):
        st.caption(
            "Deleting your account permanently removes the reports stored by this local deployment."
        )
        confirm_delete = st.checkbox(
            "I understand this cannot be undone", key="confirm-account-delete"
        )
        if st.button(
            "Delete account", disabled=not confirm_delete, key="delete-account"
        ):
            response = api("DELETE", "/api/auth/account")
            if response.status_code == 204:
                st.session_state.clear()
                st.rerun()
            st.error("We could not delete the account. Please try again.")
    st.title("Your reports")
    try:
        plan_response = api("GET", "/api/reports/plan")
        if plan_response.status_code == 401:
            st.session_state.clear()
            st.rerun()
        plan = plan_response.json()
        if plan["reports_limit"] is None:
            st.caption(f"{plan['plan'].title()} plan")
        else:
            st.caption(
                f"{plan['reports_used']} of {plan['reports_limit']} reports used on the Free plan"
            )
    except requests.RequestException:
        st.error("We could not load your account. Please try again shortly.")
        return

    upload = st.file_uploader(
        "Upload a text-based PDF report",
        type=["pdf"],
        help="Maximum 10 MB. Scanned PDFs may require OCR, which is not yet available.",
    )
    if upload and st.button("Process report", type="primary"):
        with st.spinner("Validating and extracting report facts…"):
            response = api(
                "POST",
                "/api/reports",
                files={"file": (upload.name, upload.getvalue(), "application/pdf")},
            )
        if response.ok:
            st.success(
                "Report processed. Review detected candidates against the original PDF."
            )
            st.rerun()
        else:
            st.error(
                response.json().get("detail", "The report could not be processed.")
            )

    response = api("GET", "/api/reports")
    if not response.ok:
        st.error("We could not load your reports.")
        return
    reports = response.json()
    if not reports:
        st.info(
            "Upload your first report to see extracted values and page-level evidence here."
        )
        return
    for report in reports:
        with st.expander(
            f"{report['original_filename']} · {report['page_count']} pages",
            expanded=False,
        ):
            if report.get("extraction_note"):
                st.warning(report["extraction_note"])
            findings = report["findings"]
            if findings:
                st.caption(
                    "Extracted candidates — verify every item against the original report."
                )
                st.dataframe(
                    [
                        {
                            "Name": x["name"],
                            "Value": x["value"],
                            "Unit": x["unit"],
                            "Reference range": x["reference_range"],
                            "Flag": x["flag"],
                            "Page": x["page"],
                        }
                        for x in findings
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
                with st.popover("Show source evidence"):
                    for finding in findings:
                        st.write(
                            f"Page {finding['page']} · {finding['name']}: {finding['evidence']}"
                        )
            else:
                st.info(
                    "No structured values were identified. Review the original report."
                )
            if st.button("Delete report", key=f"delete-{report['id']}"):
                deleted = api("DELETE", f"/api/reports/{report['id']}")
                if deleted.status_code == 204:
                    st.success("Report deleted.")
                    st.rerun()
                st.error("The report could not be deleted.")


if st.session_state.get("access_token"):
    dashboard()
else:
    signed_out_view()
