import streamlit as st
from src.ui.base_layout import style_background_dashboard, base_layout_style

from src.components.header_home import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login

def teacher_screen():
    
    style_background_dashboard()
    base_layout_style()
    
    
    if 'teacher' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher
    st.header(f"Welcome, {teacher_data['name']}!", text_alignment="center")

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment = "center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back To Home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
                st.session_state['login_type'] = None
                st.rerun()
        
    st.header("Login using password", text_alignment="center")
    st.space(2)
    teacher_username = st.text_input("Enter your username", placeholder="Username")
    teacher_password = st.text_input("Enter your password", placeholder="Password", type="password")    
    st.divider()
    
    
    btn1, btn2 = st.columns(2, gap="large")
    with btn1:
        if st.button("Login", type="secondary", icon=":material/passkey:", shortcut="control+enter", width='stretch'):
            if not teacher_username or not teacher_password:
                st.error("Please enter both username and password.")
            else:
                teacher = teacher_login(teacher_username, teacher_password)
                if teacher:
                    st.success(f"Welcome, {teacher['name']}!")
                    st.session_state['teacher'] = teacher
                    st.session_state['login_type'] = 'teacher'
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
        
    with btn2:
            if st.button("Register Instead", type="primary", icon=":material/passkey:", width='stretch'):
                st.session_state.teacher_login_type = 'register'
                st.rerun()
    footer_dashboard()
    
def register_teacher(teacher_username, teacher_name, teacher_password, teacher_confirm_password):
    if not teacher_username or not teacher_name or not teacher_password:
        return False, "All fields are required. Please fill in all the details."
    
    if teacher_password != teacher_confirm_password:
        return False, "Passwords do not match."
    
    if check_teacher_exists(teacher_username):
        return False, "Username already exists. Please choose a different username."
    try:
        create_teacher(teacher_username, teacher_name, teacher_password)
        return True, "Teacher registered successfully!"
    except Exception as e:
        return False, "Unexpected error occured!"

def teacher_screen_register():
    c1, c2 = st.columns(2, gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back To Home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
            
    st.header("Register Your Teacher Profile")
    
    st.space(2)
    teacher_username = st.text_input("Enter your username", placeholder="sangram")
    teacher_name = st.text_input("Enter your name", placeholder="Sangram Choudhury")
    teacher_password = st.text_input("Enter your password", placeholder="Password", type="password")
    teacher_confirm_password = st.text_input("Confirm your password", placeholder="Confirm Password", type="password")    
    st.divider()
        
        
    btn1, btn2 = st.columns(2, gap="large")
    with btn1:
        if st.button("Register Now", type="secondary", icon=":material/passkey:", shortcut="control+enter", width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)
            
    with btn2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width='stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()
    footer_dashboard()