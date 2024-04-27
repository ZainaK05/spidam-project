# plot.py

# File Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# Plot Waveform
def plot_waveform(audio, sample_rate):
    time = np.arange(0, len(audio)) / sample_rate
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform')
    plt.grid(True)
    plt.show()


# Plot RT60
def plot_rt60(audio, sample_rate, freq_range, title):
    time = np.arange(0, len(audio)) / sample_rate
    freq_bins = np.fft.fftfreq(len(audio), 1 / sample_rate)
    audio_fft = np.abs(np.fft.fft(audio))

    band_mask = (freq_bins >= freq_range[0]) & (freq_bins < freq_range[1])
    band_fft = audio_fft[band_mask]
    band_peaks, _ = find_peaks(band_fft, height=np.max(band_fft) * 0.5)
    if len(band_peaks) > 1:
        peak_times = time[band_peaks]
        rt60 = calculate_rt60(peak_times, band_fft[band_peaks])
        plot_rt60_curve(freq_bins, audio_fft, band_mask, band_peaks, rt60, title)
    else:
        print(f"No peaks found in frequency range for {title}.")


# Calculate RT60
def calculate_rt60(times, amplitudes):
    max_amp = np.max(amplitudes)
    amp_5db_below_max = max_amp - 5
    amp_25db_below_max = max_amp - 25

    # Find time values corresponding to the amplitude thresholds
    time_5db = times[np.argmax(amplitudes >= amp_5db_below_max)]
    time_25db = times[np.argmax(amplitudes >= amp_25db_below_max)]

    # Calculate RT20
    rt20 = time_25db - time_5db

    # Multiply by 3 to get RT60
    rt60 = rt20 * 3

    return rt60


# Plot RT60 Curve
def plot_rt60_curve(freq_bins, audio_fft, band_mask, band_peaks, rt60, title):
    plt.figure(figsize=(8, 6))
    plt.plot(freq_bins[band_mask], audio_fft[band_mask])
    plt.plot(freq_bins[band_peaks], audio_fft[band_peaks], '-')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(f"{title} (RT60: {rt60:.2f} seconds)")
    plt.grid(True)
    plt.show()

# Plot Additional (Placeholder)
def plot_additional(audio, sample_rate):
    # Calculate some data for the bar graph (example data)
    x = np.arange(5)
    y = np.random.randint(1, 10, size=5)

    # Create the bar graph
    plt.figure(figsize=(8, 6))
    plt.bar(x, y)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Graph')
    plt.grid(True)
    plt.show()


# Plot Combination of Low, Mid, And High Frequencies
def plot_combined_rt60(audio, sample_rate, freq_ranges):
    time = np.arange(0, len(audio)) / sample_rate
    freq_bins = np.fft.fftfreq(len(audio), 1 / sample_rate)
    audio_fft = np.abs(np.fft.fft(audio))

    plt.figure(figsize=(10, 6))

    for freq_range, color in zip(freq_ranges.values(), ['blue', 'green', 'red']):
        band_mask = (freq_bins >= freq_range[0]) & (freq_bins < freq_range[1])
        band_fft = audio_fft[band_mask]
        band_peaks, _ = find_peaks(band_fft, height=np.max(band_fft) * 0.5)
        if len(band_peaks) > 1:
            peak_times = time[band_peaks]
            rt60 = calculate_rt60(peak_times, band_fft[band_peaks])
            plt.plot(freq_bins[band_mask], audio_fft[band_mask], label=f"RT60: {rt60:.2f} s", color=color)
        else:
            print(f"No peaks found in frequency range.")

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Combined RT60 for Low, Mid, and High Frequencies')
    plt.legend()
    plt.grid(True)
    plt.show()

    
