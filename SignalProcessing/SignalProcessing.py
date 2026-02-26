import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os

# Вхідні параметри (варіант 8)
n = 500
Fs = 1000
F_max = 17
F_filter = 24

Dt_values = [2, 4, 8, 16]

# Створення папки figures
if not os.path.exists("figures"):
    os.makedirs("figures")

# Генерація сигналу
random_signal = np.random.normal(0, 10, n)
time = np.arange(n) / Fs

# Фільтрація (обмеження F_max)
w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')
signal_filtered = signal.sosfiltfilt(sos, random_signal)

# Списки для збереження результатів
discrete_signals = []
discrete_spectrums = []
recovered_signals = []
variances = []
snr_values = []

# Дисперсія початкового сигналу
signal_variance = np.var(signal_filtered)

# Основний цикл дискретизації
for Dt in Dt_values:

    # Дискретизація
    discrete_signal = np.zeros(n)

    for i in range(0, round(n / Dt)):
        discrete_signal[i * Dt] = signal_filtered[i * Dt]

    discrete_signals += [list(discrete_signal)]

    # Спектр
    spectrum = fft.fft(discrete_signal)
    spectrum_shifted = np.abs(fft.fftshift(spectrum))
    discrete_spectrums += [list(spectrum_shifted)]

    # Відновлення сигналу
    w_rec = F_filter / (Fs / 2)
    sos_rec = signal.butter(3, w_rec, 'low', output='sos')
    recovered_signal = signal.sosfiltfilt(sos_rec, discrete_signal)

    recovered_signals += [list(recovered_signal)]

    # Розрахунок похибки
    E1 = recovered_signal - signal_filtered
    variance_error = np.var(E1)
    variances.append(variance_error)

    snr = signal_variance / variance_error
    snr_values.append(snr)

# Частотна вісь
freq = fft.fftfreq(n, 1/Fs)
freq_shifted = fft.fftshift(freq)

# Функція для 2х2 графіків
def plot_2x2(x, y, title, xlabel, ylabel):

    fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
    s = 0

    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, y[s], linewidth=1)
            ax[i][j].set_title(f"Dt = {Dt_values[s]}", fontsize=14)
            s += 1

    fig.supxlabel(xlabel, fontsize=14)
    fig.supylabel(ylabel, fontsize=14)
    fig.suptitle(title, fontsize=14)

    fig.savefig('./figures/' + title + '.png', dpi=600)
    plt.close(fig)

# Побудова графіків
plot_2x2(time, discrete_signals,
         "Дискретизовані сигнали",
         "Час (секунди)",
         "Амплітуда")

plot_2x2(freq_shifted, discrete_spectrums,
         "Спектри дискретизованих сигналів",
         "Частота (Гц)",
         "Амплітуда спектру")

plot_2x2(time, recovered_signals,
         "Відновлені сигнали після ФНЧ",
         "Час (секунди)",
         "Амплітуда")

# Графік дисперсії
fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(Dt_values, variances, linewidth=1)
ax.set_xlabel("Крок дискретизації", fontsize=14)
ax.set_ylabel("Дисперсія похибки", fontsize=14)
plt.title("Залежність дисперсії від кроку дискретизації", fontsize=14)
fig.savefig('./figures/Залежність_дисперсії_від_Dt.png', dpi=600)
plt.close(fig)

# Графік співвідношення сигнал-шум
fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(Dt_values, snr_values, linewidth=1)
ax.set_xlabel("Крок дискретизації Dt", fontsize=14)
ax.set_ylabel("Співвідношення сигнал-шум", fontsize=14)
plt.title("Залежність дисперсії від кроку дискретизації", fontsize=14)
fig.savefig('./figures/Залежність_дисперсії_від_Dt.png', dpi=600)
plt.close(fig)