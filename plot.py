import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import wave

# Line 9 causes an error if not included... dont ask
# Sorry if code is bad... we'll figure it out

np.seterr(divide = 'ignore')
# Test variable - Just set to whatever audio file you want to use for testing
mono_fname = "Clap1_mono_chan.wav"

# All functions are setup to receive a mono audio filename of .wav format

def return_time(fname):

    # Returns the total time of the audio file in seconds

    samplerate, data = wavfile.read(fname)
    length = data.shape[0] / samplerate
    print(f"length = {length}s")
    return length

def return_freq(fname):

    # Returns the frequency of the audio file in Hz

    samplerate, data = wavfile.read(fname)
    print(f"sample rate = {samplerate}Hz")
    return samplerate

def return_channel_num(fname):

    # Returns the number of channels the audio file has

    samplerate, data = wavfile.read(fname)
    length = data.shape[0] / samplerate
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    return data.shape[len(data.shape) - 1]

def plot_spectrogram(mono_fname):

    # Creates a plot using matplotlib of the spectrogram of the audio file

    samplerate, data = wavfile.read(mono_fname)
    spectrum, freqs, t, im = plt.specgram(data, Fs=samplerate,
                                          NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    cbar = plt.colorbar(im)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    cbar.set_label('Intensity (dB)')
    plt.show()

    # This should be displayed in the user GUI but I'm unsure how to display it there instead

def plot_waveform(mono_fname):

    # Plots the waveform of the audio file using matplotlib

    raw = wave.open(mono_fname)
    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int16")
    f_rate = raw.getframerate()

    time = np.linspace(
        0,  # start
        len(signal) / f_rate,
        num=len(signal)
    )

    plt.figure(1)
    plt.title("Sound Wave")
    plt.xlabel("Time")
    plt.plot(time, signal)
    plt.show()

    # This should be displayed in the user GUI but I'm unsure how to display it there instead

# This part runs every function using the test variable - Should be removed on release

return_time(mono_fname)
return_freq(mono_fname)
return_channel_num(mono_fname)
plot_spectrogram(mono_fname)
plot_waveform(mono_fname)

# These will be moved to the imports section of the github but im adding
# them here so you guys can use them when testing

# pip install matplotlib
# pip install pylplot
# pip install scipy
