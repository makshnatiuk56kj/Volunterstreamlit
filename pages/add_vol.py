# add_vol.py

import streamlit as st
import db


def add_vol():
    db.init_db() # переконуємось, що таблиця існує
    st.title("Додати новий запис",text_alignment="center")
 
    if not st.session_state.get('authenticated'):
        st.error("Потрібна авторизація")
        return

    current_user_name = st.session_state.get('name')          # Повне ім'я з users таблиці

    if not current_user_name:
        st.error("Не вдалося отримати ваше ім'я. Спробуйте увійти повторно.")
        return

    # Показати ім'я, але не можна змінити
    name = st.text_input("ПІБ волонтера", value=current_user_name, disabled=True)

   
    hours = st.number_input("Години", min_value=1, max_value=100)

    # Вибір категорії
    category = st.selectbox("Оберіть категорію волонтерської діяльності", db.volunteer_categories)

    # Якщо вибрано "Інше", даємо текстове поле
    if category == "Інше":
        other_category = st.text_input("Вкажіть власну категорію")
        category = other_category if other_category else None

    description = st.text_area("Короткий опис діяльності")
    photo = st.file_uploader("Завантажте фото", type=["jpg", "jpeg", "png"])
    
    if st.button("Зберегти", key="save_volunteer"):
        if not name or not hours:
            st.error("ПІБ та години обов'язкові")
            return

        photo_bytes = photo.read() if photo else None
        db.add_volunteer(name, hours, category, description, photo_bytes)

        st.success("Діяльність успішно додана!")
        st.write(f"ПІБ: {name}")
        st.write(f"Години: {hours}")
        st.write(f"Категорія: {category}")
        st.write(f"Опис: {description}")
        if photo:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(photo_bytes))
            image.thumbnail((200,200))
            st.image(image, width=200)