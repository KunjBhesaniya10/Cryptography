import string
from collections import Counter
from Key_length_estimate import estimate_key_length

# Letter frequency in English language
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228,
    'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
    'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987,
    'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
    'Y': 1.974, 'Z': 0.074
}

ALPHABET = string.ascii_uppercase

# Function to shift a character by n positions in the alphabet
def shift_character(char, shift):
    if char in ALPHABET:
        shifted_index = (ALPHABET.index(char) - shift) % 26
        return ALPHABET[shifted_index]
    return char

def decrypt_segment(segment, shift):
    return ''.join([shift_character(c, shift) for c in segment])

# Function to split ciphertext into segments based on key length. each segment
# has letters encrypted by same part of key.
def split_into_segments(ciphertext, key_length):
    segments = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        if char in ALPHABET:
            segments[i % key_length] += char
    return segments

# Function to calculate the chi-squared value for a given text and shift
def chi_squared_stat(segment):
   
    letter_counts = Counter(segment)
    total_letters = sum(letter_counts.values())

    chi_sq = 0.0
    for letter in ALPHABET:
        observed = letter_counts[letter]
        expected = ENGLISH_FREQ[letter] / 100 * total_letters
        chi_sq += ((observed - expected) ** 2) / expected 
    return chi_sq

# Function to guess the key by analyzing chi-squared values for each segment
def guess_key(ciphertext, key_length):
    segments = split_into_segments(ciphertext,key_length)
    key = ''

    for segment in segments:
        chi_squared_scores = []
        for shift in range(26):
            decrypted_segment = decrypt_segment(segment, shift)
            chi_sq = chi_squared_stat(decrypted_segment)
            chi_squared_scores.append((shift, chi_sq))

        best_shift = min(chi_squared_scores, key=lambda x: x[1])[0]
        key += ALPHABET[best_shift]

    return key


# Function to decrypt Vigenère cipher using guessed Key
def decrypt_vigenere(ciphertext, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
            shift = ALPHABET.index(key[i % key_length])
            decrypted_text += shift_character(char, shift)
    
    return decrypted_text

if __name__ == '__main__':

    with open("encrypted_text.txt","r") as f:
        ciphertext = f.readline()
    possible_key_lengths = estimate_key_length(ciphertext) 
    possible_decryptions=[]
    
    # Guessing  the keys for each possible length using frequency analysis

    for key_length in [key_lengths[0] for key_lengths in possible_key_lengths] :
        guessed_key = guess_key(ciphertext, key_length)
        decrypted_text = decrypt_vigenere(ciphertext, guessed_key)
        chi_stat = chi_squared_stat(decrypted_text)
        possible_decryptions.append((decrypted_text,chi_stat,guessed_key))
        print(chi_stat,key_length)

    possible_decryptions.sort(key= lambda x: (x[1],x[2]))
    guessed_key = possible_decryptions[0][2]
    decrypted_text = possible_decryptions[0][0]

    print(f"Guessed Key: {guessed_key}")

    # Decrypt the ciphertext using the guessed key
    print(f"Decrypted Text: {decrypted_text}")

   
