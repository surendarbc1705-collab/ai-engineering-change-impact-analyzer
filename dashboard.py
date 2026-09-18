import streamlit as st
import requests

st.set_page_config(
    page_title="AI Engineering Change Impact Analyzer",
    page_icon="🔐",
    layout="wide"
)

# =========================
# LOGIN CREDENTIALS
# =========================

USERNAME = "Innocore"
PASSWORD = "Admin@123"


# =========================
# LOGIN PAGE
# =========================

def login_page():

    st.title("🔐 Login")

    st.write("AI Engineering Change Impact Analyzer")

    username = st.text_input(
        "User ID",
        placeholder="Enter User ID"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter Password"
    )

    if st.button("Login", use_container_width=True):

        if username == USERNAME and password == PASSWORD:
            st.session_state["logged_in"] = True
            st.rerun()

        else:
            st.error("Invalid User ID or Password")


# =========================
# MAIN APPLICATION
# =========================

def main_app():

    st.title("🔍 AI Engineering Change Impact Analyzer")
    st.caption("AI-powered engineering change impact analysis")

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.success("Logged in as: Innocore")

    st.subheader("Proposed Engineering Change")

    change_description = st.text_area(
        "Describe the change you are planning:",
        placeholder="Example: Remove Customer_Status column from Customer table",
        height=120
    )

    if st.button("🚀 Analyze Change", use_container_width=True):

        if not change_description.strip():
            st.warning("Please enter a change description.")

        else:
            try:

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "change_description": change_description
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.divider()

                    # Risk Assessment
                    st.subheader("Risk Assessment")

                    risk = result.get(
                        "risk_level",
                        "UNKNOWN"
                    )

                    if risk == "HIGH":
                        st.error(
                            f"🔴 Risk Level: {risk}"
                        )

                    elif risk == "MEDIUM":
                        st.warning(
                            f"🟠 Risk Level: {risk}"
                        )

                    else:
                        st.success(
                            f"🟢 Risk Level: {risk}"
                        )

                    # Affected Components
                    st.subheader("Affected Components")

                    components = result.get(
                        "affected_components",
                        []
                    )

                    for component in components:

                        with st.container(border=True):

                            st.write(
                                f"**{component.get('name', 'Unknown')}**"
                            )

                            st.write(
                                f"Impact: **{component.get('impact', 'UNKNOWN')}**"
                            )

                            st.write(
                                f"Why: {component.get('reason', '')}"
                            )

                    # Historical Incidents
                    st.subheader("Historical Incidents")

                    incidents = result.get(
                        "historical_incidents",
                        []
                    )

                    if incidents:

                        for incident in incidents:

                            with st.container(border=True):

                                st.write(
                                    f"**{incident.get('id', 'Unknown')}**"
                                )

                                st.write(
                                    f"Impact: {incident.get('impact', '')}"
                                )

                                st.write(
                                    f"Relevance: {incident.get('relevance', '')}"
                                )

                    else:

                        st.info(
                            "No relevant historical incidents found."
                        )

                    # Downstream Consequences
                    st.subheader(
                        "Downstream Consequences"
                    )

                    consequences = result.get(
                        "downstream_consequences",
                        []
                    )

                    for consequence in consequences:

                        st.write(
                            f"⚠️ {consequence}"
                        )

                    # Recommendations
                    st.subheader(
                        "Recommended Actions"
                    )

                    recommendations = result.get(
                        "recommendations",
                        []
                    )

                    for recommendation in recommendations:

                        st.write(
                            f"✅ {recommendation}"
                        )

                    # Rollback
                    st.subheader("Rollback Plan")

                    rollback = result.get(
                        "rollback_plan",
                        []
                    )

                    for action in rollback:

                        st.write(
                            f"↩️ {action}"
                        )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI server is not running. "
                    "Please start the FastAPI server first."
                )


# =========================
# SESSION CONTROL
# =========================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


if st.session_state["logged_in"]:
    main_app()

else:
    login_page()