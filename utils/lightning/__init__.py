import gc
from .predict_utils import *


def clean_memory():
    gc.collect()
    torch.cuda.empty_cache()


def seed_everything(seed=42, workers=True):
    # Fix all random seeds to make experiments reproducible
    L.seed_everything(seed=seed, workers=workers)
