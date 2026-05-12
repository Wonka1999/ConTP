import argparse
import json
import os
from argparse import Namespace

import omegaconf
from omegaconf import OmegaConf

from .. import root_path


def log_config(config, prefix='config'):
    # Pretty-print a config object (dict / Namespace / omegaconf.dictconfig.DictConfig)
    if type(config) == dict:
        pass
    elif type(config) == omegaconf.dictconfig.DictConfig:
        config = OmegaConf.to_object(config)
    elif type(config) == argparse.Namespace:
        config = vars(config)
    else:
        raise RuntimeError(f'Param args is with illegal type: {config}')
    print(f'[{prefix}]:')
    print(json.dumps(config, indent=4, ensure_ascii=False))  # indent 4 spaces; keep non-ASCII characters as-is


def config_to_namespace(config):
    # Convert config from OmegaConf to Namespace
    return Namespace(**OmegaConf.to_object(config))


def namespace_to_config(config):
    # Convert config from Namespace to OmegaConf
    return OmegaConf.create(vars(config))


def config_to_dict(config):
    # Convert config from OmegaConf to dict
    return OmegaConf.to_object(config)


def dict_to_config(config_dict):
    # Convert config from dict to OmegaConf
    return OmegaConf.create(config_dict)


def load_config(path):
    # Load saved parameters from a Lightning checkpoint's hparams file
    config = OmegaConf.load(path)
    try:  # Lightning saves parameters under the "config" field by default
        config = config.config
    except:  # plain yaml file without the "config" field
        pass
    return config


def merge_config(config, *args):
    # Update config; uniformly handle dict, yaml file paths, and command-line arguments
    for x in args:
        if type(x) == dict:
            # dict: key-value pairs
            config = OmegaConf.merge(config, x)
        elif type(x) == str:
            if x.endswith('.yaml') and '=' not in x:
                # yaml path
                config = OmegaConf.merge(config, OmegaConf.load(x))
            else:
                # command line arguments
                config = OmegaConf.merge(config, OmegaConf.from_dotlist([x]))
        else:
            raise RuntimeError(f'Invalid type: {type(x)} of {x}')
    return config


def parse_config(*args):
    '''
    Load configuration, including project settings and model hyper-parameters.
    Supports reading from yaml files, custom parameter dicts, and command-line arguments.
    :param *args: parameter overrides
    :return: args: OmegaConf (omegaconf.dictconfig.DictConfig)
    '''
    cmd_args = os.sys.argv[1:]

    if len(cmd_args) > 0:
        if cmd_args[0] == '-f':
            cmd_args = cmd_args[2:]
        print('cmd_args', cmd_args)

    default_config = OmegaConf.create()
    default_config_list = ['utils/config/default_config/project/project.yaml',
                           # 'utils/config/default_config/project/nni.yaml',
                           'utils/config/default_config/lightning/LitData.yaml',
                           'utils/config/default_config/lightning/LitModel.yaml',
                           'utils/config/default_config/dataset/MyDataset.yaml',
                           'utils/config/default_config/model/MyModel.yaml']
    default_config_list = [os.path.join(root_path, x) for x in default_config_list]
    default_config = merge_config(default_config, *default_config_list)
    config = merge_config(default_config, *args, *cmd_args)
    return config


if __name__ == '__main__':
    config = parse_config()
    print('========== format config ==========')
    log_config(config)
