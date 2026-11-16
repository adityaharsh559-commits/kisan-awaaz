crops = ["gehun", "chawal", "makka", "sarson"]

print(crops)           # the whole list
print(crops[0])        # gehun (counting starts at 0, not 1)
print(crops[2])        # makka
crops.append("chana")  # add an item at the end
print(len(crops))      # 5 (how many items)

for crop in crops:
    print("Fasal:", crop)

count = 1
while count <= 3:
    print("Round", count)
    count = count + 1

tips = {
    "gehun": "Pehli sinchai buwai ke 20-25 din baad karein.",
    "chawal": "Kheti mein paani ka star banaye rakhein.",
    "makka": "Achhi jal-nikasi wali zameen chunein.",
}

print(tips["gehun"])   # looks up the value using the label
tips["sarson"] = "Practice tip for sarson."   # add a new pair

def get_tip(crop):
    crop = crop.lower()
    if crop in tips:
        return tips[crop]
    return "Is fasal ki jaankari abhi nahi hai."

print(get_tip("Gehun"))
print(get_tip("aam"))


while True:
    crop = input("Fasal ka naam (band karne ke liye 'exit'): ")
    if crop.lower() == "exit":
        break
    print(get_tip(crop))