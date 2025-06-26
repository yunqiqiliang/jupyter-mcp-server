"""Helper utility functions."""

import datetime
from typing import Optional, Dict, Any

# Import streamlit only when available
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    # Mock streamlit functions for testing
    class MockStreamlit:
        def error(self, message): print(f"ERROR: {message}")
        def success(self, message): print(f"SUCCESS: {message}")
        def expander(self, title): return MockExpander()
        def text(self, content): print(content)
        @property
        def session_state(self): return {}
    
    class MockExpander:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def text(self, content): print(content)
    
    st = MockStreamlit()


def format_datetime(dt: datetime.datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object to string."""
    return dt.strftime(format_str)


def validate_connection(host: str, port: int, timeout: int = 5) -> bool:
    """Validate a network connection."""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def display_error(message: str, details: Optional[str] = None) -> None:
    """Display an error message with optional details."""
    st.error(message)
    if details:
        with st.expander("Error Details"):
            st.text(details)


def display_success(message: str) -> None:
    """Display a success message."""
    st.success(message)


def get_session_state(key: str, default: Any = None) -> Any:
    """Get a value from Streamlit session state."""
    if HAS_STREAMLIT:
        return st.session_state.get(key, default)
    return default


def set_session_state(key: str, value: Any) -> None:
    """Set a value in Streamlit session state."""
    if HAS_STREAMLIT:
        st.session_state[key] = value