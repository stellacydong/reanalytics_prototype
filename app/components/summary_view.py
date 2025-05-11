# app/components/summary_view.py

import streamlit as st

def display_summary(summary_text: str):
    import streamlit as st
    st.subheader("📘 Treaty Summary")
    st.markdown(summary_text)


def display_treaty_summary(summary: str):
    """
    Render the LLM-generated treaty summary in the app.

    Args:
        summary (str): Text output from the language model.
    """
    st.subheader("📄 Treaty Summary")
    
    if summary:
        st.markdown(
            f"<div style='background-color:#f9f9f9;padding:1em;border-left:5px solid #4CAF50;'>"
            f"{summary.replace('\n', '<br>')}"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("No summary available. Please upload a treaty file and run the summarizer.")
