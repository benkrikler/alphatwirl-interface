import operator
from functools import reduce


class WeightCalculatorProduct(object):
    """
    return the product of multiple weights
    """

    def __init__(self, weight_list):
        self.weight_list = weight_list

    def __repr__(self):
        name_value_pairs = (
            ('weight_list', self.weight_list),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, event):
        weights = [getattr(event, attr)[0] for attr in self.weight_list]
        return reduce(operator.mul, weights, 1)


class WeightCalculatorSingleAttr(object):
    """
    return the a single event attribute as a weight
    """

    def __init__(self, attr, index=0):
        self.weight_attr = attr
        self.index = index

    def __repr__(self):
        name_value_pairs = (
            ('weight_attr', self.weight_attr),
            ('index', self.index),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, event):
        return getattr(event, self.weight_attr)[self.index]


class WeightCalculatorConst(object):
    """
    return a constant value as a weight
    """

    def __init__(self, weight):
        self.weight = weight

    def __repr__(self):
        name_value_pairs = (
            ('weight', self.weight),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, event):
        return self.weight
