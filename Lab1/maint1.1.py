def encrypt(key, message, alphabet):
    encrypted_message = ""
    for ch in message:
        if ch in alphabet:
            pos = alphabet.index(ch)
            new_pos = (pos + key) % 26
            encrypted_message += alphabet[new_pos]
    return encrypted_message


def decrypt(key, message, alphabet):
    decrypted_message = ""
    for ch in message:
        if ch in alphabet:
            pos = alphabet.index(ch)
            new_pos = (pos - key) % 26
            decrypted_message += alphabet[new_pos]
    return decrypted_message


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

while True:
    choice = input("Do you want to encrypt a message, or decrypt it? E/D\n").upper().strip().replace(" ", "")
    if choice == "E" or choice == "D":
        break
    else:
        print("Invalid choice. Please choose either encryption: E, or decryption: D.")

while True:
    key = int(input("Enter your key (1-25): "))
    if 1 <= key <= 25:
        break
    else:
        print("Invalid key. Please enter a key between 1 and 25.")

if choice == "E":
    message = input("Enter your message for encryption\n").upper().replace(" ", "").strip()
    result = encrypt(key, message, alphabet)
    print(f"Encrypted message: {result}")
else:
    message = input("Enter your cryptogram for decryption\n").upper().replace(" ", "").strip()
    result = decrypt(key, message, alphabet)
    print(f"Decrypted message: {result}")
