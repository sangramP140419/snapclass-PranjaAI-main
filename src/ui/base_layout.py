import streamlit as st

def style_background_home():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #5865f2 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def style_background_dashboard():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #E0E3FF !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def base_layout_style():
    st.markdown(
        """
        <style>
            #mainMenu, footer, header {visibility: hidden;}

            .block-container {
                padding-top: 1.5rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )