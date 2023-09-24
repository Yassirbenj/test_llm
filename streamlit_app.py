import openai
import streamlit as st

st.title("ChatGPT-like clone")

openai.api_key = st.secrets["openai"]

with st.form("input form"):
    st.write("<h3>Enter the customer personae ✨</h3>", unsafe_allow_html=True)
    customer_persona = st.text_input("Enter the customer persona:")

    if st.form_submit_button("Initiate discussion"):
        if customer_persona is not None:
            messages = [
                {"role": "system", "content": customer_persona},
            ]
            
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        
        if "messages" not in st.session_state:
            st.session_state.messages = messages
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
if prompt := st.chat_input("What is up?"):
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
            messages=conversation,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
