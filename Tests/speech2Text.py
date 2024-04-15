# import whisper
#
# model = whisper.load_model("medium")
# result = model.transcribe("../ECDLR.m4a", initial_prompt="Diez Hordenes, Dalinar, Roshar", language=None, task="transcribe")
# print(result)
# print(whisper.available_models())




from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
import torch

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
# pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2", device="cuda")
# transcription = pipe("../ECDLR.m4a")
# print(transcription)

model_id = "openai/whisper-large-v2"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to("cuda")

processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device="cuda"
)

x = pipe("./ECDLR.mp3", generate_kwargs={"prompt": "Roshar"})
print(x)
# import whisper
#
# model = whisper.load_model("base").to("cuda")
#
# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("../ECDLR.m4a")
# audio = whisper.pad_or_trim(audio)
#
# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)
#
# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")
#
# # decode the audio
# options = whisper.DecodingOptions()
# result = whisper.decode(model, mel, options)
#
# # print the recognized text
# print(result.text)
