import streamlit as st
import asyncio
from core.ai_engine import get_ai_review
from utils.helpers import read_uploaded_file, get_download_link

st.set_page_config(page_title="Pro Code Analyzer", layout="wide", page_icon="🛡️")

st.title("🛡️ Modular AI Code Analyzer")
st.caption("Аудит кода с использованием Mistral AI")

with st.sidebar:
    st.header("⚙️ Настройки")
    st_model = st.selectbox("Модель", ["mistral-small-latest", "mistral-medium-latest"])
    st.divider()
    st_mode = st.radio("Режим анализа", ["Стандартный", "Безопасность", "Оптимизация"])

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📥 Ввод кода")
    file = st.file_uploader("Выбрать файл .py", type=['py'])
    input_value = read_uploaded_file(file)
    code_input = st.text_area("Код для проверки:", value=input_value, height=450)
    run_btn = st.button("🚀 Запустить аудит", use_container_width=True, type="primary")

with col2:
    st.subheader("📊 Результат анализа")
    
    if run_btn:
        if not code_input.strip():
            st.warning("Пожалуйста, введите код!")
        else:
            with st.spinner("ИИ анализирует код..."):
                full_result = asyncio.run(get_ai_review(code_input, st_mode, st_model))
                st.markdown(full_result)
                st.download_button("📥 Скачать отчет", get_download_link(full_result), "audit.txt", use_container_width=True)
    else:
        st.info("Здесь появится отчет после нажатия кнопки слева.")