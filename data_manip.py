# data_manip.py

# Import Files
import soundfile as sf
import numpy as np


# First Check File Path of Audio
def check_file(file_path):
    try:
        audio, sample_rate = sf.read(file_path)
        return audio, sample_rate
    except Exception as e:
        # Exception Handling
        print(f"Error reading file: {e}")
        return None, None


# Remove Metadata Tags
def remove_metadata(audio):
    if hasattr(audio, 'info') and isinstance(audio.info, dict):
        # Check if Metadata Tags are Present
        if 'metadata' in audio.info:
            # Remove Metadata Tags
            audio = audio.without_metadata()
            print("Metadata removed successfully.")
        else:
            # No Metadata Found
            print("No metadata found in the audio.")
    else:
        # Exception Handling
        print("Audio object does not have valid metadata information.")
    print("Proceeding with audio plot...")

    return audio


# Process Audio
def process_audio(file_path):
    audio, sample_rate = check_file(file_path)
    if audio is not None:
        audio = remove_metadata(audio)
        audio_mono = convert_to_mono(audio)
        return audio_mono, sample_rate
    else:
        return None, None


def convert_to_mono(audio):
    if isinstance(audio, np.ndarray):
        if audio.ndim > 1:
            # Check Number of Audio Channels
            num_channels = audio.shape[1]
            if num_channels > 2:
                # Turn Multi to Stereo before Converting to Mono
                audio = np.mean(audio, axis=1)
                print("Converted multi-channel audio to stereo audio.")

            # Convert stereo audio to mono
            audio_mono = np.mean(audio, axis=1)
            print("Converted to mono audio.")
            return audio_mono
        else:
            return audio
    else: #
        print("Invalid audio object format, please try again.")
        return None

