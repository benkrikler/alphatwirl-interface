from alphatwirl_interface.completions import complete, to_null_collector_pairs


class BasicProducer(object):
    '''
        A basic producer implementing the bare-bone for all derived classes.
    '''

    def __init__(self, outputName):
        self.outputName = outputName
        self.value = []

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def _format_attributes(self, attributes):
        values = [getattr(self, attr) for attr in attributes]
        template = '{} = {!r}'
        formattedStrings = []
        for attr, value in zip(attributes, values):
            formattedString = template.format(attr, value)
            formattedStrings.append(formattedString)

        return ', '.join(formattedStrings)

    def _attach_to_obj(self, obj):
        setattr(obj, self.outputName, self.value)

    def _value(self, obj):
        return [42]

    def begin(self, obj):
        self.value = []
        self._attach_to_obj(obj)

    def event(self, obj):
        self._attach_to_obj(obj)
        self.value[:] = self._value(obj)

    def module(self):
        return to_null_collector_pairs([self])[0]
