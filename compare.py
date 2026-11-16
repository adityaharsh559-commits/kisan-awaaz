import time
import whisper

AUDIO = "farmer_voice.wav"
HINT = "किसान की फसल की समस्या: गेहूं, चावल, पत्ते पीले, कीड़े, खाद, सिंचाई, बीज।"
MODELS = ["small", "medium"]   # medium downloads about 1.5 GB the first time

for name in MODELS:
    print(f"\n=== Model: {name} ===")
    model = whisper.load_model(name)

    start = time.time()
    plain = model.transcribe(AUDIO, language="hi")
    print(f"Without hint ({time.time() - start:.0f}s): {plain['text']}")

    start = time.time()
    hinted = model.transcribe(AUDIO, language="hi", initial_prompt=HINT)
    print(f"With hint    ({time.time() - start:.0f}s): {hinted['text']}")