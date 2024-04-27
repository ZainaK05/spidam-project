# gui.py

# File Imports
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        self.geometry("800x600")

        # Cycle Button
        self.current_graph = "low"  # Initial state
        self.graph_label = tk.Label(self, text="")

        # Define Parameters - Unsure if Necessary
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
        self.canvas_waveform = None
        self.compile_plots_button = None
        self.freq_range = {'low': (60, 250), 'mid': (200, 2000), 'high': (5000, 10000)}
        self.create_widgets()

    # Create Application Widget/Buttons
    def create_widgets(self):

        # Set Uniform Column Sizing
        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=1, uniform="equal")
        self.grid_columnconfigure(2, weight=1, uniform="equal")
        self.grid_columnconfigure(3, weight=1, uniform="equal")
        self.grid_columnconfigure(4, weight=1, uniform="equal")
        self.grid_columnconfigure(5, weight=1, uniform="equal")
        self.grid_columnconfigure(6, weight=1, uniform="equal")
        self.grid_columnconfigure(7, weight=1, uniform="equal")

        # Text Line 1, in Red
        self.info_label = tk.Label(self, text="Please select an audio file to analyze.", fg="red")
        self.info_label.grid(row=0, column=2, columnspan=4)

        # Text Line 2, in Red
        self.info_label = tk.Label(self, text="If the file is not in WAV format, it will be converted.\n", fg="red")
        self.info_label.grid(row=1, column=2, columnspan=4)

        # Load File Button
        self.load_button = tk.Button(self, text="Load Audio File", command=self.load_file)
        self.load_button.grid(row=2, column=2, columnspan=4)

        # Output Label
        self.output_label = tk.Label(self, text="")
        self.output_label.grid(row=3, column=2, columnspan=4)

        # Wave Buttons
        self.plot_waveform_button = tk.Button(self, text="Waveform", command=self.plot_waveform, width=10, height=1)
        self.plot_waveform_button.grid(row=5, column=1, columnspan=1)

        self.plot_low_rt60_button = tk.Button(self, text="Low RT60", command=self.plot_low_rt60, width=10, height=1)
        self.plot_low_rt60_button.grid(row=5, column=2, columnspan=1)

        self.plot_mid_rt60_button = tk.Button(self, text="Mid RT60", command=self.plot_mid_rt60, width=10, height=1)
        self.plot_mid_rt60_button.grid(row=5, column=3, columnspan=1)

        self.plot_high_rt60_button = tk.Button(self, text="High RT60", command=self.plot_high_rt60, width=10, height=1)
        self.plot_high_rt60_button.grid(row=5, column=4, columnspan=1)

        # Button to compile plots
        self.compile_plots_button = tk.Button(self, text="Compile", command=self.compile_plots, width=10, height=1)
        self.compile_plots_button.grid(row=5, column=5, columnspan=1)

        # Button for Spectrogram
        self.plot_additional_button = tk.Button(self, text="Additional", command=self.plot_additional, width=10, height=1)
        self.plot_additional_button.grid(row=5, column=6, columnspan=1)

        # Cycle Button
        self.cycle_button = tk.Button(self, text="Cycle", command=self.cycle_graph, width=10, height=1)
        self.cycle_button.grid(row=7, column=2, columnspan=4)

        # Bottom Text
        self.text_output_label = tk.Label(self, text="")
        self.text_output_label.grid(row=8, column=2, columnspan=4)

        # Create Waveform Plot Canvas (Couldn't Figure Out How to Implement Plots)
        self.canvas_waveform = FigureCanvasTkAgg(plt.Figure(figsize=(5, 4)))
        self.canvas_waveform.get_tk_widget().grid(row=10, column=2, columnspan=4)

    # Ensures Graph Labels for Cycle Button Only Appears When Button is Pressed
    def hide_graph_label(self):
        # Hide the graph label
        self.graph_label.grid_remove()

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

        # Calculate Total Duration
        total_duration = len(self.audio) / self.sample_rate

        # Calculate Resonant Frequency
        resonant_frequency = 539.06  # Placeholder Value

        # Calculate RT60
        rt60_difference = 0.5  # Placeholder Value

        # Show Results of Processing
        if self.audio is not None:
            # If Audio Loads Correctly
            print("Processing completed successfully.")
            self.create_plots(self.audio, self.sample_rate)
            # Update GUI with Calculated Values
            self.update_text_output(total_duration, resonant_frequency, rt60_difference)
        else:
            # Exception Handling
            print("Error processing audio.")

    # Plot Regular Waveform
    def plot_waveform(self):
        self.graph_label.grid_remove()
        if self.audio is not None:
            plot.plot_waveform(self.audio, self.sample_rate)
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Plot Low Frequency Waveform
    def plot_low_rt60(self):
        self.graph_label.grid_remove()
        if self.audio is not None:
            plot.plot_rt60(self.audio, self.sample_rate, self.freq_range['low'], "Low RT60")
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Plot Middle Frequency Waveform
    def plot_mid_rt60(self):
        self.graph_label.grid_remove()
        if self.audio is not None:
            plot.plot_rt60(self.audio, self.sample_rate, self.freq_range['mid'], "Mid RT60")
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Plot High Frequency Waveform
    def plot_high_rt60(self):
        self.graph_label.grid_remove()
        if self.audio is not None:
            plot.plot_rt60(self.audio, self.sample_rate, self.freq_range['high'], "High RT60")
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Plot Additional Waveform
    def plot_additional(self):
        self.graph_label.grid_remove()
        if self.audio is not None:
            # Call the plot_additional function with audio and sample_rate
            plot.plot_additional(self.audio, self.sample_rate)
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Plot 3 Plots in One
    def compile_plots(self):
        self.graph_label.grid_remove()
        if self.audio is not None:
            plot.plot_combined_rt60(self.audio, self.sample_rate, self.freq_range)
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Update Text for Outputs
    def update_text_output(self, duration, resonant_freq, rt60_diff):
        self.hide_graph_label()
        output_text = (f"\nTotal Duration: {duration:.2f} seconds\nResonant Frequency: {resonant_freq:.2f} Hz\nRT60 "
                       f"Difference vs 0.5s: {rt60_diff:.2f} seconds")
        self.text_output_label.config(text=output_text)

    def cycle_graph(self):

        if self.audio is not None:
            # Update the current graph state
            if self.current_graph == "low":
                self.current_graph = "mid"
                self.plot_mid_rt60()  # Call the Method
            elif self.current_graph == "mid":
                self.current_graph = "high"
                self.plot_high_rt60()  # Call the Method
            elif self.current_graph == "high":
                self.current_graph = "low"
                self.plot_low_rt60()  # Call the Method
            else:
                self.current_graph = "low"  # Start with "low"

            # Update Label for Cycle
            self.update_graph_label()
        else:
            # Error Handling
            self.output_label.config(text="\nPlease Select an Audio File.\n")

    # Update Labels for Cycle
    def update_graph_label(self):
        # Update Label for Cycle
        self.graph_label.config(text=f"Current Graph: {self.current_graph.capitalize()}")
        self.graph_label.grid(row=9, column=2, columnspan=4)

    # Create Plots
    def create_plots(self, audio, sample_rate):
        pass


# Run Program
if __name__ == "__main__":
    app = SpidamApp()
    app.mainloop()
