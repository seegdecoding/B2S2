import numpy as np
import torch
from hifigan.hifigan import HifiGanGenerator
from utils.ckpt_utils import load_ckpt
from utils.hparams import set_hparams, hparams
from utils.meters import Timer

total_time = 0



class HifiGAN():
    def __init__(self):
        base_dir = hparams['vocoder_ckpt']
        config_path = f'{base_dir}/config.yaml'
        config = set_hparams(config_path, global_hparams=False)
        hparams.update(config)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = HifiGanGenerator(hparams)
        load_ckpt(self.model, base_dir, 'model_gen')
        self.model.to(self.device)
        self.model.eval()


    def spec2wav(self, mel):
        device = self.device
        with torch.no_grad():
            if isinstance(mel, np.ndarray):
                mel = torch.FloatTensor(mel)
            mel = mel.unsqueeze(0).to(device)
            p = None
            mel = mel.transpose(2, 1)
            with Timer('hifigan', enable=hparams['profile_infer']):
                y = self.model(mel, f0=p).view(-1)
        wav_out = y.cpu().numpy()
        return wav_out

