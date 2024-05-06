import requests
from streamlit_mic_recorder import mic_recorder
import streamlit as st

url = "http://127.0.0.1:5000/audio/translations"

def callback():
    if st.session_state.AUDIO_output:
        audio_bytes = st.session_state.AUDIO_output['bytes']
        with open('myfile2.wav', mode='bw') as f:
            f.write(st.session_state.AUDIO_output["bytes"])
            st.audio(audio_bytes)
        files = {"file": open("myfile2.wav", mode="rb")}
        data = {
            "model_name": "medium"
        }
        with st.spinner('Loading...'):
            response = requests.post(url, files=files, data=data)
        st.write(response.json()["text"])

audio = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    format="webm",
    callback=callback,
    key="AUDIO"
)

