import itertools
from typing import List, Tuple
from collections import defaultdict
#from Levenshtein import distance as levenshtein_distance :: pip install python-Levenshtein
#Or else below code
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


# Mapping of QWERTY keys to Braille dot positions
key_to_dot = {'D': 1, 'W': 2, 'Q': 3, 'K': 4, 'O': 5, 'P': 6}

# Sample dictionary (QWERTY Braille input for words)
braille_dict = {
    "hello": ["DOP", "D", "DK", "DKO", "DOP"],  # dummy representation
    "help": ["DOP", "D", "DK", "DWP"],
    "cat": ["DK", "D", "DP"],
    "dog": ["DOP", "D", "DK"],
    "code": ["DK", "O", "D", "DP"]
}

def braille_char_to_binary(char_keys: str) -> str:
    # Converts QWERTY keys pressed to a 6-bit braille binary string
    binary = ['0'] * 6
    for key in char_keys.upper():
        if key in key_to_dot:
            binary[key_to_dot[key] - 1] = '1'
    return ''.join(binary)

def word_to_braille(word_keys: List[str]) -> str:
    # Converts a word (list of braille keys like ["DK", "D", "Q"]) to binary representation
    return ' '.join([braille_char_to_binary(char) for char in word_keys])

def find_closest_word(input_sequence: List[str], dictionary: dict, top_n=1) -> List[Tuple[str, int]]:
    input_binary = word_to_braille(input_sequence)
    distances = []
    
    for word, braille_seq in dictionary.items():
        word_binary = word_to_braille(braille_seq)
        dist = levenshtein_distance(input_binary, word_binary)
        distances.append((word, dist))
    
    distances.sort(key=lambda x: x[1])
    return distances[:top_n]

# Example input from user
user_input = ["DOP", "D", "DK", "DKO", "DOP"]  # Supposedly typed "hello" with some typo
suggestions = find_closest_word(user_input, braille_dict)

print("Suggested corrections:")
for word, dist in suggestions:
    print(f"- {word} (distance: {dist})")
