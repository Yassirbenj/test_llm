import openai
import streamlit as st

st.title("ChatGPT-like clone")

openai.api_key = st.secrets["openai"]

st.sidebar.markdown("### Customer Persona")
customer_persona = st.sidebar.text_area("Enter the customer persona:")

if customer_persona is not None:
    system_message = {"role": "system", "content": customer_persona}

    # Add the system message to the messages list
    messages = [system_message]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = messages

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

        # Include the customer persona content in the initial message
        initial_message = st.session_state.messages[0]["content"]  # Get the customer persona
        conversation_messages = st.session_state.messages[1:]  # Exclude the customer persona

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": initial_message},  # Include customer persona
                *conversation_messages,  # Include other conversation messages
                {"role": "user", "content": prompt},  # Include user input
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
