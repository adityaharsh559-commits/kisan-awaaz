from listen import listen
from knowledge import get_answer
from speak import speak

print("किसान आवाज़ तैयार है।\n")

while True:
    text, lang = listen("hi")
    if not text:
        continue

    print("\nAapne kaha:", text)
    answer = get_answer(text)
    print("Jawab:", answer)
    speak(answer)

    again = input("\nAur sawaal? (Enter = haan, q = band karein): ")
    if again.lower() == "q":
        break