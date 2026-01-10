# charts.py

import streamlit as st
import pandas as pd
import altair as alt
from db import get_volunteers

def plot_hours_by_category():
    """Відображає графік суми годин по категоріях"""
    volunteers = get_volunteers()

    if not volunteers:
        st.info("Поки що немає жодного запису для відображення графіку")
        return

    # Створюємо DataFrame
    df = pd.DataFrame(volunteers, columns=["id", "name", "hours", "category", "description", "photo"])
    
    # Групуємо по категорії та сумуємо години
    df_grouped = df.groupby("category", as_index=False)["hours"].sum()

    # Створюємо стовпчиковий графік Altair
    chart = alt.Chart(df_grouped).mark_bar(color="#4CAF50").encode(
        x=alt.X("category", sort="-y", title="Категорія волонтерської діяльності"),
        y=alt.Y("hours", title="Сума годин"),
        tooltip=["category", "hours"]
    ).properties(
        width=700,
        height=400,
        title="Графік кількості годин по категоріях"
    )

    st.altair_chart(chart)



def show_top_category():
    volunteers = get_volunteers()
    
    if not volunteers:
        st.info("Поки що немає жодного запису для аналізу")
        return

    # Створюємо DataFrame
    df = pd.DataFrame(volunteers, columns=["id", "name", "hours", "category", "description", "photo"])

    # Групуємо по категорії та сумуємо години
    df_grouped = df.groupby("category", as_index=False)["hours"].sum()

    # Знаходимо категорію з максимальною сумою годин
    top_row = df_grouped.loc[df_grouped["hours"].idxmax()]

    st.info(f"Категорія з найбільшою кількістю годин: **{top_row['category']}** — {top_row['hours']} годин")


# import streamlit as st
# import pandas as pd
# import altair as alt
# from db import get_volunteers


# def plot_hours_by_category():
#     """Відображає графік активності волонтерів з можливістю вибору типу графіку"""
#     volunteers = get_volunteers()

#     if not volunteers:
#         st.info("Поки що немає жодного запису для відображення графіку")
#         return

#     # Створюємо DataFrame
#     df = pd.DataFrame(volunteers, columns=["id", "name", "hours", "category", "description", "photo"])

#     # Запитуємо користувача, який графік він хоче бачити
#     chart_type = st.selectbox(
#         "Виберіть тип графіку",
#         ["Стовпчиковий", "Лінійний", "Круговий", "Heatmap"]
#     )

#     if chart_type == "Стовпчиковий":
#         df_grouped = df.groupby("category", as_index=False)["hours"].sum()
#         chart = alt.Chart(df_grouped).mark_bar(color="#4CAF50").encode(
#             x=alt.X("category", sort="-y", title="Категорія"),
#             y=alt.Y("hours", title="Сума годин"),
#             tooltip=["category", "hours"]
#         )

#     elif chart_type == "Лінійний":
#         # Для прикладу, відображаємо суму годин по категорії як лінію
#         df_grouped = df.groupby("category", as_index=False)["hours"].sum()
#         chart = alt.Chart(df_grouped).mark_line(point=True, color="#2196F3").encode(
#             x="category",
#             y="hours",
#             tooltip=["category", "hours"]
#         )

#     elif chart_type == "Круговий":
#         df_grouped = df.groupby("category", as_index=False)["hours"].sum()
#         chart = alt.Chart(df_grouped).mark_arc().encode(
#             theta="hours:Q",
#             color="category:N",
#             tooltip=["category", "hours"]
#         )

#     elif chart_type == "Heatmap":
#         # Групуємо за категоріями та іменами
#         df_grouped = df.groupby(["category", "name"], as_index=False)["hours"].sum()
#         chart = alt.Chart(df_grouped).mark_rect().encode(
#             x=alt.X("name:N", title="Волонтер"),
#             y=alt.Y("category:N", title="Категорія"),
#             color=alt.Color("hours:Q", title="Години"),
#             tooltip=["name", "category", "hours"]
#         )

#     chart = chart.properties(width=700, height=400)
#     st.altair_chart(chart)



# def show_top_category():
#     volunteers = get_volunteers()
    
#     if not volunteers:
#         st.info("Поки що немає жодного запису для аналізу")
#         return

#     df = pd.DataFrame(volunteers, columns=["id", "name", "hours", "category", "description", "photo"])
    
#     if df.empty:
#         st.info("Немає даних для аналізу")
#         return

#     df_grouped = df.groupby("category", as_index=False)["hours"].sum()
#     top_row = df_grouped.loc[df_grouped["hours"].idxmax()]

#     st.info(f"Категорія з найбільшою кількістю годин: **{top_row['category']}** — {top_row['hours']} годин")
