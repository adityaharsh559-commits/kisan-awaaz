import unicodedata

# ---------- Words the farmer might say ----------
# Whisper spells Hindi words in different ways, so we list several variants.
CROP_WORDS = {
    "गेहूं": ["गेहूं", "गेंहू", "गेहु", "gehun", "gehu", "wheat"],
    "चावल": ["चावल", "धान", "chawal", "dhan", "rice", "paddy"],
    "टमाटर": ["टमाटर", "tamatar", "tomato"],
}

PROBLEM_WORDS = {
    "yellow": ["पीले", "पीला", "पीली", "पीलापन", "peele", "peela", "yellow"],
    "insects": ["कीड़े", "कीड़ा", "कीट", "इल्ली", "keede", "keeda", "insect", "pest"],
    "water": ["सूख", "मुरझा", "सिंचाई", "sukh", "murjha", "sinchai", "wilt"],
    "fertilizer": ["खाद", "उर्वरक", "khad", "fertilizer"],
}

# ---------- Advice ----------
# PLACEHOLDER TEXT: must be reviewed and replaced by an agriculture expert
# (e.g. a Krishi Vigyan Kendra) before the public launch.
ADVICE = {
    "yellow": "पत्तों का पीला होना कई कारणों से हो सकता है, जैसे पोषक तत्वों की कमी, ज़्यादा पानी या कोई रोग। "
              "अपने खेत की मिट्टी की जाँच करवाइए और नज़दीकी कृषि विज्ञान केंद्र से सलाह लीजिए।",
    "insects": "फसल में कीड़े दिखें तो पहले उनकी पहचान करवाइए। "
               "कोई भी कीटनाशक अपने आप न डालें, कृषि अधिकारी से सही दवा और मात्रा पूछिए।",
    "water": "पौधे सूख रहे हों तो खेत की नमी जाँचिए और ज़रूरत के हिसाब से सिंचाई कीजिए। "
             "ज़्यादा पानी भी नुकसान करता है, इसलिए पानी रुकने न दीजिए।",
    "fertilizer": "खाद की मात्रा मिट्टी की जाँच और फसल की अवस्था पर निर्भर करती है। "
                  "मिट्टी जाँच करवाकर कृषि विज्ञान केंद्र से सही मात्रा पूछिए।",
}

FALLBACK = ("माफ़ कीजिए, मैं आपकी समस्या ठीक से समझ नहीं पाया। "
            "कृपया फसल का नाम और समस्या दोबारा बताइए, या अपने नज़दीकी कृषि विज्ञान केंद्र से संपर्क कीजिए।")


# ---------- Matching ----------
def normalize(text):
    """Make different spellings of the same word look the same."""
    text = unicodedata.normalize("NFC", text.lower())
    for ch in "ंँ़":           # remove dots (gehuun -> gehu)
        text = text.replace(ch, "")
    text = text.replace("ू", "ु").replace("ी", "ि")   # long vowels -> short
    return text


def get_answer(text):
    t = normalize(text)

    crop = None
    for crop_name, words in CROP_WORDS.items():
        if any(normalize(w) in t for w in words):
            crop = crop_name
            break

    problems = [p for p, words in PROBLEM_WORDS.items()
                if any(normalize(w) in t for w in words)]

    if not problems:
        return FALLBACK

    intro = f"आपने {crop} की फसल के बारे में पूछा है। " if crop else ""
    return intro + " ".join(ADVICE[p] for p in problems)


if __name__ == "__main__":
    tests = [
        "मेरे गेहूं के पत्ते पीले हो गये, क्या करूं?",
        "mere gehun mein keede lag gaye",
        "धान की फसल सूख रही है",
        "आज मौसम कैसा है",
    ]
    for sentence in tests:
        print("Sawaal:", sentence)
        print("Jawab :", get_answer(sentence))
        print()