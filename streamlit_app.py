import openai
import streamlit as st

st.title("ChatGPT-like clone")

openai.api_key = st.secrets["openai"]

st.sidebar.markdown("### Customer Persona")
customer_persona = st.sidebar.text_area("Enter the customer persona:")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Add user input to the messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Create the conversation by including the customer persona as part of the initial message
        conversation = [{"role": "system", "content": customer_persona}]
        conversation.extend(st.session_state.messages)  # Include other conversation messages
        conversation.append({"role": "user", "content": prompt})  # Include user input

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=conversation,  # Use the extended conversation
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
