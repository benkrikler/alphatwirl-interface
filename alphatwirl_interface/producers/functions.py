import numpy as np

from .basic import BasicProducer


class NewFromFunction(BasicProducer):
    '''
        Generic producer to calculate inputs from functions.
        The passed function needs to return a sequence.
        Can either be used directly, e.g.

          met_ht_ratio = NewFromFunction(
            'met_ht_ratio',
            inputs=['MET', 'HT'],
            function=np.divide,
          )

        or to implement specialisations as classes, see
         - alphatwirl_interface.functions.Divide
         - alphatwirl_interface.functions.TransverseMomentum
    '''

    def __init__(self, outputName, inputs, function):
        super(NewFromFunction, self).__init__(outputName)
        self.inputs = inputs
        self.function = function

    def _value(self, obj):
        return self.function(
            *[np.array(getattr(obj, n)) for n in self.inputs]
        )

    def __repr__(self):
        attributes = ['outputName', 'inputs', 'function']
        formattedAttrs = super(
            NewFromFunction, self)._format_attributes(attributes)

        return '{}({})'.format(
            self.__class__.__name__,
            formattedAttrs,
        )


class Divide(NewFromFunction):
    '''
        Divides two inputs by each other (can be vectors)
    '''

    def __init__(self, outputName, inputs):
        super(self.__class__, self).__init__(outputName, inputs, np.divide)


class TransverseMomentum(NewFromFunction):
    '''
        Calculates the transverse momentum of particles given their
        momenta in the x- and y-plane, e.g.

          muon_pt = TransverseMomentum(
            outputName='muon_pt',
            inputs=['Muon_Px', 'Muon_Py'],
          )

    '''

    def __init__(self, outputName, inputs):
        super(self.__class__, self).__init__(
            outputName,
            inputs,
            function=lambda x, y: np.sqrt(np.square(x) + np.square(y))
        )
