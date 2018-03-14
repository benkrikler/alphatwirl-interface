import pytest

from alphatwirl_interface import Selection
from alphatwirl.selection.modules import AllwCount
from alphatwirl.loop import Collector, NullCollector
from alphatwirl.collector import WriteListToFile


@pytest.fixture
def example_selection():
    selection = Selection(
        dict(
            All=(
                'di_muon_mass[0] > 60',
                'di_muon_mass[0] < 120',
            )
        )
    )
    return selection


@pytest.fixture
def example_selection_with_cutflow_file():
    selection = Selection(
        dict(
            All=(
                'di_muon_mass[0] > 60',
                'di_muon_mass[0] < 120',
            )
        ),
        cutflow_file='/tmp/test.txt',
    )
    return selection


def test_cutflow_file(example_selection_with_cutflow_file):
    s = example_selection_with_cutflow_file
    # s_tuple = s.as_tuple()
    assert len(s) == 2
    assert isinstance(s[0], AllwCount)
    assert isinstance(s[1], Collector)
    assert isinstance(s[1].deliveryMethod, WriteListToFile)


def test_no_cutflow_file(example_selection):
    s = example_selection
    assert len(s) == 2
    assert isinstance(s[0], AllwCount)
    assert isinstance(s[1], NullCollector)


def test_empty_selection():
    with pytest.raises(ValueError) as ex:
        Selection({})
    assert 'cannot recognize the path_cfg' in str(ex.value)
