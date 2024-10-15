def create_permuted_alphabet(keyword, alphabet):
    # Remove duplicates from the keyword while preserving the order
    keyword = ''.join(sorted(set(keyword), key=keyword.index))

    # Create the permuted alphabet by placing the keyword at the start
    permuted_alphabet = keyword
    for letter in alphabet:
        if letter not in permuted_alphabet:
            permuted_alphabet += letter
    return permuted_alphabet


def encrypt(key, message, permuted_alphabet):
    encrypted_message = ""
    for ch in message:
        if ch in permuted_alphabet:
            pos = permuted_alphabet.index(ch)
            new_pos = (pos + key) % 26
            encrypted_message += permuted_alphabet[new_pos]
    return encrypted_message


def decrypt(key, message, permuted_alphabet):
    decrypted_message = ""
    for ch in message:
        if ch in permuted_alphabet:
            pos = permuted_alphabet.index(ch)
            new_pos = (pos - key) % 26
            decrypted_message += permuted_alphabet[new_pos]
    return decrypted_message


# Caesar cipher base alphabet (letters only, no ASCII)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

while True:
    choice = input("Do you want to encrypt a message, or decrypt it? E/D\n").upper().strip().replace(" ", "")
    if choice == "E" or choice == "D":
        break
    else:
        print("Invalid choice. Please choose either encryption: E, or decryption: D.")

# Input and validate key 1 (shift key)
while True:
    key = int(input("Enter your shift key (1-25): "))
    if 1 <= key <= 25:
        break
    else:
        print("Invalid key. Please enter a key between 1 and 25.")

# Input and validate key 2 (keyword) - must be at least 7 letters long and contain only Latin letters
while True:
    keyword = input("Enter your keyword (at least 7 unique Latin letters): ").upper().replace(" ", "").strip()
    if len(set(keyword)) >= 7 and all(ch in alphabet for ch in keyword):
        break
    else:
        print("Invalid keyword. Please enter at least 7 unique Latin letters.")

# Generate the permuted alphabet based on the keyword
permuted_alphabet = create_permuted_alphabet(keyword, alphabet)
print(f"Permuted alphabet: {permuted_alphabet}")

# Input the message
if choice == "E":
    message = input("Enter your message for encryption\n").upper().replace(" ", "").strip()
    result = encrypt(key, message, permuted_alphabet)
    print(f"Encrypted message: {result}")
else:
    message = input("Enter your cryptogram for decryption\n").upper().replace(" ", "").strip()
    result = decrypt(key, message, permuted_alphabet)
    print(f"Decrypted message: {result}")
