import cmath
import math
import matplotlib.pyplot as plt
import numpy as np

def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [cmath.exp(-2j * math.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + \
           [even[k] - T[k] for k in range(N // 2)]

if __name__ == "__main__":
    N = 16
    fs = 64  # частота дискретизации
    t = [n / fs for n in range(N)]

    # Сигнал: x(t) = sin(2π⋅10t) + 0.5sin(2π⋅20t)
    x = [math.sin(2 * math.pi * 10 * ti) + 0.5 * math.sin(2 * math.pi * 20 * ti) for ti in t]

    # --- Ручное FFT ---
    X_manual = fft([complex(val, 0) for val in x])

    # --- Библиотечное FFT (NumPy) ---
    X_numpy = np.fft.fft(x)

    print("Результат БПФ (амплитуда и фаза):\n")
    print(f"{'k':>3} {'Частота (Гц)':>15} {'Ампл.(ручн.)':>15} {'Ампл.(numpy)':>15} {'Фаза(рад)':>15}")
    print("-" * 75)

    amplitudes_manual = []
    amplitudes_numpy = []
    freqs = []

    for k in range(N // 2):
        freq = k * fs / N
        amp_manual = abs(X_manual[k]) / (N / 2)
        amp_numpy = abs(X_numpy[k]) / (N / 2)
        phase = math.atan2(X_manual[k].imag, X_manual[k].real)
        freqs.append(freq)
        amplitudes_manual.append(amp_manual)
        amplitudes_numpy.append(amp_numpy)
        print(f"{k:3d} {freq:15.2f} {amp_manual:15.4f} {amp_numpy:15.4f} {phase:15.4f}")

    # --- Графики ---
    plt.figure(figsize=(12, 6))

    # 1. Сигнал во времени
    plt.subplot(1, 2, 1)
    plt.plot(t, x, marker='o', linestyle='-', color='blue')
    plt.title("Сигнал во времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    # 2. Сравнение спектров
    plt.subplot(1, 2, 2)
    plt.plot(freqs, amplitudes_manual, marker='o', linestyle='-', color='red', label="Самописный FFT")
    plt.plot(freqs, amplitudes_numpy, marker='x', linestyle='--', color='green', label="NumPy FFT")
    plt.title("Сравнение амплитудных спектров")
    plt.xlabel("Частота (Гц)")
    plt.ylabel("Амплитуда")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
