import queue
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DEVICE = None   # None = default mic. To use another mic, put its number from the device list here, e.g. DEVICE = 1
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("Warning:", status)
    q.put(indata.copy())

input("Taiyar hone par Enter dabaiye, phir bolna shuru kijiye... ")
print("Recording chal rahi hai... bolna khatam hone par dobara Enter dabaiye.")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32",
                    device=DEVICE, callback=callback):
    input()

chunks = []
while not q.empty():
    chunks.append(q.get())

audio = np.concatenate(chunks, axis=0).flatten()

peak = float(np.max(np.abs(audio)))
print(f"Loudness level: {peak:.3f}  (0.1 to 0.9 is good)")

if peak < 0.01:
    print("Awaaz lagbhag silent hai. Mic galat ho sakta hai ya mute hai.")
else:
    audio = audio / peak * 0.9   # make quiet recordings louder

write("farmer_voice.wav", SAMPLE_RATE, (audio * 32767).astype(np.int16))
print(f"Recording save ho gayi: farmer_voice.wav ({len(audio) / SAMPLE_RATE:.1f} seconds)")