from knowledge import normalize, CROP_WORDS, PROBLEM_WORDS


def find_topics(text):
    """Returns (crop, [problems]) found in the sentence."""
    t = normalize(text)

    crop = None
    for crop_name, words in CROP_WORDS.items():
        if any(normalize(w) in t for w in words):
            crop = crop_name
            break

    problems = [p for p, words in PROBLEM_WORDS.items()
                if any(normalize(w) in t for w in words)]
    return crop, problems