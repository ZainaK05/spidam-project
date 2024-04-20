# File Imports
import tkinter as tk
from tkinter import filedialog
import soundfile as sf
from data_manip import set_channel, meta_data_strip


# File Converted GUI
class SpidamApp:
    # Application Window
    def __init__(self, root):
        self.root = root
        # Application Title
        self.root.title("Audio Analyzer")
        # Application Sizing
        self.root.geometry("600x400")
        self.create_widgets()

    # Application Widget/Button
    def create_widgets(self):
        # Text Line 1, in Red
        self.info_label = tk.Label(self.root, text="Please select an audio file to analyze.", fg="red")
        self.info_label.pack()
        # Text Line 2, in Red
        self.info_label = tk.Label(self.root, text="If the file is not in WAV format, it will be converted.", fg="red")
        self.info_label.pack()
        # File Button
        self.load_button = tk.Button(self.root, text="Load Sample File", command=self.load_file)
        self.load_button.pack(pady=10)


    # Load File
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.aac")])
        if file_path:
            file_format = file_path.split(".")[-1]
            # File Conversion Check
            if file_format != "wav":
                self.convert_to_wav(file_path)
                set_channel(file_path)
            else:
                print("File format is already wav.")
                set_channel(file_path)

    # File Conversion
    def convert_to_wav(self, file_path):
        try:
            audio, sample_rate = sf.read(file_path)
            new_file_path = file_path.replace(file_path.split(".")[-1], "wav")
            sf.write(new_file_path, audio, sample_rate)
            print(f"File converted to wav: {new_file_path}")
        except Exception as e:
            print(f"Error converting file: {e}")


# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = SpidamApp(root)
    root.mainloop()