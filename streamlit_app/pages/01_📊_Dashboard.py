"""
Dashboard page demonstrating proper absolute imports.
This shows how to structure imports when running from the project root.
"""

import streamlit as st
import sys
import os

# Add the project root to Python path to enable absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Use absolute imports instead of relative imports
from streamlit_app.config import AppConfig, DatabaseConfig
from streamlit_app.utils import DatabaseManager, format_datetime, validate_connection


def main():
    """Main dashboard page function."""
    st.title("📊 Server Dashboard")
    st.markdown("Real-time monitoring and analytics for the Jupyter MCP Server.")
    
    # Load configuration
    app_config = AppConfig.from_env()
    db_config = DatabaseConfig.from_env()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Sessions",
            value="24",
            delta="3",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="CPU Usage",
            value="67%",
            delta="-5%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Memory Usage", 
            value="4.2 GB",
            delta="0.3 GB",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Response Time",
            value="145ms",
            delta="-12ms",
            delta_color="inverse"
        )
    
    # Charts section
    st.subheader("📈 Performance Metrics")
    
    tab1, tab2, tab3 = st.tabs(["Response Times", "Connection Stats", "Error Rates"])
    
    with tab1:
        # Mock response time data
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        response_times = np.random.normal(150, 30, 30)
        df = pd.DataFrame({'Date': dates, 'Response Time (ms)': response_times})
        
        st.line_chart(df.set_index('Date'))
    
    with tab2:
        # Mock connection data
        connection_data = pd.DataFrame({
            'Hour': range(24),
            'Connections': np.random.poisson(20, 24)
        })
        st.bar_chart(connection_data.set_index('Hour'))
    
    with tab3:
        # Mock error rate data
        error_data = pd.DataFrame({
            'Error Type': ['Timeout', 'Connection Failed', 'Invalid Query', 'Permission Denied'],
            'Count': [5, 2, 8, 1]
        })
        st.bar_chart(error_data.set_index('Error Type'))
    
    # System status section
    st.subheader("🔧 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Database Connection**")
        if validate_connection(db_config.host, db_config.port):
            st.success("✅ Connected")
        else:
            st.error("❌ Disconnected")
        
        st.write("**Server Health**")
        st.success("✅ Healthy")
        
        st.write("**Last Backup**")
        st.info("2 hours ago")
    
    with col2:
        st.write("**Configuration**")
        st.text(f"Debug Mode: {'On' if app_config.debug else 'Off'}")
        st.text(f"Max Connections: {app_config.max_connections}")
        st.text(f"Timeout: {app_config.timeout}s")
        st.text(f"Log Level: {app_config.log_level}")
    
    # Recent activity
    st.subheader("📝 Recent Activity")
    
    activity_data = [
        {"Time": "10:45 AM", "Event": "New connection established", "Status": "Success"},
        {"Time": "10:42 AM", "Event": "Query executed", "Status": "Success"},
        {"Time": "10:38 AM", "Event": "User authentication", "Status": "Success"},
        {"Time": "10:35 AM", "Event": "Connection timeout", "Status": "Warning"},
        {"Time": "10:30 AM", "Event": "Server restart", "Status": "Info"}
    ]
    
    for activity in activity_data:
        cols = st.columns([1, 4, 1])
        with cols[0]:
            st.text(activity["Time"])
        with cols[1]:
            st.text(activity["Event"])
        with cols[2]:
            if activity["Status"] == "Success":
                st.success("✅")
            elif activity["Status"] == "Warning":
                st.warning("⚠️")
            else:
                st.info("ℹ️")


if __name__ == "__main__":
    main()