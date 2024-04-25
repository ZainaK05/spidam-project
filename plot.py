# File Imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import linregress


# Returns the Total Time of the Audio File in Seconds
def return_time(audio, sample_rate):
    time = np.arange(0, len(audio)) / sample_rate
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform')
    plt.grid(True)
    plt.show()
    return time


# Calculate RT60 (Reverberation Time) Differences in Seconds
def calculate_rt60(audio, sample_rate, freq_range, time):
    freq_bins = np.fft.fftfreq(len(audio), 1 / sample_rate)
    audio_fft = np.abs(np.fft.fft(audio))
    rt60_values = {}

    for band, (low, high) in freq_range.items():
        band_mask = (freq_bins >= low) & (freq_bins < high)
        band_fft = audio_fft[band_mask]
        band_peaks, _ = find_peaks(band_fft, height=np.max(band_fft) * 0.5)
        if len(band_peaks) > 1:
            peak_times = time[band_peaks]
            slope, intercept, r_value, p_value, std_err = linregress(peak_times, np.log(band_fft[band_peaks]))
            rt60 = -1 / slope
            rt60_values[band] = rt60
        else:
            rt60_values[band] = np.nan

    return rt60_values


# Create Plot
def create_plots(audio, sample_rate):
    time = return_time(audio, sample_rate)
    freq_range = {'low': (20, 200), 'mid': (200, 2000), 'high': (2000, 20000)}