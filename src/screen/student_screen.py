import streamlit as st
import numpy as np
from PIL import Image
from src.ui.base_layout import style_background_dashboard, base_layout_style

from src.components.header_home import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login

def student_screen():
    style_background_dashboard()
    base_layout_style()
    
    c1, c2 = st.columns(2, vertical_alignment = "center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back To Home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
            
    st.header("Login using FaceID", text_alignment="center")
    st.space(2)
    photo_source = st.camera_input("Position Your Head in Center")
    
    if photo_source:
        np.array(Image.open(photo_source))
    footer_dashboard()