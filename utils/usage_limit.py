import streamlit as st


MAX_USES = 2


def initialize_usage():

    if "usage_count" not in st.session_state:
        st.session_state.usage_count = 0


def can_use():

    initialize_usage()

    return st.session_state.usage_count < MAX_USES


def increase_usage():

    initialize_usage()

    st.session_state.usage_count += 1


def remaining_uses():

    initialize_usage()

    return MAX_USES - st.session_state.usage_count