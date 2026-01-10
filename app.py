# app.py

import streamlit as st
from pages.add_vol import add_vol
from pages.all_vol import print_vol
from pages.charts import plot_hours_by_category, show_top_category
from dh import add_hd,print_dh
from db import init_db, init_db_users,create_admin_if_not_exists,get_total_hours,init_dh,register_user,authenticate_user,init_dh




# Конфігурація сторінки
st.set_page_config(
    page_title='Волонтер',
    page_icon='',
    layout='centered' # wide для таблиць і т.д. Вирівнює не по центру, а по лівому краю
)

# Ініціалізуємо сторінку
if 'page' not in st.session_state:
    st.session_state.page = "Головна"





st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;} 
    </style>
    """,
    unsafe_allow_html=True
)




st.markdown(
    """
    <style>
    /* Прибираємо верхній відступ сторінки */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }

    /* Прибираємо марджини для картинки */
    div[data-testid="stImage"] {
        margin-top: 0rem;
        margin-bottom: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)




col1,col2,col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png")







# Ініціалізація бази (викликаємо один раз при старті)
init_db()
init_db_users()
create_admin_if_not_exists()  # Створює admin/123, якщо його немає
init_dh()




if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False # користувач ще не увійшов
    st.session_state.username = None # ім'я користувача пусте, бо він ще не увійшов
    st.session_state.name = None # аналогічно для повного імені
    st.session_state.role = None # аналогічно для ролі користувача: він ще не увійшов

# Ініціалізуємо сторінку
if 'page' not in st.session_state:
    st.session_state.page = "Головна"

if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login' 


# Кнопки навігації
nav_buttons = ["Головна", "Наша діяльність", "Де волонтерити"] # завжди доступні всім користувачам кнопки

# додаткові кнопки для авторизованих користувачів
if st.session_state.authenticated:      # authenticated - True, якщо користувач увійшов
    nav_buttons.append("Додати діяльність")
if st.session_state.authenticated:
    nav_buttons.append("Вийти")
else:                                   # якщо користувач не увійшов, то відображаємо кнопку входу/реєстрації
    nav_buttons.append("Увійти / Зареєструватися")

# Відображаємо кнопки навігації в один рядок
cols = st.columns(len(nav_buttons))     # створюємо стільки колонок, скільки кнопок

# Тепер циклом перевіряємо яку кнопку користувач натиснув
for i, label in enumerate(nav_buttons): # ітеруємося по кнопках
    with cols[i]:                       # кожна кнопка в своїй колонці
        if st.button(label):            # якщо натиснута кнопка
            if label == "Вийти":        # якщо її напис "Вийти", то виходимо з акаунту, і міняємо сесію на початкові значення і головну сторінку
                st.session_state.authenticated = False
                st.session_state.username = st.session_state.name = st.session_state.role = None
                st.session_state.page = "Головна"
            elif label == "Увійти / Зареєструватися":   # якщо натиснута кнопка для входу/реєстрації, то переходимо на сторінку авторизації
                st.session_state.page = "Авторизація"
            else:
                st.session_state.page = label # інакше просто змінюємо сторінку на ту, що відповідає кнопці. Лишились тільки загальні кнопки

st.markdown("---")
















if st.session_state.page == "Головна":
    total_hours = get_total_hours()

    # Форматуємо число з пробілами (наприклад, 12 450)
    formatted_hours = f"{total_hours:,}".replace(",", " ")

    st.markdown(f"""
        <p style="text-align: center; font-size: 36px; font-weight: bold; color: #2c7a2c; margin-bottom: 0;">
            Волонтер — це ти!
        </p>
        <p style="text-align: center; font-size: 18px; margin-top: 8px; margin-bottom: 54px;">
            Кожна година змінює світ на краще.<br>
            Приєднуйся до спільноти, яка вже 
            наробила<strong style="color: #4CAF50; font-size: 24px;"> {formatted_hours} годин</strong> добра!
        </p>
        """, unsafe_allow_html=True)
    #show_top_category()
    plot_hours_by_category()

elif st.session_state.page == "Наша діяльність":
    print_vol()

elif st.session_state.page == "Де волонтерити":
    print_dh()
    if st.session_state.authenticated and st.session_state.role == "admin": # Якщо адміністратор увійшов
        add_hd()  # тільки адмін бачить форму додавання

elif st.session_state.page == "Додати діяльність":
    if not st.session_state.authenticated: # Якщо користувач не увійшов
        st.error("Увійдіть, щоб додавати записи")
        st.stop() # зупиняємо подальше виконання коду на цій сторінці
    
    add_vol() # Якщо користувач увійшов, показуємо форму додавання

elif st.session_state.page == "Авторизація": # Якщо обрана сторінка авторизації
    # Заголовок змінюється залежно від режиму
    st.header("Авторизація" if st.session_state.auth_mode == 'login' else "Реєстрація")

    # Основна форма (залежно від режиму)
    if st.session_state.auth_mode == 'login': # Якщо вибрано вхід, то відображаємо форму входу
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Ім'я користувача", key="login_username")
            password = st.text_input("Пароль", type="password", key="login_password")
            submitted = st.form_submit_button("Увійти", use_container_width=True)

            if submitted: # Якщо натиснута кнопка Увійти, то перевіряємо логін і пароль з БД
                success, name, role = authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True # міняємо сесійний стан,позначаємо, що користувач увійшов
                    st.session_state.username = username
                    st.session_state.name = name
                    st.session_state.role = role
                    st.session_state.page = "Головна" # Кидаємо користувача на головну сторінку
                    st.success(f"Вітаємо, {name}!")
                    st.rerun()
                else: # Якщо неуспішно, показуємо помилку
                    st.error("Неправильне ім'я користувача або пароль")

    else:  # registration
        with st.form("register_form", clear_on_submit=False):
            new_username = st.text_input("Ім'я користувача (логін)", key="reg_username")
            new_name = st.text_input("Повне ім'я", key="reg_name")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Пароль", type="password", key="reg_pass")
            new_password2 = st.text_input("Повторіть пароль", type="password", key="reg_pass2")

            submitted = st.form_submit_button("Зареєструватися", use_container_width=True)

            if submitted:
                if new_password != new_password2:
                    st.error("Паролі не співпадають")
                elif not all([new_username, new_name, new_email, new_password]):
                    st.error("Заповніть усі поля")
                else:
                    success = register_user(new_username, new_name, new_email, new_password)
                    if success:
                        st.success("Реєстрація успішна! Тепер можете увійти.")
                        st.session_state.auth_mode = 'login'
                        st.rerun()
                    else:
                        st.error("Такий логін або email вже використовується")

    # ── Блок перемикання режимів (завжди внизу) ───────────────────────────────
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Уже маю акаунт → Увійти",
            use_container_width=True,
            type="secondary" if st.session_state.auth_mode == 'login' else "primary"
        ):
            st.session_state.auth_mode = 'login'
            st.rerun()

    with col2:
        if st.button(
            "Новий користувач → Зареєструватися",
            use_container_width=True,
            type="secondary" if st.session_state.auth_mode == 'registration' else "primary"
        ):
            st.session_state.auth_mode = 'registration'
            st.rerun()


