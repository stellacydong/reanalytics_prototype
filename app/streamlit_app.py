# app/streamlit_app.py

import os
import sys
import streamlit as st
import json

# Fix Python path so imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import components
from app.components.treaty_uploader import upload_treaties
from app.components.optimizer_engine import optimize_portfolio
from app.components.dashboard import show_dashboard
from app.components.report_generator import PortfolioReportGenerator

# Set Streamlit page config
st.set_page_config(page_title="Treaty Portfolio Optimizer", page_icon="📈", layout="wide")

# App title
st.title("Treaty Portfolio Optimizer + Co-Pilot 🚀")
st.markdown("**Optimize your reinsurance treaty portfolio for better capital efficiency and lower tail risk.**")
st.markdown("---")

# Step 1: Upload Treaties
uploaded_treaties = upload_treaties()

if uploaded_treaties:
    st.success(f"✅ Uploaded {len(uploaded_treaties)} treaty file(s)!")

    # Step 2: Optimize Button
    if st.button("🚀 Optimize Portfolio with AI"):
        result = optimize_portfolio()
        st.session_state['original_portfolio'] = result['original_portfolio']
        st.session_state['optimized_portfolio'] = result['optimized_portfolio']
        st.success("✅ Portfolio optimization complete!")

# Step 3: Dashboard Display
if 'original_portfolio' in st.session_state and 'optimized_portfolio' in st.session_state:
    show_dashboard(st.session_state['original_portfolio'], st.session_state['optimized_portfolio'])

    # Step 4: Report Generation
    st.markdown("---")
    st.subheader("📄 Download Executive Report")
    if st.button("Generate PDF Report"):
        generator = PortfolioReportGenerator()
        report_path = generator.generate_report(
            st.session_state['original_portfolio'],
            st.session_state['optimized_portfolio'],
            output_filename="portfolio_optimization_report.pdf"
        )
        with open(report_path, "rb") as file:
            st.download_button(
                label="📥 Download Portfolio Report",
                data=file,
                file_name="portfolio_optimization_report.pdf",
                mime="application/pdf"
            )

# Footer
st.markdown("---")
st.caption("Built with ❤️ for Reinsurance Innovation • Powered by AI • © 2025")
