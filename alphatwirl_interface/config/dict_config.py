from __future__ import absolute_import
import six
import collections
#import base_stage
from .base_stage import BaseStage
from .config_exceptions import BadAlphaTwirlInterfaceConfig
import os
import logging
logger = logging.getLogger(__name__)


__all__ = ["Sequence"]


class BadStagesDescription(BadAlphaTwirlInterfaceConfig):
    pass


class Sequence():
    def __init__(self, stages, output_dir=os.getcwd(), **stage_descriptions):
        self.output_dir = output_dir
        self.stages = self._create_stages(stages, self.output_dir)
        self._configure_stages(self.stages, stage_descriptions)

    @staticmethod
    def _create_stages(self, stages, out_dir=os.getcwd()):
        stages = [make_stage(i, out_dir, stage_cfg) for i, stage_cfg in enumerate(stages)]
        stage_names = [stage.name for stage in stages]
        return collections.OrderedDict(zip(stage_names, stages))

    @staticmethod
    def _configure_stages(self, stages, stage_descriptions):
        for name, stage in stages.items():
            cfg = stage_descriptions.get(name, None)
            if not cfg:
                raise BadStagesDescription("Missing description for stage '{}'".format(name))
            elif not isinstance(cfg, dict):
                raise BadStagesDescription("Description for stage '{}' is not a dictionary".format(name))
            stage.apply_description(**cfg)

    def validate(self):
        raise NotImplementedError

    def to_reader_collector_pairs(self):
        pairs = []
        for stage in self.stages:
            pairs += stage.as_rc_pairs()
        return pairs


def make_stage(index, output_dir, stage_cfg, default_type="BinnedDataframe"):
    if isinstance(stage_cfg, six.string_types):
        return default_type(stage_cfg)
    elif not isinstance(stage_cfg, dict):
        msg = "Bad stage configuration, for stage {} in stages list".format(index)
        logger.error(msg + "\n Each stage config must be either a single string or a dictionary")
        raise BadStagesDescription(msg)

    if len(stage_cfg) != 1:
        msg = "More than one key in dictionary spec for stage {} in stages list".format(index)
        logger.error(msg + "\n dictionary given: {}".format(stage_cfg))
        raise BadStagesDescription(msg)
    name, args = stage_cfg.items()[0]
    stage_type = args.pop("type", default_type)

    # Find the actual concrete class based on the string
    stage_class = None
    for subclass in BaseStage.__subclasses__():
        if stage_type == subclass.__name__:
            stage_class = subclass
            break
    if not stage_class:
        raise BadStagesDescription("Unknown type for stage '{}': {}".format(name, stage_type))
    return stage_class(name, output_dir, **args)
