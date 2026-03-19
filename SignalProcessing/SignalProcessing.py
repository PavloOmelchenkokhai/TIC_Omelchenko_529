import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

# Параметри варіанту 8
n = 500
Fs = 1000
F_max = 17

# Створення папки
if not os.path.exists("figures"):
    os.makedirs("figures")

# Генерація сигналу
random_signal = np.random.normal(0, 10, n)
time = np.arange(n) / Fs

# Фільтр обмеження частоти
w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')
signal_filtered = signal.sosfiltfilt(sos, random_signal)

# Списки для результатів
quantized_signals = []
variances = []
snr_values = []

signal_variance = np.var(signal_filtered)

# Цикл квантування
for M in [4, 16, 64, 256]:

    quantize_signal = signal_filtered.copy()

    # Крок квантування
    delta = (np.max(quantize_signal) - np.min(quantize_signal)) / (M - 1)

    # Рівні квантування
    quantize_levels = np.arange(np.min(quantize_signal),
                                np.max(quantize_signal) + delta,
                                delta)

    # Таблиця квантування
    quantize_bit = np.arange(0, M)
    bit_length = int(np.log2(M))

    quantize_bit = [format(bits, f'0{bit_length}b') for bits in quantize_bit]

    quantize_table = np.c_[quantize_levels[:M], quantize_bit[:M]]

    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))

    table = ax.table(
        cellText=quantize_table,
        colLabels=['Значення сигналу', 'Код'],
        loc='center'
    )

    table.set_fontsize(14)
    table.scale(1, 1.5)

    ax.axis('off')

    plt.title(f"Таблиця квантування (M = {M})", fontsize=14, pad=20)

    plt.tight_layout()
    fig.savefig(f'./figures/quant_table_M_{M}.png', dpi=600)
    plt.close(fig)

    # Квантування сигналу
    quantized = []

    for value in quantize_signal:
        index = np.argmin(np.abs(quantize_levels - value))
        quantized.append(quantize_levels[index])

    quantized = np.array(quantized)
    quantized_signals.append(quantized)

    # Дисперсія і SNR
    error = quantized - quantize_signal
    variance = np.var(error)
    variances.append(variance)

    snr = signal_variance / variance
    snr_values.append(snr)

    # Бітова послідовність
    bits = []

    for value in quantized:
        index = np.argmin(np.abs(quantize_levels - value))
        bits.append(format(index, f'0{bit_length}b'))

    bits = [int(item) for item in list(''.join(bits))]

    # Графік бітів
    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.step(range(len(bits)), bits)
    ax.set_title(f"Бітова послідовність (M = {M})")
    ax.set_xlabel("Номер біта")
    ax.set_ylabel("Біт")

    fig.savefig(f'figures/bits_M_{M}.png', dpi=600)
    plt.close(fig)

# Графік цифрових сигналів
fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))

M_values = [4, 16, 64, 256]
s = 0

for i in range(2):
    for j in range(2):
        ax[i][j].plot(time, quantized_signals[s])
        ax[i][j].set_title(f"M = {M_values[s]}")
        ax[i][j].set_xlabel("Час (с)")
        ax[i][j].set_ylabel("Амплітуда")
        s += 1

plt.suptitle("Цифрові сигнали при різних рівнях квантування")
fig.savefig("figures/quantized_signals.png", dpi=600)
plt.close(fig)

# Графік дисперсії
fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(M_values, variances)
ax.set_xlabel("Кількість рівнів квантування M")
ax.set_ylabel("Дисперсія")
ax.set_title("Залежність дисперсії від кількості рівнів квантування")

fig.savefig("figures/variance_vs_M.png", dpi=600)
plt.close(fig)

# Графік SNR
fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(M_values, snr_values)
ax.set_xlabel("Кількість рівнів квантування M")
ax.set_ylabel("Відношення сигнал/шум (SNR)")
ax.set_title("Залежність SNR від кількості рівнів квантування")

fig.savefig("figures/snr_vs_M.png", dpi=600)
plt.close(fig)