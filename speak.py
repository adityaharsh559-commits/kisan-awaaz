import os
from gtts import gTTS


def speak(text, lang="hi", filename="answer.mp3"):
    """Convert text to speech and play it."""
    gTTS(text=text, lang=lang).save(filename)
    os.startfile(filename)   # opens the default audio player (Windows)