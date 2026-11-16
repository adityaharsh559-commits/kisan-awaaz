name = input("Aapka naam kya hai? ")
print("Namaste", name)

crop = "Gehun"        # text (string)
land_acres = 2.5      # decimal number (float)
farmers = 120         # whole number (integer)
is_irrigated = True   # True or False (boolean)

print(crop, land_acres, farmers, is_irrigated)

acres = float(input("Kitne acre zameen hai? "))
print("Aadha acre:", acres / 2)

price = int(input("Tamatar ka bhav (Rs/kg): "))

if price > 30:
    print("Achha daam hai, bech do!")
elif price >= 15:
    print("Theek daam hai.")
else:
    print("Kam daam hai, thoda ruko.")

crop = input("Fasal ka naam: ").lower()

if crop == "gehun":
    print("Tip: Pehli sinchai buwai ke 20-25 din baad karein.")
elif crop == "chawal":
    print("Tip: Kheti mein paani ka star banaye rakhein.")
else:
    print("Is fasal ki jaankari abhi nahi hai.")
    
        