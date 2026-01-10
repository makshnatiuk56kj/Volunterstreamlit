# all_vol.py

import streamlit as st
from db import get_volunteers
from PIL import Image
import io

def print_vol():
    st.title("Перегляд волонтерської діяльності")

    volunteers = get_volunteers()

    if not volunteers:
        st.info("Поки що немає жодного запису.")
        return

    for vol in volunteers:
        # 6 значень: id, name, hours, category, description, photo
        id, name, hours, category, description, photo_bytes = vol

        col1, col2 = st.columns([2, 1])  # ліва колонка ширша

        with col1:
            st.markdown(f"**{name}** — {hours} годин — *{category}*")
            st.write(description)

        with col2:
            if photo_bytes:
                image = Image.open(io.BytesIO(photo_bytes))
                image.thumbnail((200, 200))  # пропорції зберігаються
                st.image(image, width=200)   # спосіб задати ширину

        st.markdown("---")
