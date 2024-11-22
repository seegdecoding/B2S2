from mel import librosa_wav2spec
from model import HifiGAN
from utils.hparams import set_hparams
import numpy as np
from scipy.io import wavfile

def save_wav(wav, path, sr, norm=False):
    if norm:
        wav = wav / np.abs(wav).max()
    wav = wav * 32767
    wavfile.write(path[:-4] + '.wav', sr, wav.astype(np.int16))

set_hparams()
vocoder = HifiGAN()

import glob
mel_list = glob.glob('/path/to/mel/*.npy')

for mel_name in mel_list:
    mel = np.load(mel_name)
    wav_gen = vocoder.spec2wav(mel)
    save_wav(wav_gen, mel_name.replace('.npy', '.wav'), 16000)

