from __future__ import absolute_import
import copy
import six
import numpy as np
from .base_stage import BaseStage
from .config_exceptions import BadAlphaTwirlInterfaceConfig


from alphatwirl.configure import TableConfigCompleter, TableFileNameComposer
from alphatwirl_interface.completions import complete
from alphatwirl.binning import Binning, Echo


__all__ = ["BinnedDataframe"]


class BadBinnedDataframeConfig(BadAlphaTwirlInterfaceConfig):
    pass


class BinnedDataframe(BaseStage):
    def apply_description(self, binning, weights=None):
        self._binning = _create_binning_list(self.name, binning)
        self._weights = _create_weights(weights)

    def as_rc_pairs(self):
        if not hasattr(self, "_reader_collector_pair"):
            self._reader_collector_pair = self._create_rc_pairs()
        return self._reader_collector_pair

    def _create_rc_pairs(self):
        keyAttrNames, keyOutColumnNames, binnings, keyIndices = zip(*self._binning)
        if not any(keyIndices):
            keyIndices = None
        base_cfg = dict(keyAttrNames=keyAttrNames,
                        keyOutColumnNames=keyOutColumnNames,
                        binnings=binnings,
                        keyIndices=keyIndices
                       )

        df_configs = {}
        if not self._weights:
            name_composer = TableFileNameComposer()
            df_configs["unweighted"] = base_cfg
        else:
            for name, weights in self._weights.items():
                config = copy.copy(base_cfg)
                if weights != 1:
                    config["weight"] = weights
                df_configs[name] = config

            name_composer = WithInsertTableFileNameComposer(TableFileNameComposer(), df_configs.keys())
            tableConfigCompleter = TableConfigCompleter(createOutFileName=name_composer, defaultOutDir=self.output_dir)

        return complete(df_configs.values(), tableConfigCompleter)


def _create_binning_list(stage_name, bin_list):
    if not isinstance(bin_list, list):
        raise BadBinnedDataframeConfig("binning section for stage '{}' not a list".format(stage_name))
    binning = []
    for i, one_bin_dimension in enumerate(bin_list):
        if not isinstance(one_bin_dimension, dict):
            raise BadBinnedDataframeConfig("binning item no. {} is not a dictionary".format(i))
        cleaned_dimension_dict = {"_" + k: v for k, v in one_bin_dimension.items()}
        binning.append(_create_one_dimension(stage_name, **cleaned_dimension_dict))
    return binning


def _create_one_dimension(stage_name, _in, _out, _bins=None, _index=None):
    if not isinstance(_in, six.string_types):
        msg = "{}: binning dictionary contains non-string value for 'in'"
        raise BadBinnedDataframeConfig(msg.format(stage_name))
    if not isinstance(_out, six.string_types):
        msg = "{}: binning dictionary contains non-string value for 'out'"
        raise BadBinnedDataframeConfig(msg.format(stage_name))
    if _index and not isinstance(_index, six.string_types):
        msg = "{}: binning dictionary contains non-string and non-integer value for 'index'"
        raise BadBinnedDataframeConfig(msg.format(stage_name))

    if _bins is None:
        bin_obj = Echo(nextFunc=None)
    elif isinstance(_bins, dict):
        # - bins: {nbins: 6 , low: 1  , high: 5 , overflow: True}
        # - bins: {edges: [0, 200., 900], overflow: True}
        if "nbins" in _bins and "low" in _bins and "high" in _bins:
            low = _bins["low"]
            high = _bins["high"]
            nbins = _bins["nbins"]
            edges = np.linspace(low, high, nbins + 1)
        elif "edges" in _bins:
            edges = _bins["edges"]
        else:
            msg = "{}: No way to infer binning edges for in={}"
            raise BadBinnedDataframeConfig(msg.format(stage_name, _in))
        bin_obj = Binning(boundaries=edges)
    else:
        msg = "{}: bins is neither None nor a dictionary for in={}"
        raise BadBinnedDataframeConfig(msg.format(stage_name, _in))

    return (str(_in), str(_out), bin_obj, _index)


def _create_weights(weights):
    if weights is None:
        return None
    if isinstance(weights, list):
        return {str(w): w for w in weights}
    elif isinstance(weights, dict):
            return weights
    # else we've got a single, scalar value
    return {"weighted": weights}


class WithInsertTableFileNameComposer():
    def __init__(self, composer, inserts):
        self.inserts = inserts
        self.composer = composer
        self.frame_idx = 0

    def __call__(self, columnNames, indices, **kwargs):
        this_insert = self.inserts[self.frame_idx]
        suffix = kwargs.get("suffix", self.composer.default_suffix)
        kwargs["suffix"] = "--{}.{}".format(this_insert, suffix)
        self.frame_idx += 1
        return self.composer(columnNames, **kwargs)
