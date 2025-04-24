import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
logo = Image.open("initialData/mts_logo_cmyk.png")
st.set_page_config(
    page_title="МТС Техподдержка AI",
    page_icon=logo,
    layout="wide"
)
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    try:
        logo = Image.open("initialData/mts_logo_cmyk.png")
        st.image(logo, width=100)
    except:
        st.warning("Логотип не найден")

with col2:
    st.markdown("""
    <style>
        .big-title {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            margin-bottom: 30px !important;
        }
    </style>
    <h1 class="big-title">Пользователи системы</h1>
    """, unsafe_allow_html=True)

# замените на данные из БД
@st.cache_data
def load_users_data():
    users = pd.DataFrame({
        'ID': range(1, 21),
        'Имя': [f'Пользователь {i}' for i in range(1, 21)],
        'Телефон': [f'+7 (9{str(np.random.randint(10,99))}) {np.random.randint(100,999)}-{np.random.randint(10,99)}-{np.random.randint(10,99)}' for _ in range(20)],
        'Удовлетворённость (%)': np.random.randint(-100, 101, 20),
        'Дата регистрации': pd.date_range('2025-01-01', periods=20)
    })
    return users

users_df = load_users_data()

def color_satisfaction(val):
    color = 'red' if val < 0 else 'green' if val > 50 else 'orange'
    return f'background-color: {color}; color: white'

col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("Поиск по имени или телефону:")

with col2:
    satisfaction_filter = st.slider(
        "Фильтр по удовлетворённости:",
        min_value=-100,
        max_value=100,
        value=(-100, 100)
    )

filtered_df = users_df[
    (users_df['Удовлетворённость (%)'] >= satisfaction_filter[0]) & 
    (users_df['Удовлетворённость (%)'] <= satisfaction_filter[1])
]

if search_query:
    filtered_df = filtered_df[
        filtered_df['Имя'].str.contains(search_query, case=False) |
        filtered_df['Телефон'].str.contains(search_query, case=False)
    ]

st.dataframe(
    filtered_df.style.applymap(color_satisfaction, subset=['Удовлетворённость (%)']),
    column_config={
        "Удовлетворённость (%)": st.column_config.ProgressColumn(
            "Удовлетворённость",
            help="Уровень удовлетворённости от -100 до 100%",
            format="%d%%",
            min_value=-100,
            max_value=100,
        ),
        "Дата регистрации": st.column_config.DateColumn(
            "Дата регистрации",
            format="DD.MM.YYYY"
        )
    },
    hide_index=True,
    use_container_width=True
)


st.subheader("Статистика")
col1, col2, col3 = st.columns(3)

try:
    col1.metric("Всего пользователей", len(users_df))
    
    if len(filtered_df) == 0:
        col2.metric("Средняя удовлетворённость", "N/A")
        col3.metric("Доля положительных оценок", "N/A")
        st.warning("Нет данных для отображения по текущим фильтрам")
    else:
        avg_satisfaction = filtered_df['Удовлетворённость (%)'].mean()
        positive_percentage = (len(filtered_df[filtered_df['Удовлетворённость (%)'] > 0]) / len(filtered_df)) * 100
        
        col2.metric("Средняя удовлетворённость", f"{avg_satisfaction:.1f}%")
        col3.metric("Доля положительных оценок", f"{positive_percentage:.1f}%")

except Exception as e:
    st.error(f"Ошибка при расчете статистики: {str(e)}")
    col2.metric("Средняя удовлетворённость", "Ошибка")
    col3.metric("Доля положительных оценок", "Ошибка")