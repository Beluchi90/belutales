# utils/state.py - State management utilities for BeluTales
import streamlit as st

def set_qp(**kwargs):
    """Set query parameters and session state"""
    merge = kwargs.pop('_merge', True)
    
    for key, value in kwargs.items():
        # Update session state
        st.session_state[key] = value
        
        # Update query parameters if relevant
        if key in ['cat', 'pick', 'quiz'] and value is not None:
            current_params = dict(st.query_params)
            current_params[key] = str(value)
            st.query_params.update(current_params)
        elif key in ['cat', 'pick', 'quiz'] and value is None:
            # Remove parameter if value is None
            current_params = dict(st.query_params)
            if key in current_params:
                del current_params[key]
                st.query_params.clear()
                st.query_params.update(current_params)
