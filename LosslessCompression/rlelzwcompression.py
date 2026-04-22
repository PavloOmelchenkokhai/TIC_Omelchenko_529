import math
import collections
import matplotlib.pyplot as plt

# ЧИТАННЯ ФАЙЛУ
with open("sequence.txt", "r", encoding="utf-8") as file:
    original_sequences = [line.strip() for line in file if line.strip()]

results_table = []

# RLE
def encode_rle(sequence):
    if not sequence:
        return ""

    result = ""
    count = 1

    def encode_char(ch):
        return f"#{ch}" if ch.isdigit() else ch

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            result += encode_char(sequence[i - 1]) + str(count)
            count = 1

    result += encode_char(sequence[-1]) + str(count)

    return result


def decode_rle(encoded):
    result = ""
    i = 0

    while i < len(encoded):

        if encoded[i] == '#':
            char = encoded[i + 1]
            i += 2
        else:
            char = encoded[i]
            i += 1

        count = ""
        while i < len(encoded) and encoded[i].isdigit():
            count += encoded[i]
            i += 1

        result += char * int(count)

    return result


# LZW
def encode_lzw(sequence):
    dictionary = {ch: i for i, ch in enumerate(sorted(set(sequence)))}
    next_code = len(dictionary)

    current = ""
    result = []

    for symbol in sequence:
        combined = current + symbol
        if combined in dictionary:
            current = combined
        else:
            result.append(dictionary[current])
            dictionary[combined] = next_code
            next_code += 1
            current = symbol

    if current:
        result.append(dictionary[current])

    return result, dictionary


# ОСНОВНА ЧАСТИНА
with open("results_rle_lzw.txt", "w", encoding="utf-8") as file:

    for i, sequence in enumerate(original_sequences, 1):

        file.write(f"\n===== Послідовність {i} =====\n")

        counts = collections.Counter(sequence)
        probabilities = {k: v / len(sequence) for k, v in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probabilities.values())

        file.write(f"Оригінал: {sequence}\n")
        file.write(f"Розмір оригіналу: {len(sequence)*8} bits\n")
        file.write(f"Ентропія: {round(entropy, 4)}\n")

        # RLE
        encoded_rle = encode_rle(sequence)
        decoded_rle = decode_rle(encoded_rle)

        size_rle = len(encoded_rle) * 8
        cr_rle = round((len(sequence)*8) / size_rle, 2)

        file.write("\n--- RLE ---\n")
        file.write(f"Закодована: {encoded_rle}\n")
        file.write(f"Декодована: {decoded_rle}\n")
        file.write(f"Розмір закодованої: {size_rle} bits\n")
        file.write(f"Розмір декодованої: {len(decoded_rle)*8} bits\n")
        file.write(f"Коефіцієнт стиснення: {cr_rle}\n")

        # LZW
        encoded_lzw, lzw_dict = encode_lzw(sequence)
        encoded_lzw_str = ''.join(map(str, encoded_lzw))

        size_lzw = len(encoded_lzw) * 16
        cr_lzw = round((len(sequence)*8) / size_lzw, 2)

        file.write("\n--- LZW ---\n")
        file.write(f"Закодована: {encoded_lzw_str}\n")
        file.write(f"Розмір закодованої: {size_lzw} bits\n")
        file.write(f"Коефіцієнт стиснення: {cr_lzw}\n")

        file.write("\nСловник LZW:\n")
        for key, value in lzw_dict.items():
            file.write(f"{key} : {value}\n")

        results_table.append([
            f"Посл. {i}",
            round(entropy, 2),
            cr_rle if cr_rle >= 1 else "-",
            cr_lzw
        ])

# ТАБЛИЦЯ
fig, ax = plt.subplots()
ax.axis('off')

table = ax.table(
    cellText=results_table,
    colLabels=["Послідовність", "Ентропія", "КС RLE", "КС LZW"],
    loc='center'
)

table.scale(1, 2)
plt.savefig("comparison_table.png")
plt.show()