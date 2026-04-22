import requests
import streamlit as st

st.set_page_config(page_title="AI Procurement Decision Engine", page_icon="🎯", layout="wide")
st.title("AI Procurement Decision Engine")

backend_url = st.text_input("Backend URL", value="http://localhost:8000")
file = st.file_uploader("Upload Vendor CSV", type=["csv"])

if file:
    with st.spinner("Analyzing vendor data..."):
        try:
            response = requests.post(
                f"{backend_url.rstrip('/')}/analyze",
                files={"file": (file.name, file.getvalue(), "text/csv")},
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    st.subheader("Top Vendor")
    st.success(result["top_vendor"])

    st.subheader("Explanation")
    st.write(result["explanation"])

    st.subheader("Full Ranking")
    st.dataframe(result["ranking"], use_container_width=True)
