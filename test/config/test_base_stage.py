import pytest
import alphatwirl_interface.config.base_stage as base_stage


@pytest.fixture
def base_1():
    return base_stage.BaseStage("base_1", "some/out/directory")


def test_BaseStage(base_1):
    assert base_1.name == "base_1"
    assert base_1.output_dir == "some/out/directory"
    with pytest.raises(AttributeError) as ex:
        base_1.name = "hello"
    assert "can't set attribute" in str(ex)

    with pytest.raises(AttributeError) as ex:
        base_1.output_dir = "hello"
    assert "can't set attribute" in str(ex)


def test_apply_description_raises(base_1):
    some_cfg = dict(selection="junk", something_else=True)
    with pytest.raises(NotImplementedError):
        base_1.apply_description(**some_cfg)


def test_as_rc_pairs_raises(base_1):
    with pytest.raises(NotImplementedError):
        base_1.as_rc_pairs()
