import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os

# Вхідні параметри (варіант 8)
n = 500
Fs = 1000
F_max = 17

# Генерація випадкового сигналу
random_signal = np.random.normal(0, 10, n)

# Формування часових відліків
time = np.arange(n) / Fs

# Розрахунок параметрів ФНЧ
w = F_max / (Fs / 2)

sos = signal.butter(3, w, 'low', output='sos')

# Фільтрація сигналу
filtered_signal = signal.sosfiltfilt(sos, random_signal)


# Функція побудови графіків
def plot_graph(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)
    plt.grid()

    if not os.path.exists("figures"):
        os.makedirs("figures")

    fig.savefig('./figures/' + title + '.png', dpi=600)
    plt.close(fig)


# Побудова сигналу
plot_graph(time,
           filtered_signal,
           "Сигнал з максимальною частотою F_max = 17 Гц",
           "Час (секунди)",
           "Амплітуда сигналу")

# Розрахунок спектру
spectrum = fft.fft(filtered_signal)
spectrum_shifted = np.abs(fft.fftshift(spectrum))

freq = fft.fftfreq(n, 1 / Fs)
freq_shifted = fft.fftshift(freq)

# Побудова спектра
plot_graph(freq_shifted,
           spectrum_shifted,
           "Спектр з максимальною частотою F_max = 17 Гц",
           "Частота (Гц)",
           "Амплітуда спектру")
