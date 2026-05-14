import os
import math
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, pi
from scipy.fft import fft, fftfreq


# Побудова графіків
def plot(x, y, axis_x="", axis_y="", title="graph"):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, linewidth=1)

    ax.set_xlabel(axis_x, fontsize=12)
    ax.set_ylabel(axis_y, fontsize=12)
    plt.title(title, fontsize=12)

    if not os.path.isdir("./figures/"):
        os.mkdir("./figures/")

    fig.savefig(f"./figures/{title}.png", dpi=300)
    plt.close(fig)


# Генерація випадкової послідовності
def create_sequence():
    bits = np.random.randint(0, 2, 10)

    sequence = np.zeros(1000)

    for i in range(10):
        for j in range(100):
            sequence[i * 100 + j] = bits[i]

    return sequence


# Спектр сигналу
def spectrum(signal):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / 1000)

    return xf[:N // 2], np.abs(yf[:N // 2])


# ASK
def ask_modulation(frequency, sequence):
    sequence_ask = np.zeros(1000)

    for i in range(len(sequence)):
        sequence_ask[i] = sequence[i] * cos(
            2 * pi * frequency * i / 1000
        )

    return sequence_ask


def ask_demodulation(frequency, sequence):
    ask_product = np.zeros(1000)
    ask_demodulated_signal = np.zeros(1000)
    threshold = np.ones(1000) * 25
    sequence_demodulated = np.zeros(1000)

    for i in range(len(sequence)):
        ask_product[i] = sequence[i] * cos(
            2 * pi * frequency * i / 1000
        )

    for i in range(10):
        S = 0

        for t in range(100):
            index = t + 100 * i
            S += ask_product[index]
            ask_demodulated_signal[index] = S

    ask_demodulated = 1 / 2 * (
            np.sign(ask_demodulated_signal - threshold) + 1
    )

    for i in range(10):
        value = ask_demodulated[100 * i + 99]

        for t in range(100):
            sequence_demodulated[t + 100 * i] = value

    return ask_demodulated_signal, sequence_demodulated


# PSK
def psk_modulation(frequency, sequence):
    sequence_psk = np.zeros(1000)

    for i in range(len(sequence)):
        sequence_psk[i] = sin(
            2 * pi * frequency * i / 1000 +
            sequence[i] * pi + pi
        )

    return sequence_psk


def psk_demodulation(frequency, sequence):
    psk_product = np.zeros(1000)
    psk_demodulated_signal = np.zeros(1000)
    threshold = np.ones(1000) * 25
    sequence_demodulated = np.zeros(1000)

    for i in range(len(sequence)):
        psk_product[i] = sequence[i] * sin(
            2 * pi * frequency * i / 1000
        )

    for i in range(10):
        S = 0

        for t in range(100):
            index = t + 100 * i
            S += psk_product[index]
            psk_demodulated_signal[index] = S

    psk_demodulated = 1 / 2 * (
            np.sign(psk_demodulated_signal - threshold) + 1
    )

    for i in range(10):
        value = psk_demodulated[100 * i + 99]

        for t in range(100):
            sequence_demodulated[t + 100 * i] = value

    return psk_demodulated_signal, sequence_demodulated


# FSK
def fsk_modulation(frequency1, frequency2, sequence):
    sequence_fsk = np.zeros(1000)

    for i in range(len(sequence)):
        sequence_fsk[i] = (
                sequence[i] *
                sin(2 * pi * frequency1 * i / 1000)
                +
                abs(sequence[i] - 1) *
                sin(2 * pi * frequency2 * i / 1000)
        )

    return sequence_fsk


def fsk_demodulation(frequency1, frequency2, sequence):
    fsk_product1 = np.zeros(1000)
    fsk_product2 = np.zeros(1000)

    fsk_demodulated_signal1 = np.zeros(1000)
    fsk_demodulated_signal2 = np.zeros(1000)

    sequence_demodulated = np.zeros(1000)

    for i in range(len(sequence)):
        fsk_product1[i] = sequence[i] * sin(
            2 * pi * frequency1 * i / 1000
        )

        fsk_product2[i] = sequence[i] * sin(
            2 * pi * frequency2 * i / 1000
        )

    for i in range(10):
        S1 = 0
        S2 = 0

        for t in range(100):
            index = t + 100 * i

            S1 += fsk_product1[index]
            S2 += fsk_product2[index]

            fsk_demodulated_signal1[index] = S1
            fsk_demodulated_signal2[index] = S2

    fsk_detected = 1 / 2 * (
            np.sign(
                fsk_demodulated_signal1 -
                fsk_demodulated_signal2
            ) + 1
    )

    for i in range(10):
        value = fsk_detected[100 * i + 99]

        for t in range(100):
            sequence_demodulated[t + 100 * i] = value

    return (
        fsk_demodulated_signal1,
        fsk_demodulated_signal2,
        sequence_demodulated
    )


# Шум
def create_noise(mean, std, length):
    return np.random.normal(mean, std, length)


# Завадостійкість
def noise_stress(sequence, sequence_modulated,
                 modulation, frequency):
    error_modulated = []

    for i in range(20):
        p = 0

        for m in range(200):
            noise = create_noise(0, 1, 1000)
            sequence_noise = sequence_modulated + i * noise

            if modulation == "ASK":
                _, demod = ask_demodulation(
                    frequency[0],
                    sequence_noise
                )

            elif modulation == "PSK":
                _, demod = psk_demodulation(
                    frequency[0],
                    sequence_noise
                )

            else:
                _, _, demod = fsk_demodulation(
                    frequency[0],
                    frequency[1],
                    sequence_noise
                )

            summa = abs(sum(sequence - demod))
            p += summa / 1000

        error_modulated.append(p / 200)

    return error_modulated

def main(ask, psk, fsk1, fsk2):
    sequence = create_sequence()

    x = np.arange(len(sequence)) / 1000

    plot(
        x,
        sequence,
        axis_x="Час, c",
        axis_y="Амплітуда",
        title="1_Випадкова_послідовність"
    )

    # ASK
    sequence_ask = ask_modulation(ask, sequence)

    plot(
        x,
        sequence_ask,
        "Час, c",
        "Амплітуда",
        "2_ASK"
    )

    x_spectrum, spectrum_ask = spectrum(sequence_ask)

    plot(
        x_spectrum,
        spectrum_ask,
        "Частота, Гц",
        "Амплітуда",
        "3_Спектр_ASK"
    )

    # PSK
    sequence_psk = psk_modulation(psk, sequence)

    plot(
        x,
        sequence_psk,
        "Час, c",
        "Амплітуда",
        "4_PSK"
    )

    x_spectrum, spectrum_psk = spectrum(sequence_psk)

    plot(
        x_spectrum,
        spectrum_psk,
        "Частота, Гц",
        "Амплітуда",
        "5_Спектр_PSK"
    )

    # FSK
    sequence_fsk = fsk_modulation(fsk1, fsk2, sequence)

    plot(
        x,
        sequence_fsk,
        "Час, c",
        "Амплітуда",
        "6_FSK"
    )

    x_spectrum, spectrum_fsk = spectrum(sequence_fsk)

    plot(
        x_spectrum,
        spectrum_fsk,
        "Частота, Гц",
        "Амплітуда",
        "7_Спектр_FSK"
    )

    # Шум
    noise = create_noise(0, 1, 1000)

    ask_noise = sequence_ask + noise
    psk_noise = sequence_psk + noise
    fsk_noise = sequence_fsk + noise

    plot(x, ask_noise, "Час", "Амплітуда", "8_ASK_з_шумом")
    plot(x, psk_noise, "Час", "Амплітуда", "9_PSK_з_шумом")
    plot(x, fsk_noise, "Час", "Амплітуда", "10_FSK_з_шумом")

    # Демодуляція
    ask_demod_signal, ask_bits = ask_demodulation(ask, ask_noise)
    plot(x, ask_demod_signal, "Час", "Амплітуда", "11_ASK_демодуляція")
    plot(x, ask_bits, "Час", "Амплітуда", "12_ASK_біти")

    psk_demod_signal, psk_bits = psk_demodulation(psk, psk_noise)
    plot(x, psk_demod_signal, "Час", "Амплітуда", "13_PSK_демодуляція")
    plot(x, psk_bits, "Час", "Амплітуда", "14_PSK_біти")

    fsk_d1, fsk_d2, fsk_bits = fsk_demodulation(
        fsk1,
        fsk2,
        fsk_noise
    )

    plot(x, fsk_d1, "Час", "Амплітуда", "15_FSK_demod_1")
    plot(x, fsk_d2, "Час", "Амплітуда", "16_FSK_demod_2")
    plot(x, fsk_bits, "Час", "Амплітуда", "17_FSK_біти")

    # Шумостійкість
    error_ask = noise_stress(
        sequence,
        sequence_ask,
        "ASK",
        [ask]
    )

    error_psk = noise_stress(
        sequence,
        sequence_psk,
        "PSK",
        [psk]
    )

    error_fsk = noise_stress(
        sequence,
        sequence_fsk,
        "FSK",
        [fsk1, fsk2]
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(np.arange(20), error_ask)
    ax.plot(np.arange(20), error_psk)
    ax.plot(np.arange(20), error_fsk)

    ax.set_xlabel("Рівень шуму")
    ax.set_ylabel("Ймовірність помилки")
    ax.legend(["ASK", "PSK", "FSK"])

    plt.title("18_Завадостійкість")

    fig.savefig("./figures/18_Завадостійкість.png", dpi=300)
    plt.close(fig)

    print("У папці figures створено 18 графіків")


if __name__ == "__main__":
    main(
        ask=25,
        psk=25,
        fsk1=30,
        fsk2=15
    )