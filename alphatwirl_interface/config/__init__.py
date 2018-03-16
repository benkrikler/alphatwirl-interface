import base_stage
import binned_df_stage
import cutflow_stage


__all__ = ["read_yaml"]


from .dict_config import sequence_from_dict


def read_yaml(cfg_filename, output_dir=None):
    import yaml
    with open(cfg_filename, "r") as infile:
        cfg = yaml.load(infile)

    # Override the output_dir in the config file if this function is given one
    if output_dir:
        cfg["output_dir"] = output_dir

    return sequence_from_dict(**cfg)
