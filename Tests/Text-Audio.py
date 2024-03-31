from transformers import pipeline

pipe = pipeline("text-to-speech", model="suno/bark-small")
text = "[clears throat] This is a test ... and I just took a long pause."
output = pipe(text)

from IPython.display import Audio
Audio(output["audio"], rate=output["sampling_rate"])



# Ensure audio values are within the valid range for 16-bit integer

# print(type(output["audio"]))
# output_path = "output_audio.wav"
# with open(output_path, "wb") as f:
#     f.write(output['audio'])

print("Audio saved successfully.")
# Audio(output["audio"], rate=output["sampling_rate"])
