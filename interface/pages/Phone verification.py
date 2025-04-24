import streamlit as st
from PIL import Image
import interface.pages.helpers.numverify as numverify


def phone_verification_page():
    logo = Image.open("initialData/mts_logo_cmyk.png")
    st.set_page_config(
        page_title="МТС Техподдержка AI",
        page_icon=logo,
        layout="wide"
    )
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
        <h1 class="big-title">Проверка номера телефона</h1>
        """, unsafe_allow_html=True)
    
    with st.form("phone_form"):
        phone = st.text_input("Введите номер телефона:", 
                             placeholder="Без +7, просто 9261234567")
        country = st.selectbox("Код страны:", ["RU", "US", "KZ", "BY"], index=0)

        submitted = st.form_submit_button("Проверить", type="primary")
    
    if submitted:
        if not phone:
            st.warning("Пожалуйста, введите номер телефона")
            return
        
        try:
            with st.spinner("Проверяем номер..."):

                result = numverify.valid_phone_number(phone, country)

            if not result.get('valid'):
                st.error("❌ Неверный номер телефона")
                return
            
            st.success("✅ Номер действителен")
            
            info_html = f"""
            <div class="phone-info">
                <h4>Информация о номере:</h4>
                <p><b>Номер:</b> {result.get('number', 'N/A')}</p>
                <p><b>Международный формат:</b> {result.get('international_format', 'N/A')}</p>
                <p><b>Локальный формат:</b> {result.get('local_format', 'N/A')}</p>
                <hr>
                <p><b>Оператор:</b> {result.get('carrier', 'N/A')}</p>
                <p><b>Тип линии:</b> {result.get('line_type', 'N/A')}</p>
                <p><b>Локация:</b> {result.get('location', 'N/A')}</p>
                <hr>
                <p><b>Страна:</b> {result.get('country_name', 'N/A')}</p>
                <p><b>Код страны:</b> {result.get('country_code', 'N/A')}</p>
                <p><b>Префикс страны:</b> {result.get('country_prefix', 'N/A')}</p>
            </div>
            """
            
            st.markdown(info_html, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Ошибка при проверке номера: {str(e)}")


phone_verification_page()