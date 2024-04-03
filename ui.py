import streamlit as st
from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

title = st.text_input('AI Reactor Engineer', placeholder='Enter here...')

if title:  # Only proceed if the user has entered something
    response = remote_chain.invoke({
        "input": title,
        # Use the last 10 messages from the session state chat history
        "chat_history": st.session_state.chat_history[-10:]
    })
    outp = response['output']

    # Add user and AI messages to the session state chat history
    st.session_state.chat_history.append({"content": title, "role": "user"})
    st.session_state.chat_history.append({"content": outp, "role": "ai"})

    st.write(outp)