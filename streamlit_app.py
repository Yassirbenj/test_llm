import openai
import streamlit as st

st.title("Customer simulator")

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
    st.write (conversation)

# Add an input field to collect the message for evaluation
evaluation_message = st.text("Evaluate this sales conversation by main factors")

# When the user submits an evaluation message, send it to ChatGPT for evaluation
if st.button("Evaluate"):
    if evaluation_message:
        #st.write(st.session_state.messages)
        # Create a conversation with the evaluation message
        evaluation_conversation = st.session_state.messages + [{"role": "user", "content": evaluation_message}]
        
        # Send the evaluation message to ChatGPT
        evaluation_response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=evaluation_conversation,
        )
        
        # Display the evaluation response
        st.write("Evaluation Response:")
        st.write(evaluation_response.choices[0].message["content"])
        
