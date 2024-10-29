def is_valid_message(message):
    valid_chars = set("AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ")
    return all(char in valid_chars for char in message)


def prepare_message(message):
    message = message.replace(" ", "").upper()
    return ''.join(filter(lambda char: char in "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ", message))


def generate_key(msg, key):
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def encrypt_vigenere(msg, key):
    encrypted_text = []
    key = generate_key(msg, key)
    alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
    for i in range(len(msg)):
        char = msg[i]
        if char in alphabet:
            encrypted_index = (alphabet.index(char) + alphabet.index(key[i])) % len(alphabet)
            encrypted_char = alphabet[encrypted_index]
        else:
            encrypted_char = char
        encrypted_text.append(encrypted_char)
    return "".join(encrypted_text)


def decrypt_vigenere(msg, key):
    decrypted_text = []
    key = generate_key(msg, key)
    alphabet = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
    for i in range(len(msg)):
        char = msg[i]
        if char in alphabet:
            decrypted_index = (alphabet.index(char) - alphabet.index(key[i]) + len(alphabet)) % len(alphabet)
            decrypted_char = alphabet[decrypted_index]
        else:
            decrypted_char = char
        decrypted_text.append(decrypted_char)
    return "".join(decrypted_text)

def main():
    choice = int(input("Alege operația: 1 - Criptare, 2 - Decriptare: "))
    key = input("Introduceți cheia (minim 7 caractere): ").upper()

    while len(key) < 7:
        key = input("Cheia trebuie să aibă cel puțin 7 caractere. Introduceți din nou cheia: ").upper()

    message = input("Introduceți mesajul: ")
    message = prepare_message(message)

    if not is_valid_message(message):
        print("Mesajul conține caractere nepermise. Folosiți doar A-Z, Â, Ș, Ț, Î, Ă.")
        return

    key = generate_key(message, key)

    if choice == 1:
        encrypted_text = encrypt_vigenere(message, key)
        print("Mesajul criptat:", encrypted_text)
    elif choice == 2:
        decrypted_text = decrypt_vigenere(message, key)
        print("Mesajul decriptat:", decrypted_text)
    else:
        print("Alegere invalidă.")


if __name__ == "__main__":
    main()
