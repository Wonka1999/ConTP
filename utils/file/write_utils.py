import json

import numpy as np
import pandas as pd
import torch
import yaml
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def data2file(data, path, **kwargs):
    # Save data to disk; dispatch by the output file extension. Returns True on success, raises otherwise.
    suffix = path.split(".")[-1]
    if suffix == "fasta":
        write_fasta(path, data, **kwargs)
    elif suffix == "pt":
        torch.save(data, path, **kwargs)
    elif suffix == "npy":
        np.save(path, data, **kwargs)
    elif suffix == "xlsx":
        data.to_excel(path, **kwargs)
    elif suffix == "tsv":
        data = pd.DataFrame(data) if type(data) != pd.DataFrame else data
        data.to_csv(path, sep="\t", **kwargs)
    elif suffix == "csv":
        data = pd.DataFrame(data) if type(data) != pd.DataFrame else data
        data.to_csv(path, sep=",", **kwargs)
    elif suffix == "yaml":
        with open(path, "w") as f:
            yaml.dump(data, f, **kwargs)
    elif suffix == "json":
        with open(path, "w") as f:
            json.dump(data, f, **kwargs)
    else:
        write_file(data, path, **kwargs)
    return True


def write_file(text, file, **kwargs):
    # Write text content to a file
    with open(file, "w") as f:
        f.write(text)


def write_fasta(path, seqs, custom_index=None, description=None):
    """
    Write a fasta file via biopython.
    :param path: output file path
    :param seqs: list of sequences
    :param custom_index: custom record indices; defaults to 0..len(seqs)-1 when None
    :param description: per-sequence description or label list
    """
    custom_index = [str(i) for i in range(len(seqs))] if custom_index is None else custom_index
    records = []
    for i in range(len(seqs)):
        if description is None:
            seq_record = SeqRecord(Seq(seqs[i]), id=custom_index[i], description="")
        else:
            seq_record = SeqRecord(Seq(seqs[i]), id=custom_index[i], description=f"| {description[i]}")
        records.append(seq_record)
    try:
        SeqIO.write(records, path, "fasta")
    except Exception:
        raise RuntimeError("Failed to write fasta")


def write_yaml(path, data, **kwargs):
    # Serialize data to a yaml file
    assert ".yaml" in path, "output file must be a yaml file"
    with open(path, "w") as f:
        yaml.dump(data, f, **kwargs)


def write_data_label_pair_file(path, seqs, labels, custom_index=None):
    """
    Write (seq_list, label_list) to an xlsx/csv/tsv table file.
    Returns True on success, raises otherwise.
    :param path: output file path
    :param seqs: list of sequences
    :param labels: list of labels
    :param custom_index: custom record indices; defaults to 0..len(seqs)-1 when None
    :return: True
    """
    custom_index = [i for i in range(len(seqs))] if custom_index is None else custom_index
    df = pd.DataFrame({"Index": custom_index, "Data": seqs, "Label": labels})
    if "xlsx" in path:
        df.to_excel(path, index=False)
    else:
        sep = "\t" if ".tsv" in path else ","
        df.to_csv(path, sep=sep, index=False)
    return True
