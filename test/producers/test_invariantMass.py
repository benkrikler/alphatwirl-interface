import pytest
import numpy as np
from alphatwirl_interface.producers.invariantMass import _extract_index, _extract_values
from alphatwirl_interface.producers import InvariantMass
from .fixtures import example_event


@pytest.mark.parametrize("test_input,expected_name,expected_index", [
    ('Muon[0]', 'Muon', 0),
    ('Muon[4]', 'Muon', 4),
    ('Muon[23]', 'Muon', 23),
    ('Muon[999]', 'Muon', 999),
    ('Muon_1', 'Muon_1', None),
])
def test_extract_index(test_input, expected_name, expected_index):
    name, index = _extract_index(test_input)
    assert name == expected_name
    assert index == expected_index


@pytest.mark.usefixtures("example_event")
def test_extract_values(example_event):
    namesAndIndices = [('Muon_E', 1), ('Muon_Pz', 0)]
    values = list(_extract_values(example_event, namesAndIndices))
    assert values[0] == example_event.Muon_E[1]
    assert values[1] == example_event.Muon_Pz[0]


@pytest.mark.usefixtures("example_event")
def test_invariant_mass(example_event):
    e = example_event
    di_muon_mass = InvariantMass(
        'di_muon_mass',
        ['Muon_E[0]', 'Muon_Px[0]', 'Muon_Py[0]', 'Muon_Pz[0]'],
        ['Muon_E[1]', 'Muon_Px[1]', 'Muon_Py[1]', 'Muon_Pz[1]'],
    )
    # would usually be called in alphatwirl
    di_muon_mass.begin(example_event)
    di_muon_mass.event(example_event)
    # manual calculation
    v0 = [e.Muon_E[0], e.Muon_Px[0], e.Muon_Py[0], e.Muon_Pz[0]]
    v1 = [e.Muon_E[1], e.Muon_Px[1], e.Muon_Py[1], e.Muon_Pz[1]]
    v = np.add(v0, v1)
    energySquared = pow(v[0], 2)
    momentumSquared = np.dot(v[1:], v[1:])
    expected_mass = np.sqrt(energySquared - momentumSquared)
    # test
    assert hasattr(e, 'di_muon_mass')
    assert getattr(e, 'di_muon_mass') == expected_mass
