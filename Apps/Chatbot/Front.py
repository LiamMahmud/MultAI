import base64
import os
import time

import requests
from PIL import Image
from pathlib import Path
import streamlit as st

ICON = "./BotFaceSinFondo.png"
InfoIcon = "./InfoIcon.png"
url = 'http://127.0.0.1:5000/chat/completions'

model_config = {"model_name": "Mistral-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
      "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
     "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
     "repeat_penalty": 1.1, "stop": None
     }

# Configuraciones de la página
st.set_page_config(
    page_title="Smart Recruit",
    page_icon=Image.open(ICON),
    layout="wide"
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)
st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .logo-img {
        width: 60px;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Replicate Credentials
with st.sidebar:
    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(ICON, "rb").read()).decode()}">
            <h1 style='text-align: center; color: white; font-size: 40px;'>Smart Recruit</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    # # st.markdown('# 🦙💬 Llama 2 Chatbot')
    # if 'REPLICATE_API_TOKEN' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     replicate_api = st.secrets['REPLICATE_API_TOKEN']
    # else:
    #     replicate_api = st.text_input('Enter Replicate API token:', type='password')
    #     if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    #         st.success('Proceed to entering your prompt message!', icon='👉')
    # os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        model_name = selected_model
    elif selected_model == 'Llama2-13B':
        model_name = selected_model
    st.sidebar.markdown(f"""
    <style>
        .tooltip {{
            position: relative;
            display: inline-block;
        }}

        .tooltip .info-icon {{
            width: 20px;
            height: 20px;
            display: inline-block;
            background-image: url('data:image/png;base64,{base64.b64encode(open(InfoIcon, "rb").read()).decode()}');
            background-size: cover;
            margin-left: 0px;
        }}

        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div class="tooltip">
            <span>Temperature</span>
            <div class="info-icon"></div>
            <span class="tooltiptext">Adjust the temperature parameter</span>
        </div>: <br>""", unsafe_allow_html=True)
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01, label_visibility='collapsed')
    st.sidebar.markdown("""
            <div class="tooltip">
                <span>Top P</span>
                <div class="info-icon"></div>
                <span class="tooltiptext">Adjust the top P parameter</span>
            </div>: <br>""", unsafe_allow_html=True)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01, label_visibility='collapsed')
    st.sidebar.markdown("""
            <div class="tooltip">
                <span>Max Length</span>
                <div class="info-icon"></div>
                <span class="tooltiptext">Adjust the maximum length parameter</span>
            </div>: <br>""", unsafe_allow_html=True)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8, label_visibility='collapsed')
    # st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    avatar = "💬" if message["role"] == "user" else ICON  # Change the avatar based on the role, they must match to the ones generating
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
# def generate_llama2_response(prompt_input):
#     string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
#     for dict_message in st.session_state.messages:
#         if dict_message["role"] == "user":
#             string_dialogue += "User: " + dict_message["content"] + "\n\n"
#         else:
#             string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
#     output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
#                            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
#                                   "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
#     return output

def generate_response(prompt):
    response = requests.post(url, json=model_config)
    print(response.json()["choices"][0]["message"])
    return response.json()["choices"][0]["message"]["content"]

# User-provided prompt
if prompt := st.chat_input(disabled=not True):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="💬"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            model_config["prompt"] = [{"role": "user", "content": prompt}]
            response = generate_response(prompt)
            placeholder = st.empty()
            full_response = ''
            # probar elemento write_stream
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)















# st.markdown(
#     """
#     <style>
#     footer {visibility: hidden;}
#     .stDeployButton {
#             visibility: hidden;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# # Titulo
#
# LOGO_IMAGE = "BotFaceSinFondo.png"
#
# st.markdown(
#     """
#     <style>
#     .container {
#         display: flex;
#         align-items: center;
#         justify-content: center; /* Add this line to center horizontally */
#         margin: auto; /* Add this line to center horizontally */
#     }
#     .logo-img {
#         width: 100px;
#         height: auto;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# st.markdown(
#     f"""
#     <div class="container">
#         <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
#         <h1 style='text-align: center; color: grey;'>OmniConverse</h1>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


