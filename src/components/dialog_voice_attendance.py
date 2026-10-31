import streamlit as st
from src.database.config import supabase
from src.database.db import create_attendance

@st.dialog("Attendance Report")
def voice_attendance_dialog():
    return