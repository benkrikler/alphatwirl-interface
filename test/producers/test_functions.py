import pytest
import numpy as np
from alphatwirl_interface.producers import TransverseMomentum, Divide, NewFromFunction

from .fixtures import example_event


@pytest.mark.usefixtures("example_event")
def test_new_from_function(example_event):
    e = example_event
    new_attr = 'sin'
    p = NewFromFunction(
        new_attr,
        inputs=['Muon_Px'],
        function=np.sin,
    )
    # would usually be called in alphatwirl
    p.begin(e)
    p.event(e)
    # manual calculation
    expected = np.sin(e.Muon_Px)
    assert hasattr(example_event, new_attr)
    for ratio, exp_ratio in zip(getattr(e, new_attr), expected):
        assert ratio == exp_ratio


@pytest.mark.usefixtures("example_event")
def test_divide(example_event):
    e = example_event
    new_attr = 'px_py_ratio'
    p = Divide(
        new_attr,
        inputs=['Muon_Px', 'Muon_Py'],
    )
    # would usually be called in alphatwirl
    p.begin(e)
    p.event(e)
    # manual calculation
    expected = np.divide(e.Muon_Px, e.Muon_Py)
    # test
    assert hasattr(example_event, new_attr)
    for ratio, exp_ratio in zip(getattr(e, new_attr), expected):
        assert ratio == exp_ratio


@pytest.mark.usefixtures("example_event")
def test_transverse_momentum(example_event):
    e = example_event
    new_attr = 'muon_pt'
    p = TransverseMomentum(
        new_attr,
        inputs=['Muon_Px', 'Muon_Py'],
    )
    # would usually be called in alphatwirl
    p.begin(e)
    p.event(e)
    # manual calculation
    expected = np.sqrt(np.square(e.Muon_Px) + np.square(e.Muon_Py))
    # test
    assert hasattr(example_event, new_attr)
    for mu_pt, exp_pt in zip(getattr(e, new_attr), expected):
        assert mu_pt == exp_pt
