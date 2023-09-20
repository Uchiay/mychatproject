import streamlit as st

Welcome_MSG="""
    Introduce yourself!!

    Welcome to CDP Chat Bot!!! I am ChatCDP.

    I am a chat bot that can help you with your data needs. I can answer questions about the data in the CDP Data Warehouse. I can also help you write SQL queries to get the data you need.
"""

def init_get_system_prompt():
    return Welcome_MSG

# do `streamlit run init_prompt.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("Initiallzing System prompt for ChatBot")
    st.markdown(init_get_system_prompt())