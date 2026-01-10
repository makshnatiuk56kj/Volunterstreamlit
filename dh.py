import streamlit as st
from db import init_dh, volunteer_categories, add_dh, get_volh
from PIL import Image


def add_hd():
    init_dh()
    st.title("Додаєднатися до групи волонтерства")
    colh=st.selectbox("Наявні категорії", volunteer_categories)


    detail=st.text_area("Що потрібно зробити")
    hours = st.number_input("Години", min_value=1, max_value=100)

    
    
    if st.button("Зберегти", key="save_volh"):
        if not colh or not detail:
            st.error("Категорія і опис обов'язкові")
            return

        add_dh(colh,detail,hours)

        st.success("Діяльність успішно додана!")
        st.write(f"Категорія: {colh}")
        st.write(f": {detail}")
        st.write(f"Години: {hours}")



def print_dh():
    st.header("", text_alignment="center")

    place=get_volh()


    if not place:
        st.info("")
        return
    
    for row in place:

        id, colh, detail, hours = row

        col1, col2= st.columns([1,2])


        with col1:
            st.markdown(f"**{colh}**")
            st.write(f"Час: {hours} год.")

        with col2:
            st.write(f"{detail}")

        st.markdown("---")
    




