"""
Main Streamlit application entry point.
Run with: streamlit run streamlit_app/app.py
"""

import streamlit as st
import sys
import os

# Add the project root to Python path to enable absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Main application function."""
    st.set_page_config(
        page_title="Jupyter MCP Server Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🚀 Jupyter MCP Server Dashboard")
    st.markdown("Welcome to the Jupyter MCP Server management interface.")
    
    # Navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Use the pages above to navigate through different sections of the application.")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📊 Server Status")
        st.success("Server is running")
        st.metric("Active Connections", "5")
        st.metric("Uptime", "2h 15m")
    
    with col2:
        st.header("🔧 Quick Actions")
        if st.button("Restart Server"):
            st.info("Server restart initiated...")
        if st.button("View Logs"):
            st.info("Opening logs...")

if __name__ == "__main__":
    main()