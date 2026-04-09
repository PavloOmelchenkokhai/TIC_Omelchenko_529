import math
import collections

# Читання файлу
with open("sequence.txt", "r", encoding="utf-8") as file:
    original_sequences = [line.strip() for line in file if line.strip()]

# RLE
def encode_rle(sequence):
    if not sequence:
        return ""

    result = []
    count = 1

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            result.append(f"{sequence[i - 1]}:{count}")
            count = 1

    result.append(f"{sequence[-1]}:{count}")
    return ' '.join(result)


def decode_rle(encoded):
    result = []
    for pair in encoded.split():
        if ':' not in pair:
            continue
        char, count = pair.split(':')
        result.append(char * int(count))
    return ''.join(result)


# LZW
def encode_lzw(sequence):
    unique_chars = sorted(set(sequence))
    dictionary = {ch: i for i, ch in enumerate(unique_chars)}
    reverse_dict = {i: ch for ch, i in dictionary.items()}

    next_code = len(dictionary)
    current = ""
    result = []

    for symbol in sequence:
        combined = current + symbol
        if combined in dictionary:
            current = combined
        else:
            if current:
                result.append(dictionary[current])
            dictionary[combined] = next_code
            reverse_dict[next_code] = combined
            next_code += 1
            current = symbol

    if current:
        result.append(dictionary[current])

    return result, reverse_dict


def decode_lzw(codes, initial_dict):
    dictionary = initial_dict.copy()
    dict_size = max(dictionary.keys()) + 1

    previous = dictionary[codes[0]]
    result = previous

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = previous + previous[0]

        result += entry
        dictionary[dict_size] = previous + entry[0]
        dict_size += 1
        previous = entry

    return result


# Основна частина
with open("results_rle_lzw.txt", "w", encoding="utf-8") as file:

    file.write("===== COMPARISON TABLE =====\n")
    file.write(f"{'Seq':<5}{'Entropy':<10}{'RLE CR':<10}{'LZW CR':<10}\n")

    for i, sequence in enumerate(original_sequences, 1):

        file.write(f"\n\n===== Sequence {i} =====\n")

        # Частоти
        counts = collections.Counter(sequence)

        # Ймовірності
        probabilities = {k: v / len(sequence) for k, v in counts.items()}

        # Ентропія
        entropy = -sum(p * math.log2(p) for p in probabilities.values())

        file.write(f"Sequence: {sequence}\n")
        file.write(f"Entropy: {round(entropy, 4)}\n")

        # RLE
        encoded_rle = encode_rle(sequence)
        decoded_rle = decode_rle(encoded_rle)

        size_original = len(sequence) * 8
        size_rle = len(encoded_rle.encode('utf-8')) * 8

        cr_rle = round(size_original / size_rle, 2) if size_rle != 0 else 0

        file.write("\n--- RLE ---\n")
        file.write(f"Encoded: {encoded_rle}\n")
        file.write(f"Correct: {sequence == decoded_rle}\n")
        file.write(f"CR: {cr_rle}\n")

        # LZW
        encoded_lzw, lzw_dict = encode_lzw(sequence)
        decoded_lzw = decode_lzw(encoded_lzw, lzw_dict)

        size_lzw = len(encoded_lzw) * 16
        cr_lzw = round(size_original / size_lzw, 2) if size_lzw != 0 else 0

        file.write("\n--- LZW ---\n")
        file.write(f"Encoded: {encoded_lzw}\n")
        file.write(f"Correct: {sequence == decoded_lzw}\n")
        file.write(f"CR: {cr_lzw}\n")

        file.write("\nLZW Dictionary:\n")
        for k, v in lzw_dict.items():
            file.write(f"{k}: {v}\n")

        file.write(f"\n[Table Row] {i:<5}{round(entropy,4):<10}{cr_rle:<10}{cr_lzw:<10}\n")