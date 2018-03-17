from __future__ import absolute_import
import six
import collections
from .base_stage import BaseStage
from .config_exceptions import BadAlphaTwirlInterfaceConfig
import os
import logging
logger = logging.getLogger(__name__)


__all__ = ["sequence_from_dict"]


class BadStagesDescription(BadAlphaTwirlInterfaceConfig):
    pass


def sequence_from_dict(stages, output_dir=os.getcwd(), **stage_descriptions):
    stages = _create_stages(stages, output_dir)
    _configure_stages(stages, stage_descriptions)

    pairs = []
    for stage in stages:
        pairs += stage.as_rc_pairs()
    return pairs


def _create_stages(stages, out_dir=os.getcwd()):
    return [_make_stage(i, out_dir, stage_cfg) for i, stage_cfg in enumerate(stages)]


def _configure_stages(stages, stage_descriptions):
    for stage in stages:
        name = stage.name
        cfg = stage_descriptions.get(name, None)
        if not cfg:
            raise BadStagesDescription("Missing description for stage '{}'".format(name))
        elif not isinstance(cfg, dict):
            raise BadStagesDescription("Description for stage '{}' is not a dictionary".format(name))
        stage.apply_description(**cfg)


def _make_stage(index, output_dir, stage_cfg, default_type="BinnedDataframe"):
    if isinstance(stage_cfg, six.string_types):
        stage_type = default_type
        name = stage_cfg
        args = {}
    elif isinstance(stage_cfg, dict):
        if len(stage_cfg) != 1:
            msg = "More than one key in dictionary spec for stage {} in stages list".format(index)
            logger.error(msg + "\n dictionary given: {}".format(stage_cfg))
            raise BadStagesDescription(msg)
        [(name, args)] = stage_cfg.items()
        stage_type = args.pop("type", default_type)
    else:
        msg = "Bad stage configuration, for stage {} in stages list".format(index)
        logger.error(msg + "\n Each stage config must be either a single string or a dictionary")
        raise BadStagesDescription(msg)

    # Find the actual concrete class based on the string
    stage_class = None
    for subclass in BaseStage.__subclasses__():
        if stage_type == subclass.__name__:
            stage_class = subclass
            break
    if not stage_class:
        raise BadStagesDescription("Unknown type for stage '{}': {}".format(name, stage_type))
    return stage_class(name, output_dir, **args)
