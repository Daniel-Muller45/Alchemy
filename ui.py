import streamlit as st
from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000")

st.title("AI Reactor Engineer")

# Initialize chat history in the session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    with st.chat_message("assistant"):
        st.markdown('Hi I\'m Alchemy, your reactor engineering assistant. Please ask me any questions.')

# Display chat messages from history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
user_input = st.chat_input("Enter your query here...")

if user_input:  # Proceed if the user has entered something
    # Add user message to chat history
    st.session_state.chat_history.append({"content": user_input, "role": "user"})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call the remote AI engine
    response = remote_chain.invoke({
        "input": user_input,
        # Use the last 10 messages from the chat history
        "chat_history": st.session_state.chat_history[-10:]
    })

    # Extract the AI's response from the output
    ai_response = response['output']

    # Display AI message in the chat
    with st.chat_message("ai"):
        st.markdown(ai_response)

    # Add AI message to chat history
    st.session_state.chat_history.append({"content": ai_response, "role": "ai"})
