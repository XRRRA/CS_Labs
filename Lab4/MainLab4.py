import random
import string


def generate_random_message():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def text_to_binary(text):
    binary_message = ''.join([format(ord(char), '08b') for char in text])
    return binary_message


def print_binary_representation(binary_message):
    print("\nReprezentare binara:")
    print(f"Bit string: {binary_message}")
    print(f"Lungimea: {len(binary_message)} bits")


def calculate_l1(binary_message):
    if len(binary_message) != 64:
        raise ValueError("Input must be exactly 64 bits long")

    l1 = binary_message[:32]
    return l1


print("Algoritmul DES - Calcularea L1")
print("1. Introdu un mesaj manual")
print("2. Genereaza un mesaj aleatoriu")

choice = input("Introdu alegerea ta (1/2): ").strip()

if choice == '1':
    while True:
        message = input("Introdu un mesaj cu lungimea de 8 caractere: ").strip()
        if len(message) == 8:
            break
        print("Mesajul trebuie sa aiba lungimea de 8 caractere! ")
else:
    message = generate_random_message()
    print(f"Mesajul generat: {message}")

message_binary = text_to_binary(message)

print_binary_representation(message_binary)

l1 = calculate_l1(message_binary)

print("\nCalcularea L1:")
print(f"L1 (primii 32 bits): {l1}")
print(f"L1 in Hex: 0x{int(l1, 2):08X}")

l1_text = ''.join([chr(int(l1[i:i + 8], 2)) for i in range(0, 32, 8)])
print(f"L1 in Text: {l1_text}")
