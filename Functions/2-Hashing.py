import hashlib

text = input("Enter anything : ")
hashed_text = hashlib.sha256(text.encode()).hexdigest()
print(f"The hashed version of {text} is {hashed_text}")
# tip: 
# run the code multipe times for same input, what did you observe ? 
# ANSWER: You would see that, the code generated for same input is ALWAYS same.Can you guess why ? This happens because,
#         hashing just means, generating some code for a given text. The code generated is always same for a particular set of characters
#         Also, hashing takes place very quickly. 
# So, simple hashing is not preferred for securing passwords