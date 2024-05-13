import streamlit as st
import cohere

# An example LLM chatbot using Cohere API and Streamlit
# Adapted from the StreamLit OpenAI Chatbot example - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

with st.sidebar:
    # if hasattr(st, 'secrets'):
    #     if 'COHERE_API_KEY' in st.secrets:
    #         cohere_api_key = st.secrets['COHERE_API_KEY']
    # else:
    cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

st.title("💬 Chat with Mr. Nolan")

# Set initial message
initial_message = "G'day! I'm Graham Nolan, a computer science teacher from Australia. I studied software engineering and now teach at Hong Kong International School. Feel free to ask me anything about coding, technology, or my experiences!"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "text": initial_message}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

if prompt := st.chat_input():
    if not cohere_api_key:  
        st.info("Please add your Cohere API key to continue.")
        st.stop()

    client = cohere.Client(api_key=cohere_api_key)
    st.chat_message("user").write(prompt)
    response = client.chat(model="command-r", 
                           chat_history=st.session_state.messages,
                           message=prompt)
    st.session_state.messages.append({"role": "user", "text": prompt})
    msg = response.text
    st.session_state.messages.append({"role": "assistant", "text": msg})
    st.chat_message("assistant").write(msg)