import pytest


@pytest.fixture
def example_event():
    class Event(object):
        def __init__(self, Muon_E, Muon_Px, Muon_Py, Muon_Pz):
            self.Muon_E = Muon_E
            self.Muon_Px = Muon_Px
            self.Muon_Py = Muon_Py
            self.Muon_Pz = Muon_Pz

    event = Event(
        Muon_E=[50, 60],
        Muon_Px=[10, 10],
        Muon_Py=[20, 30],
        Muon_Pz=[20, 20],
    )
    return event
