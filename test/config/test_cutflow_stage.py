import pytest
import alphatwirl_interface.config.cutflow_stage as cfs


@pytest.fixture
def selection_cut_1():
    return "ev.jet_pt[0] > 0"


@pytest.fixture
def selection_cut_2():
    return "ev.nJet > 1"


@pytest.fixture
def selection_cut_alias():
    return "some_alias"


def test__process_single_selection_1(selection_cut_1):
    out_selection = cfs._process_single_selection("test__process_single_selection", 
                                                  selection_cut_1, "ev")
    assert out_selection == "ev: ev.jet_pt[0] > 0"


def test__process_single_selection_alias(selection_cut_alias):
    aliases = dict(some_alias = "ev.something == 1")
    out_selection = cfs._process_single_selection("test__process_single_selection_alias",
                                                  selection_cut_alias, "ev", aliases=aliases)
    assert out_selection == "ev: ev.something == 1"


def test__process_single_selection_raises(selection_cut_alias):
    name = "test__process_single_selection_raises"
    with pytest.raises(cfs.BadCutflowConfig) as ex:
        out_selection = cfs._process_single_selection(name, selection_cut_alias, "ev", aliases={1:"blargwd"})
    assert "Issue pre-processing selection" in str(ex.value)


@pytest.fixture
def selection_dict_1(selection_cut_1):
    return dict(All=[selection_cut_1, False])


def test__prepare_selection_1(selection_dict_1):
    name = "test__prepare_selection_1"
    out = cfs._prepare_selection(name, selection_dict_1, "ev")
    assert len(out) == 1
    assert out["All"][0] == "ev: ev.jet_pt[0] > 0"
    assert out["All"][1] == "False"


@pytest.fixture
def selection_dict_2(selection_cut_1, selection_cut_2):
    return dict(All=[selection_cut_1, dict(Any=[selection_cut_2, True])])


def test__prepare_selection_2(selection_dict_2):
    name = "test__prepare_selection_2"
    out = cfs._prepare_selection(name, selection_dict_2, "ev")
    assert len(out) == 1
    assert out["All"][0] == "ev: ev.jet_pt[0] > 0"
    assert out["All"][1]["Any"][0] == "ev: ev.nJet > 1"
    assert out["All"][1]["Any"][1] == "True"


@pytest.fixture
def selection_dict_3(selection_cut_1, selection_cut_2):
    return dict(All=[selection_cut_1, dict(Any=dict(Not=selection_cut_2))])


def test__prepare_selection_3(selection_dict_3):
    name = "test__prepare_selection_3"
    out = cfs._prepare_selection(name, selection_dict_3, "ev")
    assert len(out) == 1
    assert out["All"][0] == "ev: ev.jet_pt[0] > 0"
    assert out["All"][1]["Any"]["Not"] == "ev: ev.nJet > 1"
    assert len(out["All"][1]) == 1
    assert len(out["All"][1]["Any"]) == 1
    assert isinstance(out["All"][1]["Any"], dict)


def test__prepare_selection_raises(selection_dict_2):
    name = "test__prepare_selection_raises"
    with pytest.raises(cfs.BadCutflowConfig) as ex:
        cfs._prepare_selection(name, selection_dict_2, "ev", aliases=["not_a", "dict"])
    assert "aliases is not a dictionary" in str(ex.value)


@pytest.fixture
def selection_file(tmpdir):
    test_file = tmpdir.join("test_selection_file.yml")
    test_file.write("""selection: {All: [ "ev.one > 1", "ev.beta == 3" ]}""")
    return str(test_file)


@pytest.fixture
def selection_file_alias(tmpdir):
    contents = """selection: {All: [ "ev.one > 1", "ev.beta == 3" ]}\n"""
    contents += """aliases: {"blah": "ev.random_token > ev.another_token"}"""
    test_file = tmpdir.join("test_selection_file_alias.yml")
    test_file.write(contents)
    return str(test_file)


def test__load_selection_file(selection_file):
    name = "test__load_selection_file"
    selection, aliases = cfs._load_selection_file(name, selection_file)
    assert aliases is None
    assert len(selection) == 1
    assert len(selection["All"]) == 2


def test__load_selection_file_aliases(selection_file_alias):
    name = "test__load_selection_file_aliases"
    selection, aliases = cfs._load_selection_file(name, selection_file_alias)
    assert isinstance(aliases, dict)
    assert len(aliases) == 1
    assert len(selection) == 1
    assert len(selection["All"]) == 2


def test__create_weights():
    name = "test__create_weights"
    assert cfs._create_weights(name, weights=None) is None
    assert cfs._create_weights(name, weights="some_attribute") == "some_attribute"
    assert cfs._create_weights(name, weights=["some_attribute"]) == "some_attribute"
    with pytest.raises(cfs.MultipleWeightedSelectionsNotImplemented) as ex:
        cfs._create_weights(name, weights=["some", "attribute"])


@pytest.fixture
def cutflow_1(tmpdir):
    return cfs.CutFlow("cutflow_1", str(tmpdir))


def test_CutFlow(cutflow_1, tmpdir):
    assert cutflow_1.name == "cutflow_1"
    assert cutflow_1.output_dir == str(tmpdir)


def test_apply_description_1(cutflow_1, selection_dict_1):
    config = dict(selection=selection_dict_1, aliases=dict(some_alias="ev.something == 1"),
                counter_weights="an_attribrute")
    cutflow_1.apply_description(**config)
    assert len(cutflow_1.selection) == 1
    assert list(cutflow_1.selection.keys()) == ["All"]
    assert cutflow_1._weights == "an_attribrute"


def test_apply_description_file(cutflow_1, selection_file):
    config = dict(selection_file=selection_file, aliases=dict(some_alias="ev.something == 1"),
                counter_weights="an_attribrute")
    cutflow_1.apply_description(**config)
    assert len(cutflow_1.selection) == 1
    assert list(cutflow_1.selection.keys()) == ["All"]
    assert cutflow_1._weights == "an_attribrute"


def test_apply_description_raises(cutflow_1, selection_file, selection_dict_1):
    config = dict(selection_file=selection_file, selection=selection_dict_1,
                  aliases=dict(some_alias="ev.something == 1"), counter_weights="an_attribrute")
    with pytest.raises(cfs.BadCutflowConfig) as ex:
        cutflow_1.apply_description(**config)
    assert "Both selection and selection_file" in str(ex)

    config = dict(aliases=dict(some_alias="ev.something == 1"), counter_weights="an_attribrute")
    with pytest.raises(cfs.BadCutflowConfig) as ex:
        cutflow_1.apply_description(**config)
    assert "Neither selection nor selection_file" in str(ex)


#def test_as_rc_pairs(self):
#def test__create_rc_pairs(self):
