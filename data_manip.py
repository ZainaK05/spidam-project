import pydub as pd
from pydub import utils, AudioSegment


def audio_manip(fname):
    file_name = fname
    audio = AudioSegment.from_wav(file_name)
    mono_chan = audio.set_channels(1)
    meta_data = pd.utils.mediainfo(r"C:\Users\alawr\PycharmProjects\Sound project\spidam-project\Clap1_mono_chan.wav")
    print(meta_data)
    mono_chan.export(f"{file_name}_mono_chan.wav", format="wav")


audio_manip("Clap2.wav")
