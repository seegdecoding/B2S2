import os
import traceback

import numpy as np
import torch

from utils.commons.ckpt_utils import get_last_checkpoint
from utils.commons.hparams import hparams
from utils.commons.trainer import Trainer
import torch_xla.core.xla_model as xm
import torch_xla.distributed.parallel_loader as pl
import torch_xla.distributed.xla_multiprocessing as xmp


def move_to_tpu(batch, *args, **kwargs):
    device = xm.xla_device()
    # base case: object can be directly moved using `cuda` or `to`
    if callable(getattr(batch, 'to', None)):
        return batch.to(device, non_blocking=True)
    elif isinstance(batch, list):
        for i, x in enumerate(batch):
            batch[i] = move_to_tpu(x)
        return batch
    elif isinstance(batch, tuple):
        batch = list(batch)
        for i, x in enumerate(batch):
            batch[i] = move_to_tpu(x)
        return tuple(batch)
    elif isinstance(batch, dict):
        for k, v in batch.items():
            batch[k] = move_to_tpu(v)
        return batch
    return batch


class TPUTrainer(Trainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_gpu_ids = [
            int(x) for x in os.environ.get("CUDA_VISIBLE_DEVICES", "").split(",") if x != '']
        self.use_ddp = False
        torch.set_default_tensor_type('torch.FloatTensor')
        self.device = xm.xla_device()
        self.on_device = True
        self.move_to_device_fn = move_to_tpu

    def fit(self, task_cls):
        self.task = task_cls()
        self.task.trainer = self
        self.run_single_process(self.task)
        return 1

    def optimizer_step(self, optimizer):
        xm.optimizer_step(optimizer)
