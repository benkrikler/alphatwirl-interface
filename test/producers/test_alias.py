# from alphatwirl_interface.producers import Alias
#
# def test_integer_attr_alias():
#     originalName = 'original'
#     newName = 'newName'
#     event = object()
#     event.original = 5
#     alias = Alias(newName, originalName)
#
#     alias.begin(event)
#     assert hasattr(event, newName)
#     assert getattr(event, newName) == getattr(event, originalName)
