"""
Query page for the Streamlit application.
This file demonstrates proper absolute imports that work when running from the project root.
"""

import streamlit as st
import sys
import os
from typing import List, Dict, Any

# Add the project root to Python path to enable absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Use absolute imports instead of relative imports
from streamlit_app.config import AppConfig, DatabaseConfig
from streamlit_app.utils import DatabaseManager, format_datetime, validate_connection, display_error, display_success


def main():
    """Main query page function."""
    st.title("🔍 Database Query Interface")
    st.markdown("Execute database queries and view results.")
    
    # Initialize configuration
    db_config = DatabaseConfig.from_env()
    app_config = AppConfig.from_env()
    
    # Sidebar configuration
    st.sidebar.header("Connection Settings")
    
    # Override config with user inputs
    db_config.host = st.sidebar.text_input("Database Host", value=db_config.host)
    db_config.port = st.sidebar.number_input("Database Port", value=db_config.port, min_value=1, max_value=65535)
    db_config.database = st.sidebar.text_input("Database Name", value=db_config.database)
    db_config.username = st.sidebar.text_input("Username", value=db_config.username)
    
    # Connection status
    st.sidebar.subheader("Connection Status")
    if validate_connection(db_config.host, db_config.port):
        st.sidebar.success("✅ Connection Available")
    else:
        st.sidebar.error("❌ Connection Failed")
    
    # Main query interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("SQL Query")
        query = st.text_area(
            "Enter your SQL query:",
            height=200,
            placeholder="SELECT * FROM your_table LIMIT 10;"
        )
        
        execute_button = st.button("Execute Query", type="primary")
    
    with col2:
        st.subheader("Query Templates")
        templates = {
            "Show Tables": "SHOW TABLES;",
            "Describe Table": "DESCRIBE your_table;",
            "Count Records": "SELECT COUNT(*) FROM your_table;",
            "Recent Records": "SELECT * FROM your_table ORDER BY created_at DESC LIMIT 10;"
        }
        
        selected_template = st.selectbox("Select a template:", list(templates.keys()))
        if st.button("Use Template"):
            st.session_state.query_template = templates[selected_template]
            st.rerun()
    
    # Apply template if selected
    if hasattr(st.session_state, 'query_template'):
        query = st.session_state.query_template
        del st.session_state.query_template
    
    # Execute query
    if execute_button and query.strip():
        try:
            db_manager = DatabaseManager(db_config)
            
            with st.spinner("Executing query..."):
                results = execute_query_safely(db_manager, query)
            
            if results:
                st.subheader("Query Results")
                st.dataframe(results, use_container_width=True)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export as CSV"):
                        csv_data = convert_to_csv(results)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"query_results_{format_datetime(st.session_state.get('query_time', 'unknown'))}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    st.metric("Rows Returned", len(results))
            else:
                st.info("Query executed successfully with no results.")
                
        except Exception as e:
            display_error("Query execution failed", str(e))
    
    elif execute_button:
        st.warning("Please enter a query before executing.")
    
    # Query history
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    if query and execute_button:
        st.session_state.query_history.append({
            'query': query,
            'timestamp': format_datetime(st.session_state.get('query_time', 'unknown'))
        })
    
    if st.session_state.query_history:
        st.subheader("Query History")
        for i, hist_query in enumerate(reversed(st.session_state.query_history[-5:])):
            with st.expander(f"Query {len(st.session_state.query_history) - i}: {hist_query['timestamp']}"):
                st.code(hist_query['query'], language='sql')


def execute_query_safely(db_manager: DatabaseManager, query: str) -> List[Dict[str, Any]]:
    """Execute a query safely with error handling."""
    try:
        # Store query execution time in session state
        import datetime
        st.session_state.query_time = datetime.datetime.now()
        
        results = db_manager.execute_query(query)
        display_success(f"Query executed successfully. Retrieved {len(results)} rows.")
        return results
    except Exception as e:
        raise RuntimeError(f"Database error: {str(e)}")


def convert_to_csv(data: List[Dict[str, Any]]) -> str:
    """Convert query results to CSV format."""
    import csv
    import io
    
    if not data:
        return ""
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


if __name__ == "__main__":
    main()