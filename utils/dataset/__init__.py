import pandas as pd
from sklearn.model_selection import train_test_split

from .ProteinDataset import ProteinDataset
from .Tokenizer import *


def split_dataset(dataframe, test_size=0.2, valid_size=None, stratify=None, mode=None, q=None, seed=42):
    dataframe = dataframe.copy()
    stratify_col = 'length' if stratify is None else stratify

    if mode is None:  # auto mode detection
        if pd.api.types.is_integer_dtype(dataframe[stratify_col]):
            mode = 'discrete'
        elif pd.api.types.is_string_dtype(dataframe[stratify_col]):
            mode = 'discrete'
        elif pd.api.types.is_numeric_dtype(dataframe[stratify_col]):
            mode = 'continuous'
        else:
            raise ValueError(f'Unsupported data type {dataframe[stratify].dtype}')

    if mode == 'continuous':
        stratify_col = stratify_col + '_bin'
        q = len(dataframe) // 10 if q is None else q
        dataframe[stratify_col] = pd.qcut(dataframe[stratify], q=q)
    else:
        pass

    # Stratified split of train and test sets
    train_indices, test_indices = [], []
    if test_size > 0:
        no_nan_indices = dataframe[~dataframe[stratify_col].isnull()].index
        stratify_values = dataframe.loc[no_nan_indices, stratify_col]

        train_indices, test_indices = train_test_split(
            no_nan_indices,
            test_size=test_size,
            random_state=seed,
            stratify=stratify_values
        )
        dataframe.loc[train_indices, 'split'] = 'train'
        dataframe.loc[test_indices, 'split'] = 'test'
    else:
        train_indices = dataframe[~dataframe[stratify_col].isnull()].index
        dataframe['split'] = 'train'

    # If a validation-set size is provided, further split the training set
    valid_indices = []
    if valid_size is not None:
        train_indices, valid_indices = train_test_split(
            train_indices,
            test_size=valid_size,
            random_state=seed,
            stratify=dataframe.loc[train_indices, stratify_col]
        )
        dataframe.loc[valid_indices, 'split'] = 'valid'

    indices = {
        'train': train_indices,
        'valid': valid_indices,
        'test': test_indices
    }
    return dataframe, indices
