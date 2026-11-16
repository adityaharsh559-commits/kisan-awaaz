import queue
import numpy as np
import sounddevice as sd
import whisper
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
MODEL_NAME = "medium"
HINT_HI = "किसान की फसल की समस्या: मेरे गेहूं के पत्ते पीले, कीड़े, खाद, सिंचाई, बीज।"

print("Model load ho raha hai...")
model = whisper.load_model(MODEL_NAME)


def record_audio(filename="farmer_voice.wav"):
    """Records until Enter is pressed twice. Returns the file name, or None if silent."""
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    input("Taiyar hone par Enter dabaiye, phir bolna shuru kijiye... ")
    print("Recording chal rahi hai... bolna khatam hone par dobara Enter dabaiye.")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
        input()

    chunks = []
    while not q.empty():
        chunks.append(q.get())
    audio = np.concatenate(chunks, axis=0).flatten()

    peak = float(np.max(np.abs(audio)))
    if peak < 0.01:
        print("Awaaz lagbhag silent hai. Mic check kijiye.")
        return None

    audio = audio / peak * 0.9
    write(filename, SAMPLE_RATE, (audio * 32767).astype(np.int16))
    return filename


def transcribe(filename, language="hi"):
    """Turns the audio file into text. language=None lets Whisper detect it."""
    prompt = HINT_HI if language == "hi" else None
    result = model.transcribe(filename, language=language, initial_prompt=prompt)
    return result["text"].strip(), result["language"]


def listen(language="hi"):
    """Record the farmer's voice and return (text, language)."""
    filename = record_audio()
    if filename is None:
        return "", language
    return transcribe(filename, language)


if __name__ == "__main__":
    text, lang = listen("hi")
    print("Language:", lang)
    print("Aapne kaha:", text)
    with open("last_result.txt", "w", encoding="utf-8") as f:
        f.write(text)