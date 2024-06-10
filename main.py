import streamlit as st
from search import search

pip install sentence-transformers

def handle_query(query):
    if 'спасибо' in query.lower() or 'благодар' in query.lower():
        response = 'Рад помочь! Чтобы изменить запрос или найти что-то еще, нажмите "Новый поиск".'
    elif len(query.split()) < 3:
        response = 'К сожалению, запрос слишком короткий. Уточните, пожалуйста.'
    else:
        response = search(query)
    return response




st.title("ВШЭ ДПО Бот")

if st.button("Новый поиск"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.chat_message("assistant"):
    st.write("Здравствуйте! Я бот-навигатор Дополнительного Профессионального Образования Высшей Школы Экономики. Я помогу подобрать курс, исходя из ваших интересов. Пожалуйста, расскажите, что вы хотели бы изучить?")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = handle_query(prompt)
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

