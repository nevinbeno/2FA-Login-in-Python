import bcrypt

text = input("Enter anything : ")
hashed_text = bcrypt.hashpw(text.encode(), bcrypt.gensalt()).decode()
print(f"The bcrypted version of {text} is {hashed_text}")