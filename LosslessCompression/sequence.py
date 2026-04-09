import random
import string
import collections
import math
import matplotlib.pyplot as plt

# Параметри завдання
surname = "Омельченко"
group_number = "529"
student_number = 8

N = 100

results = []
sequences = []

# Послідовність 1
list1 = ['1'] * student_number
list0 = ['0'] * (N - student_number)
seq1 = list1 + list0
random.shuffle(seq1)
seq1 = ''.join(seq1)
sequences.append(seq1)

# Послідовність 2
seq2 = list(surname) + ['0'] * (N - len(surname))
seq2 = ''.join(seq2)
sequences.append(seq2)

# Послідовність 3
list1 = list(surname)
list0 = ['0'] * (N - len(list1))
seq3 = list1 + list0
random.shuffle(seq3)
seq3 = ''.join(seq3)
sequences.append(seq3)

# Послідовність 4
letters = list(surname) + list(group_number)
n_letters = len(letters)

repeats = N // n_letters
remainder = N % n_letters

seq4 = letters * repeats + letters[:remainder]
seq4 = ''.join(seq4)
sequences.append(seq4)

# Послідовність 5
elements = list(surname[:2]) + list(group_number)

k = len(elements)
count_each = N // k

seq5 = []
for el in elements:
    seq5 += [el] * count_each

random.shuffle(seq5)
seq5 = ''.join(seq5)
sequences.append(seq5)

# Послідовність 6
letters = list(surname[:2])
digits = list(group_number)

n_letters = int(0.7 * N)
n_digits = int(0.3 * N)

seq6 = []
for _ in range(n_letters):
    seq6.append(random.choice(letters))
for _ in range(n_digits):
    seq6.append(random.choice(digits))

random.shuffle(seq6)
seq6 = ''.join(seq6)
sequences.append(seq6)

# Послідовність 7
elements = string.ascii_lowercase + string.digits
seq7 = ''.join(random.choice(elements) for _ in range(N))
sequences.append(seq7)

# Послідовність 8
seq8 = '1' * N
sequences.append(seq8)

# ФУНКЦІЯ АНАЛІЗУ
def analyze(sequence):
    counts = collections.Counter(sequence)
    probability = {k: v / len(sequence) for k, v in counts.items()}

    mean_prob = sum(probability.values()) / len(probability)

    equal = all(abs(p - mean_prob) < 0.05 * mean_prob for p in probability.values())
    uniformity = "рівна" if equal else "нерівна"

    entropy = -sum(p * math.log2(p) for p in probability.values())

    alphabet_size = len(probability)

    if alphabet_size > 1:
        redundancy = 1 - entropy / math.log2(alphabet_size)
    else:
        redundancy = 1

    return alphabet_size, entropy, redundancy, uniformity, probability


# ЗАПИС У ФАЙЛ
with open("results_sequence.txt", "w", encoding="utf-8") as f:
    for i, seq in enumerate(sequences, 1):
        alphabet_size, entropy, redundancy, uniformity, probability = analyze(seq)

        prob_str = ', '.join([f"{k}={v:.4f}" for k, v in probability.items()])

        f.write(f"Sequence {i}:\n")
        f.write(f"{seq}\n")
        f.write(f"Alphabet size: {alphabet_size}\n")
        f.write(f"Entropy: {entropy:.4f}\n")
        f.write(f"Redundancy: {redundancy:.4f}\n")
        f.write(f"Type: {uniformity}\n")
        f.write(f"Probabilities: {prob_str}\n\n")

        results.append([alphabet_size, round(entropy, 2), round(redundancy, 2), uniformity])


# ЗБЕРЕЖЕННЯ ПОСЛІДОВНОСТЕЙ
with open("sequence.txt", "w", encoding="utf-8") as f:
    for seq in sequences:
        f.write(seq + "\n")


# ТАБЛИЦЯ
fig, ax = plt.subplots(figsize=(15, 5))
ax.axis('off')

headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
rows = [f'Послідовність {i}' for i in range(1, 9)]

table = ax.table(
    cellText=results,
    colLabels=headers,
    rowLabels=rows,
    loc='center',
    cellLoc='center'
)

table.set_fontsize(12)
table.scale(1, 2)

fig.savefig("характеристики.png")
plt.show()