import streamlit as st
from router import get_route
from faq import ingest_data, faq_chain
from pathlib import Path
from sql import sql_chain
from smalltalk import small_talk_chain

faq_path = Path(__file__).parent / "resources/ecommerce_faq.csv"
ingest_data(faq_path)

def ask(query):
    route = get_route(query)
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'small-talk':
        return small_talk_chain(query)
    else:
        return f'Please ask questions related to Flipkart policies and products, Thanks!'
st.set_page_config(page_title="Askie - E-commerce Chatbot", page_icon="🛍️", layout="centered")

st.markdown("## 🛍️ Welcome to **Askie** – Your E-Commerce Assistant")
st.markdown('<p>👋 Hi there! My name is <strong>Askie</strong>. How can I help you today?</p>', unsafe_allow_html=True)


if 'messages' not in st.session_state:
    st.session_state['messages']=[]

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.markdown(messages['content'])

query  = st.chat_input('💬   Write your query here..')

if query:
    with st.chat_message('user'):
        st.markdown(query)
    st.session_state['messages'].append({'role': 'user', 'content': query})

    response = ask(query)
    with st.chat_message('ai'):
        st.markdown(response)
    st.session_state['messages'].append({'role': 'ai', 'content': response})