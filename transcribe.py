import whisper

model = whisper.load_model("small")

result = model.transcribe("farmer_voice.wav")   # detects the language automatically
print("Language detected:", result["language"])
print("Aapne kaha:", result["text"])
