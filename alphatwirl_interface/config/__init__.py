import base_stage
import binned_df_stage
import cutflow_stage
import os


__all__ = ["read_yaml"]


from .dict_config import Sequence


def read_yaml(cfg_filename, output_dir=None):
    import yaml
    with open(cfg_filename, "r") as infile:
        cfg = yaml.load(infile)
    if output_dir:
        dict_cfg["output_dir"] = output_dir

    sequence = Sequence(**dict_cfg)
    return sequence.to_reader_collector_pairs()
