# from transformers import pipeline
#
# pipe = pipeline("text-to-speech", model="suno/bark-small")
# text = "[clears throat] This is a test ... and I just took a long pause."
# output = pipe(text)
#
# from IPython.display import Audio
# Audio(output["audio"], rate=output["sampling_rate"])



# Ensure audio values are within the valid range for 16-bit integer

# print(type(output["audio"]))
# output_path = "output_audio.wav"
# with open(output_path, "wb") as f:
#     f.write(output['audio'])





from transformers import AutoProcessor, BarkModel

processor = AutoProcessor.from_pretrained("../ModelFiles/Audio/Bark")
model = BarkModel.from_pretrained("../ModelFiles/Audio/Bark").to("cuda")

voice_preset = "v2/en_speaker_2"

inputs = processor("Hello, my dog is cute", voice_preset=voice_preset).to("cuda")

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()

import scipy

sample_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sample_rate, data=audio_array)

print("Audio saved successfully.")
# Audio(output["audio"], rate=output["sampling_rate"])
