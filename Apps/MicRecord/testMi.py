from streamlit_mic_recorder import mic_recorder
import streamlit as st

def callback():
    if st.session_state.AUDIO_output:
        audio_bytes = st.session_state.AUDIO_output['bytes']
        with open('myfile2.wav', mode='bw') as f:
            f.write(st.session_state.AUDIO_output["bytes"])
        st.audio(audio_bytes)


audio = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    format="webm",
    callback=callback,
    key="AUDIO"
)

