import pytest
import alphatwirl_interface.config.binned_df_stage as bdfs
from alphatwirl.binning import Binning, Echo
from alphatwirl.summary import Reader
from alphatwirl.loop import Collector


@pytest.fixture
def bins_alphaT():
    return {"in": "AlphaT", "out": "alphaT", "bins": dict(nbins=10, low=0, high=2.5)}


@pytest.fixture
def bins_pt():
    return {"in": "jet_pt", "out": "pt_leadJet", "bins": dict(edges=[0, 20., 100.], overflow=True), "index": 0}


@pytest.fixture
def bins_region():
    return {"in": "REGION", "out": "region"}


@pytest.fixture
def weight_list():
    return [1, "weight"]


@pytest.fixture
def weight_dict():
    return dict(none=1, weighted="weight")

def test__create_one_region(bins_region):
    cfg = {"_" + k: v for k, v in bins_region.items()}
    _in, _out, _bins, _index = bdfs._create_one_dimension("test__create_one_region", **cfg)
    assert _in == "REGION"
    assert _out == "region"
    assert _index == None
    assert isinstance(_bins, Echo)


def test__create_one_dimension_aT(bins_alphaT):
    cfg = {"_" + k: v for k, v in bins_alphaT.items()}
    _in, _out, _bins, _index = bdfs._create_one_dimension("test__create_one_dimension_aT", **cfg)
    assert _in == "AlphaT"
    assert _out == "alphaT"
    assert _index == None
    assert isinstance(_bins, Binning)
    assert _bins.boundaries == tuple([i/20. for i in range(0, 51, 5)])
    assert _bins.underflow_bin == float("-inf")
    assert _bins.overflow_bin == 2.5


def test__create_one_dimension_HT(bins_pt):
    cfg = {"_" + k: v for k, v in bins_pt.items()}
    _in, _out, _bins, _index = bdfs._create_one_dimension("test__create_one_dimension_HT", **cfg)
    assert _in == "jet_pt"
    assert _out == "pt_leadJet"
    assert _index == 0
    assert isinstance(_bins, Binning)
    assert _bins.boundaries == (0, 20., 100.)
    assert _bins.underflow_bin == float("-inf")
    assert _bins.overflow_bin == 100.


def test__create_binning_list(bins_region, bins_alphaT):
    binning = bdfs._create_binning_list("test__create_binning_list", [bins_region, bins_alphaT])
    assert len(binning) == 2


def test__create_weights(weight_list):
    weights = bdfs._create_weights(weight_list)
    weight_keys = list(weights.keys())
    weight_values = list(weights.values())
    assert len(weights) == 2
    assert weight_keys[weight_values.index(1)] == "1"
    assert weight_keys[weight_values.index("weight")] == "weight"


def test__create_weights(weight_dict):
    weights = bdfs._create_weights(weight_dict)
    weight_keys = list(weights.keys())
    weight_values = list(weights.values())
    assert len(weights) == 2
    assert weight_keys[weight_values.index(1)] == "none"
    assert weight_keys[weight_values.index("weight")] == "weighted"


@pytest.fixture
def config_1(bins_alphaT, bins_pt, weight_list):
    return dict(binning=[bins_alphaT, bins_pt], weights=weight_list)


@pytest.fixture
def config_2(bins_alphaT, bins_pt, bins_region, weight_dict):
    return dict(binning=[bins_pt, bins_alphaT, bins_region], weights=weight_dict)


@pytest.fixture
def binned_df_1(tmpdir):
    return bdfs.BinnedDataframe("binned_df_1", str(tmpdir))


def test_BinnedDataframe(binned_df_1, tmpdir):
    assert binned_df_1.name == "binned_df_1"
    assert binned_df_1.output_dir == str(tmpdir)


def test_BinnedDataframe_apply_description_1(binned_df_1, config_1):
    binned_df_1.apply_description(**config_1)
    assert len(binned_df_1._binning) == 2
    assert len(binned_df_1._binning[0]) == 4
    assert len(binned_df_1._weights) == 2


def test_BinnedDataframe_apply_description_2(binned_df_1, config_2):
    binned_df_1.apply_description(**config_2)
    assert len(binned_df_1._binning) == 3
    assert len(binned_df_1._binning[0]) == 4
    assert len(binned_df_1._weights) == 2


def test_BinnedDataframe_as_rc_pairs(binned_df_1, config_1):
    binned_df_1.apply_description(**config_1)
    rc_pairs = binned_df_1.as_rc_pairs()
    assert len(rc_pairs) == len(config_1["weights"])
    assert all(map(lambda x: isinstance(x[0], Reader), rc_pairs))
