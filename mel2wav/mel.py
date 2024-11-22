import librosa
import numpy as np

def librosa_pad_lr(x, fsize, fshift, pad_sides=1):
    '''compute right padding (final frame) or both sides padding (first and final frames)
    '''
    assert pad_sides in (1, 2)
    # return int(fsize // 2)
    pad = (x.shape[0] // fshift + 1) * fshift - x.shape[0]
    if pad_sides == 1:
        return 0, pad
    else:
        return pad // 2, pad // 2 + pad % 2


def librosa_wav2spec(wav_path,
                     fft_size=1024,
                     hop_size=320,
                     win_length=1024,
                     window="hann",
                     num_mels=80,
                     fmin=80,
                     fmax=7600,
                     eps=1e-6,
                     sample_rate=16000):
    if isinstance(wav_path, str):
        wav = np.load(wav_path)
        print(wav.shape)
    else:
        wav = wav_path

    # get amplitude spectrogram
    x_stft = librosa.stft(wav, n_fft=fft_size, hop_length=hop_size,
                          win_length=win_length, window=window, pad_mode="constant")
    linear_spc = np.abs(x_stft)  # (n_bins, T)

    # get mel basis
    fmin = 0 if fmin == -1 else fmin
    fmax = sample_rate / 2 if fmax == -1 else fmax
    mel_basis = librosa.filters.mel(sr=sample_rate, n_fft=fft_size, n_mels=num_mels, fmin=fmin, fmax=fmax)

    # calculate mel spec
    mel = mel_basis @ linear_spc
    mel = np.log10(np.maximum(eps, mel))  # (n_mel_bins, T)
    #l_pad, r_pad = librosa_pad_lr(wav, fft_size, hop_size, 1)
    #wav = np.pad(wav, (l_pad, r_pad), mode='constant', constant_values=0.0)
    wav = wav[:mel.shape[1] * hop_size]

    # log linear spec
    linear_spc = np.log10(np.maximum(eps, linear_spc))
    return {'wav': wav, 'mel': mel.T, 'linear': linear_spc.T, 'mel_basis': mel_basis}

