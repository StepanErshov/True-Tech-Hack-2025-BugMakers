import streamlit as st
import json
from Models.orchestra import LatestAiDevelopmentCrew
from datetime import datetime
from config import *
from PIL import Image
import os

os.environ["OPENAI_API_KEY"] = KEY
os.environ["CREWAI_EMBEDDING_MODEL"] = URL_EMBEDDINGS
icon = Image.open("initialData/mts_logo_cmyk.png")
st.set_page_config(
    page_title="МТС Техподдержка AI",
    page_icon=icon,
    layout="wide"
)

st.title("📞 МТС Техподдержка AI Оркестратор")
st.markdown("""
Этот инструмент помогает сотрудникам техподдержки МТС анализировать запросы клиентов и генерировать ответы.
""")

with st.sidebar:
    st.header("Настройки")
    model_provider = st.selectbox(
        "Провайдер модели",
        ["Ollama (локальный)", "OpenAI", "Anthropic"],
        index=0
    )
    
    if model_provider == "Ollama (локальный)":
        model_name = st.selectbox(
            "Модель",
            ["llama3", "mistral", "neural-chat"],
            index=0
        )
    else:
        model_name = st.text_input("Имя модели", "gpt-4")
    
    verbose_mode = st.checkbox("Подробный вывод", value=True)
    st.markdown("---")
    st.markdown("**О приложении**")
    st.markdown("""
    Это демонстрация AI-оркестратора для техподдержки МТС.
    Система анализирует запрос клиента по нескольким аспектам:
    - Намерение клиента
    - Эмоциональное состояние
    - Рекомендуемое решение
    - CRM отчет
    """)

with st.form("prompt_form"):
    client_query = st.text_area(
        "Запрос клиента:",
        placeholder="Опишите проблему или вопрос клиента...",
        height=150,
        value="не работает приложение связи, что мне делать, к кому мне обращаться?"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("Отправить запрос", type="primary")
    with col2:
        clear_button = st.form_submit_button("Очистить")

if submit_button:
    try:
        with st.spinner("Анализируем запрос клиента..."):
            crew_instance = LatestAiDevelopmentCrew()
            crew = crew_instance.crew()
            
            result = crew.kickoff(inputs={"topic": client_query})
            
            output_data = {
                'task_description': client_query,
                'execution_time': datetime.now().isoformat(),
                "results": {
                    "intent_analysis": str(crew.tasks[0].output),
                    "solution_proposal": str(crew.tasks[1].output),
                    "emotion_analysis": str(crew.tasks[2].output),
                    "action_s_agent": str(crew.tasks[3].output),
                    "summary_agent": str(crew.tasks[4].output),
                    "qa_agent": str(crew.tasks[5].output)
                }
            }
            
            st.success("Анализ завершен!")
            
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📌 Намерение", "🔧 Решение", "😊 Эмоции", 
                "📝 Действия", "📊 CRM отчет", "💬 Советы по общению"
            ])
            
            with tab1:
                st.subheader("Анализ намерения клиента")
                st.markdown(f"**Результат:** {crew.tasks[0].output}")
                
            with tab2:
                st.subheader("Рекомендуемое решение")
                st.markdown(f"**Решение:** {crew.tasks[1].output}")
                
            with tab3:
                st.subheader("Эмоциональный анализ")
                st.markdown(f"**Состояние клиента:** {crew.tasks[2].output}")
                
            with tab4:
                st.subheader("Рекомендуемые действия")
                st.markdown(f"**План действий:** {crew.tasks[3].output}")
                
            with tab5:
                st.subheader("CRM отчет")
                st.json(crew.tasks[4].output)
                
            with tab6:
                st.subheader("Советы по общению с клиентом")
                st.markdown(f"**Рекомендации:** {crew.tasks[5].output}")
            
            json_result = json.dumps(output_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="Скачать полный отчет (JSON)",
                data=json_result,
                file_name=f"mts_support_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
    except Exception as e:
        st.error(f"Произошла ошибка: {str(e)}")
        error_data = {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "input": client_query
        }
        st.json(error_data)

if clear_button or not submit_button:
    st.markdown("### Примеры запросов:")
    examples = st.columns(3)
    
    with examples[0]:
        st.markdown("""
        **Техническая проблема**  
        "У меня не работает интернет на телефоне, хотя деньги на счету есть"
        """)
        
    with examples[1]:
        st.markdown("""
        **Биллинг**  
        "Мне пришло смс о списании 500 рублей за подписку, которую я не активировал"
        """)
        
    with examples[2]:
        st.markdown("""
        **Жалоба**  
        "Я уже третий раз звоню по поводу этой проблемы, но ничего не решается!"
        """)