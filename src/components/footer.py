import streamlit as st
import base64
from pathlib import Path

def footer_home():
    logo_path = (
        Path(__file__).parent
        / "logo"
        / "Prajna-removebg-preview.png"
    )

    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(
            image_file.read()
        ).decode("utf-8")
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 2rem; gap: 6px; ">
            <span style="font-weight: bold; color: white;">Created with ❤️ by </span>
            <img src="data:image/png;base64,{encoded_logo}" alt="Logo" style="height: 80px; width: 50px;">

        </div>
        """, unsafe_allow_html=True)