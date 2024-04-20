from pydub import AudioSegment
import os


def set_channel(fname):
    file_name = os.path.basename(fname)
    audio = AudioSegment.from_wav(file_name)
    mono_chan = audio.set_channels(1)
    file = os.path.splitext(file_name)
    mono_chan.export(f"{file[0]}_mono_chan.wav", format="wav")
