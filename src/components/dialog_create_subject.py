import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subjecty")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to CS")
    sub_sec = st.text_input("Section", placeholder="A")
    
    
    if st.button("Create Subject Now", type="primary", width="stretch"):
        if sub_id and sub_name and sub_sec:
            try:
                create_subject(sub_id, sub_name, sub_sec, teacher_id)
                st.toast("Subject created Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str/(e)}")
        else:
            st.warning("Please fill all the fields")