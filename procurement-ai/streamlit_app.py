from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="AI Procurement Intelligence System", page_icon="🤖", layout="wide")
st.title("AI Procurement Intelligence System")
st.caption("Upload vendor CSV, predict risk, rank vendors, generate explanation, and get negotiation advice.")

backend_url = st.text_input("Backend URL", value="http://localhost:8000")
file = st.file_uploader("Upload Vendor CSV", type=["csv"])

if file:
    with st.spinner("Running multi-agent procurement pipeline..."):
        try:
            response = requests.post(
                f"{backend_url.rstrip('/')}/analyze",
                files={"file": (file.name, file.getvalue(), "text/csv")},
                timeout=90,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    ranking_df = pd.DataFrame(result["ranking"])

    st.subheader("Decision Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Top Vendor", result["top_vendor"])
    col2.metric("Avg Risk", f"{result['risk_summary']['average_risk']:.3f}")
    col3.metric("Max Risk", f"{result['risk_summary']['max_risk']:.3f}")

    st.write("**AI Explanation**")
    st.info(result["explanation"])

    st.write("**Negotiation Advice**")
    st.success(result["negotiation"])

    st.write("**External Signals**")
    st.json(result["external_signals"])

    st.subheader("Vendor Comparison Table")
    st.dataframe(ranking_df, use_container_width=True)

    if {"vendor", "price", "risk_score"}.issubset(ranking_df.columns):
        chart_df = ranking_df[["vendor", "price", "risk_score"]].set_index("vendor")
        st.subheader("Risk vs Price")
        st.bar_chart(chart_df)

    if {"vendor", "final_score", "risk_score"}.issubset(ranking_df.columns):
        st.subheader("Final Score vs Risk")
        scatter_df = ranking_df[["vendor", "final_score", "risk_score"]].set_index("vendor")
        st.scatter_chart(scatter_df)

    st.subheader("Agent Flow")
    for step in result["decision_summary"].get("pipeline_steps", []):
        st.write(f"- {step}")

    st.subheader("Previous Decisions (Memory)")
    history_df = pd.DataFrame(result.get("history", []))
    if history_df.empty:
        st.write("No previous decisions yet.")
    else:
        st.dataframe(history_df, use_container_width=True)

    ranked_csv = ranking_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Ranked Vendors CSV",
        data=ranked_csv,
        file_name="ranked_vendors_with_risk.csv",
        mime="text/csv",
    )
else:
    st.info("Upload a CSV file to start the procurement intelligence pipeline.")
