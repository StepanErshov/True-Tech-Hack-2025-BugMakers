import streamlit as st
from api.main import post_chat_completion
import time
from PIL import Image
import audio_recorder_streamlit as ars
import os
from datetime import datetime

logo = Image.open("initialData/mts_logo_cmyk.png")
st.set_page_config(
    page_title="МТС Техподдержка AI",
    page_icon=logo,
    layout="wide"
)


def hide_streamlit_conf():
    """Скрывает элементы интерфейса Streamlit"""
    hide_streamlit_style = """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        div[data-testid="stToolbar"] {visibility: hidden;}
        div[data-testid="stStatusWidget"] {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


hide_streamlit_conf()

col1, col2 = st.columns([1, 4])
with col1:
    try:
        logo = Image.open("initialData/mts_logo_cmyk.png")
        st.image(logo, width=100)
    except:
        st.warning("Логотип не найден")

with col2:
    st.title("Hackaton MTS True Tech")

st.markdown(
    """
<style>
    .response-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .loading-spinner {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

os.makedirs("audio_files", exist_ok=True)

st.subheader("Запись аудио")
with st.expander("Важные заметки о записи"):
    st.write("""
    1. Разрешите доступ к микрофону
    2. Не переключайте вкладки во время записи
    3. Для остановки нажмите на микрофон еще раз
    """)

audio_bytes = ars.audio_recorder(
    text="Нажмите для записи",
    recording_color="#b51509",
    neutral_color="#f0190a",
    icon_name="microphone",
    icon_size="2x",
    pause_threshold=60.0 
)

if audio_bytes:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"audio_files/recording_{timestamp}.wav"
    
    with open(audio_filename, "wb") as f:
        f.write(audio_bytes)
    
    st.audio(audio_bytes, format="audio/wav")
    st.success(f"Аудио сохранено как {audio_filename}")

    # Можно добавить здесь обработку аудио через API, если нужно
    # Например, преобразование речи в текст
    # Рамзан, работа для тебя

with st.form("chat_form"):
    prompt = st.text_area(
        "Введите ваш запрос:", height=150, placeholder="Напишите ваш вопрос здесь..."
    )

    col1, col2 = st.columns([4, 1])
    with col1:
        submitted = st.form_submit_button("Отправить текст", type="primary")
    with col2:
        audio_submitted = st.form_submit_button("Отправить аудио", type="primary")

if submitted and prompt:
    response_container = st.empty()

    with response_container.container():
        st.markdown(
            '<div class="loading-spinner">⏳ Обработка запроса...</div>',
            unsafe_allow_html=True,
        )

    try:
        start_time = time.time()
        response = post_chat_completion(promt=prompt)
        processing_time = time.time() - start_time

        if isinstance(response, dict) and "choices" in response:
            answer = response["choices"][0]["message"]["content"]
        else:
            answer = str(response)

        formatted_response = f"""
        <div class="response-box">
            <h4>Ответ:</h4>
            <p>{answer}</p>
            <hr>
            <small>Время обработки: {processing_time:.2f} сек</small>
        </div>
        """

        response_container.markdown(formatted_response, unsafe_allow_html=True)

    except Exception as e:
        response_container.error(f"Произошла ошибка: {str(e)}")
elif submitted and not prompt:
    st.warning("Пожалуйста, введите текст запроса")

if audio_submitted:
    if audio_bytes:
        # Здесь можно добавить обработку аудио
        # Например, преобразование в текст и отправку в API
        # Рамзан, работа для тебя
        st.info("Функциональность обработки аудио будет добавлена здесь")
    else:
        st.warning("Пожалуйста, сначала запишите аудио")