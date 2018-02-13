# -*- coding: utf-8 -*-
from collections import defaultdict

from . import errors as err
from .terms import Constant
from .function import Function
from .predicate import Predicate


def _check_assignment(fun, point, value=None):
    assert isinstance(point, tuple)
    elements = point + (value,) if value is not None else point
    processed = []

    typ = fun.type
    if len(typ) != len(elements):
        raise err.ArityMismatch(fun, elements)

    language = fun.language
    for element, expected_type in zip(elements, typ):

        if not isinstance(element, Constant):
            # Assume a literal value has been passed instead of its corresponding constant
            element = Constant(expected_type.cast(element), expected_type)
            # raise err.IncorrectExtensionDefinition(fun, point, value)

        if element.language != language:
            raise err.LanguageMismatch(element, element.language, language)

        if not language.is_subtype(element.sort, expected_type):
            raise err.TypeMismatch(element, element.sort, expected_type)

        processed.append(element)

    return tuple(processed) if value is None else tuple(processed[:-1]), processed[-1]


class Model(object):
    """
        A First Order Language Model
    """

    def __init__(self, language):
        self.language = language
        self.function_extensions = defaultdict(dict)
        self.predicate_extensions = defaultdict(set)

    def set(self, fun: Function, point, value):
        """ Set the value of function 'fun' at point 'point' to be equal to 'value'
            'point' needs to be a tuple of constants, and value a single constant.
        """
        point, value = _check_assignment(fun, point, value)

        self.function_extensions[fun.signature][point] = value

    def add(self, predicate: Predicate, *args):
        _check_assignment(predicate, args)

        entry = frozenset(a.symbol for a in args)
        self.predicate_extensions[predicate.signature].add(entry)

    def remove(self, predicate: Predicate, *args):
        entry = frozenset(a.symbol for a in args)

        # try:
        #
        # except TypeError:
        #     if point is None:
        #         entry = frozenset()
        #     elif isinstance(point, Constant):
        #         entry = frozenset([point.symbol])
        #     else :
        #         raise err.LanguageError('Model.remove() : arguments of tuple to add for predicate needs to be a tuple of constants or a constant')
        self.predicate_extensions[predicate.signature].remove(entry)

    def value(self, fun: Function, point):
        """ Return the value of the given function on the given point in the current model """
        # print("[f({})]^s = {}".format(symbols, self.function_extensions[t.symbol.signature][symbols]))
        return self.function_extensions[fun.signature][point]

    def holds(self, predicate: Predicate, point):
        """ Return true iff the given predicate is true on the given point in the current model """

        symbols = frozenset(tuple(c.symbol for c in point))
        return symbols in self.predicate_extensions[predicate.signature]

