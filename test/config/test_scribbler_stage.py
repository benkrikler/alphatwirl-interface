from __future__ import absolute_import
import pytest
import alphatwirl_interface.config.scribbler_stage as scrs
from . import fake_scribbler_to_test as mod


def test_make_one_scribbler_NoArgs():
    scribbler = scrs._make_one_scribbler("test_make_one_scribbler_NoArgs", mod, "FakeScribbler", args={})
    assert isinstance(scribbler, mod.FakeScribbler)
    assert scribbler.value == "something"

    scribbler = scrs._make_one_scribbler("test_make_one_scribbler_NoArgs", mod, "FakeScribbler", args={}, index=1)
    assert isinstance(scribbler, mod.FakeScribbler)
    assert scribbler.value == "something"


def test_make_one_scribbler_WithArgs():
    args = {"an_int": 1, "a_str": "hi"}
    scribbler = scrs._make_one_scribbler("test_make_one_scribbler_WithArgs", mod,
                                         "FakeScribblerArgs", args=args)
    assert isinstance(scribbler, mod.FakeScribblerArgs)
    assert scribbler.an_int == 1
    assert scribbler.a_str == "hi"

    scribbler = scrs._make_one_scribbler("test_make_one_scribbler_WithArgs", mod,
                                         "FakeScribblerArgs", args=args, index=4)
    assert isinstance(scribbler, mod.FakeScribblerArgs)
    assert scribbler.an_int == 1
    assert scribbler.a_str == "hi"


@pytest.fixture
def config_list_1():
    cfgs = ["FakeScribbler",
            {"FakeScribblerArgs": {"an_int": 4, "a_str": "word"}},
            "FakeScribbler"
            ]
    return cfgs


def test_make_scribblers_list(config_list_1):
    scribblers = scrs._make_scribblers("test_make_scribblers", mod, config_list_1)
    assert len(scribblers) == 3
    assert isinstance(scribblers[0], mod.FakeScribbler)
    assert isinstance(scribblers[1], mod.FakeScribblerArgs)
    assert isinstance(scribblers[2], mod.FakeScribbler)
    assert scribblers[1].an_int == 4
    assert scribblers[1].a_str == "word"


def test_make_scribblers_single():
    cfgs = "FakeScribbler"
    scribblers = scrs._make_scribblers("test_make_scribblers", mod, cfgs)
    assert len(scribblers) == 1
    assert isinstance(scribblers[0], mod.FakeScribbler)


@pytest.fixture
def scribbler_1(tmpdir):
    return scrs.Scribbler("scribbler_1", str(tmpdir))


def test_Scribbler_1(scribbler_1, tmpdir):
    assert scribbler_1.name == "scribbler_1"
    assert scribbler_1.output_dir == str(tmpdir)


@pytest.fixture
def scribbler_1_configured_1(scribbler_1, config_list_1):
    module = "test.config.fake_scribbler_to_test"
    scribbler_1.apply_description(module, config_list_1)
    return scribbler_1


def test_scribbler_1_configured_1(scribbler_1_configured_1):
    rc_pairs = scribbler_1_configured_1.as_rc_pairs()
    assert len(rc_pairs) == 3
    assert isinstance(rc_pairs[0][0], mod.FakeScribbler)
    assert isinstance(rc_pairs[1][0], mod.FakeScribblerArgs)
    assert isinstance(rc_pairs[2][0], mod.FakeScribbler)
    assert rc_pairs[1][0].an_int == 4
    assert rc_pairs[1][0].a_str == "word"
