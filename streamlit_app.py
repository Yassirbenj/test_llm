import openai
import streamlit as st
from gtts import gTTS
import os

st.title("Customer simulator")

openai.api_key = st.secrets["openai"]

with st.form("input form"):
    st.write("<h3>Enter the customer personae ✨</h3>", unsafe_allow_html=True)
    industry=st.text_input("Enter customer industry:")
    position=st.text_input("Enter customer position:")
    company_char=st.text_input("Enter company characterstics:")
    pain_points=st.text_input("Enter pain points:")
    decision_making_factors=st.text_input("Enter some decision factors:")
    personnality=st.text_input("Enter some key personnality characteristics:")
    customer_persona = f"You are a customer receiving a call from a sales person. you have the following characterstics."
    customer_persona += f"You are in the industry of {industry}, you have the position of {position}."
    customer_persona += f"The main characteristics of the company you are working for are {company_char}."
    customer_persona += f"The main pain points in your business are {pain_points} and your decision making factors are {decision_making_factors}." 
    customer_persona += f"your main personality trait are {personnality}."
    customer_persona += f"you respond briefly to the question. "
    

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
