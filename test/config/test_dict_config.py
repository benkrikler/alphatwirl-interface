import pytest
import alphatwirl_interface.config.dict_config as dict_config
from alphatwirl_interface.config.binned_df_stage import BinnedDataframe
from alphatwirl_interface.config.cutflow_stage import CutFlow


def test__make_stage_string(tmpdir):
    stage = dict_config._make_stage(1, tmpdir, "just_a_stage_name", default_type="BinnedDataframe")
    assert isinstance(stage, BinnedDataframe)
    assert stage.name == "just_a_stage_name"


@pytest.fixture
def binned_df_cfg():
    return {"my_first_stage": {"type": "BinnedDataframe"}}


@pytest.fixture
def cutflow_cfg():
    return {"my_second_stage": {"type": "CutFlow"}}


def test__make_stage_binned_df(tmpdir, binned_df_cfg):
    stage = dict_config._make_stage(2, tmpdir, binned_df_cfg)
    assert isinstance(stage, BinnedDataframe)
    assert stage.name == "my_first_stage"


def test__make_stage_cutflow(tmpdir, cutflow_cfg):
    stage = dict_config._make_stage(2, tmpdir, cutflow_cfg)
    assert isinstance(stage, CutFlow)
    assert stage.name == "my_second_stage"


def test__make_stage_raises(tmpdir):
    with pytest.raises(dict_config.BadStagesDescription) as ex:
        cfg = {"my_third_stage": {"type": "bad_stage_type"}}
        dict_config._make_stage(3, tmpdir, cfg)
    assert "Unknown type" in str(ex)

    with pytest.raises(dict_config.BadStagesDescription) as ex:
        cfg = {"my_third_stage": {"type": "CutFlow"},
               "bad_fourth_stage": {"type": "BinnedDataframe"}}
        dict_config._make_stage(4, tmpdir, cfg)
    assert "More than one key" in str(ex)


@pytest.fixture
def a_stage_list(binned_df_cfg, cutflow_cfg):
    return [binned_df_cfg, cutflow_cfg, "my_third_stage"]


def test__create_stages(a_stage_list, tmpdir):
    stages = dict_config._create_stages(a_stage_list, tmpdir)
    assert len(stages) == 3
    assert isinstance(stages[0], BinnedDataframe)
    assert isinstance(stages[1], CutFlow)
    assert isinstance(stages[2], BinnedDataframe)


@pytest.fixture
def all_stage_configs():
    bins_alpha = {"in": "AlphaT", "out": "alphaT", "bins": dict(nbins=10, low=0, high=2.5)}
    bins_pt = {"in": "jet_pt", "out": "pt_leadJet", "bins": dict(edges=[0, 20., 100.], overflow=True), "index": 0}
    bins_region = {"in": "REGION", "out": "region"}
    weight_dict = dict(none=1, weighted="weight")
    binned_df_cfg_1 = dict(binning=[bins_pt, bins_region], weights=weight_dict)
    binned_df_cfg_2 = dict(binning=[bins_alpha], weights=None)

    selection_cut_1 = "ev.jet_pt[0] > 0"
    selection_cut_2 = "ev.nJet > 1"
    selection = dict(All=[selection_cut_1, dict(Any=dict(Not=selection_cut_2))])
    cutflow_cfg = dict(selection=selection,
                       aliases=dict(some_alias="ev.something == 1"),
                       counter_weights="an_attribrute")
    return dict(my_first_stage=binned_df_cfg_1, my_second_stage=cutflow_cfg, my_third_stage=binned_df_cfg_2)


def test__configure_stages(a_stage_list, all_stage_configs, tmpdir):
    stages = dict_config._create_stages(a_stage_list, tmpdir)
    dict_config._configure_stages(stages, all_stage_configs)


def test_sequence_from_dict(a_stage_list, all_stage_configs, tmpdir):
    rc_pairs = dict_config.sequence_from_dict(a_stage_list, output_dir=str(tmpdir), **all_stage_configs)
    # 3 stages in list, but one stage makes 2 pairs, so look for 4 rc pairs in total
    assert len(rc_pairs) == 4
