from __future__ import absolute_import
import re
import six
import numpy as np
from .base_stage import BaseStage
from .config_exceptions import BadAlphaTwirlInterfaceConfig


__all__ = ["BinnedDataframe"]


class BadCutflowConfig(BadAlphaTwirlInterfaceConfig):
    pass


class BadSelectionFile(BadAlphaTwirlInterfaceConfig):
    pass


class MultipleWeightedSelectionsNotImplemented(UserWarning):
    pass


class CutFlow(BaseStage):
    output_filename = "cut_flow.txt"
    def apply_description(self, selection_file=None, selection=None, aliases=None,
                          lambda_arg="ev", counter=True, counter_weights=None):
        if not selection and not selection_file:
            raise BadCutflowConfig("{}: Neither selection nor selection_file specified".format(self.name))
        if selection and selection_file:
            raise BadCutflowConfig("{}: Both selection and selection_file given. Choose one!".format(self.name))

        if selection_file:
            selection, aliases = self._load_selection_file(selection_file)
        self.selection = self._prepare_selection(self.name, selection, lambda_arg, aliases)

        self._weights = _create_weights(weights)

    def as_rc_pairs(self):
        if hasattr(self, "_reader_collector_pair"):
            self._reader_collector_pair = self._create_rc_pairs()
        return self._reader_collector_pair

    def _create_rc_pairs(self):
        return [Selection(self.selection, os.path.join(self.output_dir, self.output_filename))]


def _load_selection_file(selection_file):
    import yaml
    with open(selection_file, "r") as infile:
        cfg = yaml.load(infile)
    if "selection" not in cfg:
        raise BadSelectionFile("No `selection` section in selection file '{}'".format(selection_file))
    selection = cfg.pop("selection")
    aliases = cfg.pop("aliases", None)
    if cfg:
        raise BadSelectionFile("Unknown sections in selection file '{}': {}".format(selection_file, cfg.keys()))
    return selection, aliases


def _prepare_selection(stage_name, selection, lambda_arg="ev", aliases=None):
    # Despite how much we've heard about alphatwirl using dependency injection,
    # the alphatwirl.selection.build_selection method doesn't presently allow
    # me to inject a custom FactoryDispatcher, so we need to pre-process the
    # dictionaries instead

    if aliases and not isinstance(aliases, dict):
        raise BadCutflowConfig("{}: aliases is not a dictionary".format(stage_name))
    if isinstance(selection, dict):
        selection = _recurse_selection(stage_name, selection, lambda_arg, aliases)
    return selection


def _recurse_selection(stage_name, selection, lambda_arg="ev", aliases=None):
    if isinstance(selection, dict):
        tidied_selection = {}
        for key, value in selection.items():
            if key not in ("All", "Any", "Not"):
                tidied_selection[key] = value
                continue
            tidied_selection[key] = _recurse_selection(stage_name, value, lambda_arg, aliases)
    elif isinstance(selection, (list, tuple)):
        tidied_selection = [_recurse_selection(stage_name, element, lambda_arg, aliases) for element in selection]
    else:
        # Assume something scalar (string, bool, int), etc
        tidied_selection = _process_single_selection(stage_name, selection, lambda_arg, aliases)
    return tidied_selection


def _process_single_selection(stage_name, selection, lambda_arg="ev", aliases=None):
    if aliases:
        # Get the alias if there is one else returns the original selection unchanged
        selection = aliases.get(selection, selection)

    if not isinstance(selection, six.string_types):
        # Might sometimes be given other things, like bools, etc
        return str(selection)
    else:
        regex = r"{}\s*\.".format(lambda_arg)
        if re.search(regex, selection):
            return "{}: {}".format(lambda_arg, selection)

    raise BadCutflowConfig("{}: Issue pre-processing selection '{}'".format(stage_name, selection))


def _create_weights(stage_name, weights):
    if weights is None or isinstance(weights, six.string_types):
        return weights

    if isinstance(weights, (tuple, list)):
        if len(weights) != 1:
            raise MultipleWeightedSelectionsNotImplemented("{}: Sorry!  We'll add this soon...".format(stage_name))
        return weights[0]
    raise BadCutflowConfig("{}: Cannot process weight specification".format(stage_name))
