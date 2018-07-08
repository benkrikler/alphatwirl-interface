from __future__ import absolute_import
import os
import six
import importlib
from .base_stage import BaseStage
from .config_exceptions import BadAlphaTwirlInterfaceConfig
import alphatwirl
from alphatwirl_interface.completions import to_null_collector_pairs


__all__ = ["Scribbler"]


class BadScribblerConfig(BadAlphaTwirlInterfaceConfig):
    pass


class Scribbler(BaseStage):
    def apply_description(self, module, scribblers):
        #package, module = os.path.splitext(module)
        #print "BEK", module, package
        #mod = importlib.import_module(module, package=package)
        mod = importlib.import_module(module)
        self._scribblers = _make_scribblers(self.name, mod, scribblers)

    def as_rc_pairs(self):
        if not hasattr(self, "_reader_collector_pair"):
            self._reader_collector_pair = self._create_rc_pairs()
        return self._reader_collector_pair

    def _create_rc_pairs(self):
        return to_null_collector_pairs(self._scribblers)


def _make_scribblers(stage_name, module, scribbler_list):
    if isinstance(scribbler_list, six.string_types):
        return [_make_one_scribbler(stage_name, module, scribbler_list)]

    if not isinstance(scribbler_list, list):
        msg = "{}: scribblers should be either a single string, or "
        msg += "a list of names and optionally a dictionary of keyword arguments"
        raise BadScribblerConfig(msg.format(stage_name))

    scribblers = []
    for i, scribbler in enumerate(scribbler_list):
        if isinstance(scribbler, six.string_types):
            scribblers.append(_make_one_scribbler(stage_name, module, scribbler))
        elif isinstance(scribbler, dict):
            if len(scribbler) != 1:
                msg = "{}: Dictionary for scribbler {} should contain only one key, the class of the scribbler"
                raise BadScribblerConfig(msg.format(stage_name, i))
            scribbler, args = list(scribbler.items())[0]
            scribblers.append(_make_one_scribbler(stage_name, module, scribbler, args=args, index=i))
    return scribblers


def _make_one_scribbler(stage_name, mod, scribbler, args={}, index=None):
    if not isinstance(args, dict):
        msg = "{}: Args for scribbler {} aren't a dictionary"
        scribbler_name = scribbler
        if index is not None:
            scribbler_name += str(index) + ", '{}'"
        raise BadScribblerConfig(msg.format(stage_name, scribbler_name))
    scribbler = getattr(mod, scribbler)
    return scribbler(**args)
