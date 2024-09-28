import string

ALPHABET = string.ascii_uppercase

def shift_char(plain_char, key_char):
        new_pos = (ALPHABET.index(plain_char) + ALPHABET.index(key_char)) % 26
        return ALPHABET[new_pos]

# making key sequence to match plaintext length by repeating key.
def extend_key(plaintext, key):
    expanded_key = []
    key = key.upper()
    key_len = len(key)

    for i, char in enumerate(plaintext):
            expanded_key.append(key[i % key_len])

    return ''.join(expanded_key)

def vigenere_encrypt(plaintext, key):
    # preprocessing the text
    plaintext = plaintext.upper().replace(" ","")
    key_sequence = extend_key(plaintext, key)
    encrypted_message = []

    for pt_char, key_char in zip(plaintext, key_sequence):
        encrypted_message.append(shift_char(pt_char, key_char))

    return ''.join(encrypted_message)

if __name__ == '__main__':

    with open("input.txt","r") as f:
        plaintext = f.readline()
        
    key = input("Enter a Key to Encrypt the text : ")
    key = key.upper()

    encrypted_text = vigenere_encrypt(plaintext, key)

    # Output the encrypted message
    print("Original Plaintext:", plaintext)
    print("Encryption Key:", key)
    print("Encrypted Text:", encrypted_text)

    with open("encrypted_text.txt","w") as f:
        f.write(encrypted_text)
    