import streamlit as st

def add():
    st.info("Додати діяльність")
    name = st.text_input("ПІБ волонтера")
    hours = st.number_input("Години", min_value=1, max_value=100)