import math
import collections
import heapq
import matplotlib.pyplot as plt

# ЗЧИТУВАННЯ
def read_sequences():
    with open("sequence.txt", "r", encoding="utf-8") as file:
        sequences = [line.strip() for line in file if line.strip()]

    sequences = [seq[:10] for seq in sequences]
    return sequences


# ЕНТРОПІЯ
def calculate_entropy(sequence):
    counts = collections.Counter(sequence)
    probabilities = {k: v / len(sequence) for k, v in counts.items()}
    entropy = -sum(p * math.log2(p) for p in probabilities.values())
    return counts, probabilities, entropy


# AC
def build_intervals(probabilities):
    intervals = {}
    low = 0.0
    for symbol, prob in sorted(probabilities.items()):
        high = low + prob
        intervals[symbol] = (low, high)
        low = high
    return intervals


def encode_ac(sequence, probabilities):
    intervals = build_intervals(probabilities)

    low, high = 0.0, 1.0

    for symbol in sequence:
        range_ = high - low
        sym_low, sym_high = intervals[symbol]
        high = low + range_ * sym_high
        low = low + range_ * sym_low

    code = (low + high) / 2
    return code, intervals


def decode_ac(code, intervals, length):
    result = ""

    for _ in range(length):
        for symbol, (low, high) in intervals.items():
            if low <= code < high:
                result += symbol
                code = (code - low) / (high - low)
                break

    return result


# Десяткове -> двійкове
def float_to_binary(value, bits=32):
    binary = ""
    for _ in range(bits):
        value *= 2
        if value >= 1:
            binary += "1"
            value -= 1
        else:
            binary += "0"
    return binary


# HUFFMAN
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(probabilities):
    heap = [Node(ch, prob) for ch, prob in probabilities.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node is None:
        return codebook

    if node.char is not None:
        codebook[node.char] = prefix

    build_codes(node.left, prefix + "0", codebook)
    build_codes(node.right, prefix + "1", codebook)

    return codebook


def encode_huffman(sequence, codebook):
    return ''.join(codebook[ch] for ch in sequence)


def decode_huffman(encoded, tree):
    result = ""
    node = tree

    for bit in encoded:
        node = node.left if bit == "0" else node.right

        if node.char is not None:
            result += node.char
            node = tree

    return result


def main():
    sequences = read_sequences()
    results = []

    with open("results_AC_CH.txt", "w", encoding="utf-8") as file:

        for i, sequence in enumerate(sequences, 1):
            file.write(f"\n===== Sequence {i} =====\n")
            file.write(f"Sequence: {sequence}\n")

            counts, probabilities, entropy = calculate_entropy(sequence)

            file.write(f"Counts: {counts}\n")
            file.write(f"Probabilities: {probabilities}\n")
            file.write(f"Entropy: {round(entropy, 4)}\n")

            # AC
            encoded_ac, intervals = encode_ac(sequence, probabilities)
            decoded_ac = decode_ac(encoded_ac, intervals, len(sequence))

            binary_ac = float_to_binary(encoded_ac, 32)
            bps_ac = len(binary_ac) / len(sequence)

            file.write("\n--- Arithmetic Coding ---\n")
            file.write(f"Encoded (decimal): {encoded_ac}\n")
            file.write(f"Encoded (binary): {binary_ac}\n")
            file.write(f"Decoded: {decoded_ac}\n")
            file.write(f"BPS: {round(bps_ac, 4)}\n")

            # HUFFMAN
            tree = build_huffman_tree(probabilities)
            codebook = build_codes(tree)

            encoded_hc = encode_huffman(sequence, codebook)
            decoded_hc = decode_huffman(encoded_hc, tree)

            bps_hc = len(encoded_hc) / len(sequence)

            file.write("\n--- Huffman Coding ---\n")
            file.write(f"Codebook: {codebook}\n")
            file.write(f"Encoded: {encoded_hc}\n")
            file.write(f"Decoded: {decoded_hc}\n")
            file.write(f"BPS: {round(bps_hc, 4)}\n")

            results.append([bps_ac, bps_hc])

    # РИСУНОК ТАБЛИЦІ
    fig, ax = plt.subplots()
    ax.axis('off')

    table_data = [
        [i + 1, round(results[i][0], 3), round(results[i][1], 3)]
        for i in range(len(results))
    ]

    table = ax.table(
        cellText=table_data,
        colLabels=["Seq", "BPS AC", "BPS Huffman"],
        loc='center'
    )

    table.scale(1, 2)
    plt.savefig("bps_comparison.png")
    plt.show()

    print("Готово results_AC_CH.txt + bps_comparison.png")


if __name__ == "__main__":
    main()