import pytest
import alphatwirl_interface.config.cutflow_stage as cfs


@pytest.fixture
def selection_cut_1():
    return "ev.jet_pt[0] > 0"

@pytest.fixture
def selection_cut_2():
    return "ev.nJet > 1"


@pytest.fixture
def selection_dict_1(selection_cut_1):
    return dict(All=[selection_cut_1, False])


@pytest.fixture
def selection_dict_2(selection_cut_1, selection_cut_2):
    return dict(All=[selection_cut_1, dict(Any=[selection_cut_2, True])])


@pytest.fixture
def selection_dict_3(selection_cut_1, selection_cut_2):
    return dict(All=[selection_cut_1, dict(Any=dict(Not=selection_cut_2))])


#def test_apply_description(self, selection_file=None, selection=None, aliases=None,
#def test_as_rc_pairs(self):
#def test__create_rc_pairs(self):
#def test__load_selection_file(selection_file):
#def test__prepare_selection(stage_name, selection, lambda_arg="ev", aliases=None):
#def test__recurse_selection(stage_name, selection, lambda_arg="ev", aliases=None):
#def test__process_single_selection(stage_name, selection, lambda_arg="ev", aliases=None):
#def test__create_weights(stage_name, weights):
