# gui.py

# File Imports
import tkinter as tk
from tkinter import filedialog
import data_manip
import soundfile as sf
import plot


# SPIDAM Application
class SpidamApp(tk.Tk):
    def __init__(self):

        # Calls Constructor of the Super Class
        super().__init__()

        # Application Title
        self.title("SPIDAM - Audio Analyzer")

        # Application Size
        self.geometry("600x400")

        # Define Parameters
        self.info_label = None
        self.output_label = None
        self.load_button = None
        self.audio = None
        self.sample_rate = None
        self.plot_waveform_button = None
        self.plot_low_rt60_button = None
        self.plot_mid_rt60_button = None
        self.plot_high_rt60_button = None
        self.plot_additional_button = None
        self.text_output_label = None
        self.freq_range = {'low': (60, 250), 'mid': (200, 2000), 'high': (5000, 10000)}
        self.create_widgets()

    # Create Application Widget/Buttons
    def create_widgets(self):
        # Text Line 1, in Red
        self.info_label = tk.Label(self, text="Please select an audio file to analyze.", fg="red")
        self.info_label.pack()

        # Text Line 2, in Red
        self.info_label = tk.Label(self, text="If the file is not in WAV format, it will be converted.\n",
                                       fg="red")

        # Load File Button
        self.info_label.pack()
        self.load_button = tk.Button(self, text="Load Audio File", command=self.load_file)
        self.load_button.pack()

        self.output_label = tk.Label(self, text="")
        self.output_label.pack()

        # Wave Buttons
        self.plot_waveform_button = tk.Button(self, text="Plot Waveform", command=self.plot_waveform)
        self.plot_waveform_button.pack()

        self.plot_low_rt60_button = tk.Button(self, text="Plot Low RT60", command=self.plot_low_rt60)
        self.plot_low_rt60_button.pack()

        self.plot_mid_rt60_button = tk.Button(self, text="Plot Mid RT60", command=self.plot_mid_rt60)
        self.plot_mid_rt60_button.pack()

        self.plot_high_rt60_button = tk.Button(self, text="Plot High RT60", command=self.plot_high_rt60)
        self.plot_high_rt60_button.pack()

        self.plot_additional_button = tk.Button(self, text="Plot Additional", command=self.plot_additional)
        self.plot_additional_button.pack()

        # Button to compile plots
        self.compile_plots_button = tk.Button(self, text="Compile Plots", command=self.compile_plots)
        self.compile_plots_button.pack()

        # Bottom Text
        self.text_output_label = tk.Label(self, text="")
        self.text_output_label.pack()

    # Load Audio File
    def load_file(self):

        # Allows User to Select a File Path
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.aac")])
        if file_path:
            file_format = file_path.split(".")[-1]

            # If File Loads Successfully, Show in Widget
            self.output_label.config(text="\nAudio loaded successfully.\n")
            # File Conversion Check, If Not Wav, Convert It
            if file_format != "wav":
                self.convert_to_wav(file_path)
            else:
                print("File format is already in wav.")
        else:
            # If File Doesn't Load Successfully
            self.output_label.config(text="\nNo file selected.\n")

    # File Conversion
    def convert_to_wav(self, file_path):

        # If File is Not in Wav Format, Convert
        try:
            audio, sample_rate = sf.read(file_path)
            new_file_path = file_path.replace(file_path.split(".")[-1], "wav")
            sf.write(new_file_path, audio, sample_rate)
            print(f"File converted to wav: {new_file_path}")

            # Proceed with Processing Metadata
            self.process_audio(new_file_path)

        except Exception as e:
            # Exception Handling
            print(f"Error converting file: {e}")

    # Dialogue for Processing Metadata
    def process_audio(self, file_path):

        # Processing
        print("Processing Metadata... Please Wait...")

        # Store Audio and Sample Rate
        self.audio, self.sample_rate = data_manip.process_audio(file_path)

        # Calculate total duration
        total_duration = len(self.audio) / self.sample_rate

        # Calculate resonant frequency (replace this with your actual calculation)
        resonant_frequency = 1000  # Placeholder value

        # Calculate RT60 difference (replace this with your actual calculation)
        rt60_difference = 0.5  # Placeholder value

        # Show Results of Processing
        if self.audio is not None:
            print("Processing completed successfully.")
            self.create_plots(self.audio, self.sample_rate)
            # Update GUI with calculated values
            self.update_text_output(total_duration, resonant_frequency, rt60_difference)
        else:
            # Exception Handling
            print("Error processing audio.")

    # Plot Regular Waveform
    def plot_waveform(self):
        if self.audio is not None:
            plot.plot_waveform(self.audio, self.sample_rate)
        else:
            self.output_label.config(text="Load audio first.")

    # Plot Low Frequency Waveform
    def plot_low_rt60(self):
        if self.audio is not None:
            plot.plot_rt60(self.audio, self.sample_rate, self.freq_range['low'], "Low RT60")
        else:
            self.output_label.config(text="Load audio first.")

    # Plot Middle Frequency Waveform
    def plot_mid_rt60(self):
        if self.audio is not None:
            plot.plot_rt60(self.audio, self.sample_rate, self.freq_range['mid'], "Mid RT60")
        else:
            self.output_label.config(text="Load audio first.")

    # Plot High Frequency Waveform
    def plot_high_rt60(self):
        if self.audio is not None:
            plot.plot_rt60(self.audio, self.sample_rate, self.freq_range['high'], "High RT60")
        else:
            self.output_label.config(text="Load audio first.")

    # Plot Additional Waveform
    def plot_additional(self):
        if self.audio is not None:
            # Call the plot_additional function with audio and sample_rate
            plot.plot_additional(self.audio, self.sample_rate)
        else:
            self.output_label.config(text="Load audio first.")

    # Plot 3 Plots in One
    def compile_plots(self):
        if self.audio is not None:
            plot.plot_combined_rt60(self.audio, self.sample_rate, self.freq_range)
        else:
            self.output_label.config(text="Load audio first.")

    # Update Text for Outputs
    def update_text_output(self, duration, resonant_freq, rt60_diff):
        output_text = (f"\nTotal Duration: {duration:.2f} seconds\nResonant Frequency: {resonant_freq:.2f} Hz\nRT60 "
                       f"Difference vs 0.5s: {rt60_diff:.2f} seconds")
        self.text_output_label.config(text=output_text)

    # Create Plots
    def create_plots(self, audio, sample_rate):
        pass


# Run Program
if __name__ == "__main__":
    app = SpidamApp()
    app.mainloop()
