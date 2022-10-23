import scipy.signal
import scipy.fft
import numpy as np


def decompose_fourier(original_data, rate):
    amplitudes = scipy.fft.fft(original_data)
    frequencies = scipy.fft.fftfreq(len(original_data), 1 / rate)
    return amplitudes, np.abs(frequencies)


def filter_fourier(amplitudes, frequencies, rate, low_pass, high_pass):
    points_per_freq = len(frequencies) / (rate / 2)

    #amplitudes[: int(points_per_freq * low_pass)] = 0
    #amplitudes[int(points_per_freq * high_pass):] = 0

    print(len(amplitudes))
    print(len(amplitudes[: int(points_per_freq * low_pass / 2)]))
    print(len(amplitudes[-int(points_per_freq * low_pass / 2) + int(len(amplitudes)):]))
    print(len(amplitudes[int(points_per_freq * high_pass / 2): int(len(amplitudes) / 2)]))
    print(len(amplitudes[int(len(amplitudes) / 2): -int(points_per_freq * high_pass / 2) + int(len(amplitudes))]))

    amplitudes[: int(points_per_freq * low_pass / 2)] = 0
    amplitudes[int(points_per_freq * low_pass / 2) + int(len(amplitudes) / 2):] = 0
    amplitudes[int(points_per_freq * high_pass / 2): int(len(amplitudes) / 2)] = 0
    amplitudes[int(len(amplitudes) / 2): int(points_per_freq * high_pass / 2) + int(len(amplitudes) / 2)] = 0
    filtered_data = scipy.fft.ifft(amplitudes)
    return filtered_data


def filter_wiener(original_data, window_size):
    filtered_data = scipy.signal.wiener(original_data, window_size)
    return filtered_data
