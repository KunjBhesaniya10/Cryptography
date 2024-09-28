def index_of_coincidence(text):
    N = len(text)
    freqs = Counter(text)
    numerator = sum(f * (f - 1) for f in freqs.values())
    denominator = N * (N - 1)
    return numerator / denominator


def split_into_subtexts(cipher, key_length):
    """Split the cipher text into subtexts, where each subtext corresponds to the letters
    encrypted with the same part of the key."""

    subtexts = ['' for _ in range(key_length)]
    for i, letter in enumerate(cipher):
        subtexts[i % key_length] += letter
    return subtexts

def estimate_key_length(cipher, max_key_length=20):
    """Estimating the key length using the Index of Coincidence method."""
    cipher = [c for c in cipher.lower() if c in string.ascii_lowercase]  # Filter out non-alphabetic characters
    best_key_lengths = []
      # Track the smallest difference from 0.065 (English IC)
    target_ic = 0.065  # Expected IC for English text

    for key_length in range(3, max_key_length + 1):
        subtexts = split_into_subtexts(cipher, key_length)
        avg_ic = sum(index_of_coincidence(subtext) for subtext in subtexts) / key_length

        ic_difference = abs(target_ic - avg_ic)
        
        best_key_lengths.append((key_length,ic_difference))
        print(ic_difference, key_length)
    
    best_key_lengths.sort(key = lambda x : (x[1],x[0]))
    print(best_key_lengths[:5])
    return best_key_lengths
