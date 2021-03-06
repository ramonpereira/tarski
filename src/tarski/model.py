# -*- coding: utf-8 -*-
from collections import defaultdict

from . import errors as err
from .syntax import Function, Constant
from .syntax.predicate import Predicate


def _check_assignment(fun, point, value=None):
    assert isinstance(point, tuple)

    elements = point + (value,) if value is not None else point
    processed = []

    typ = fun.sort

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
            raise err.SortMismatch(element, element.sort, expected_type)

        processed.append(element)

    if value is None:
        return tuple(processed)

    assert len(processed) > 0
    return tuple(processed[:-1]), processed[-1]


class Model:
    """ A First Order Language Model """

    def __init__(self, language):
        self.evaluator = None
        self.language = language
        self.function_extensions = dict()
        self.predicate_extensions = defaultdict(set)

    def set(self, fun, *args):
        """ Set the value of function 'fun' at point 'point' to be equal to 'value'
            'point' needs to be a tuple of constants, and value a single constant.
        """
        if not isinstance(fun, Function):
            raise err.SemanticError("Model.set() can only set the value of functions")
        point, value = args[:-1], args[-1]
        point, value = _check_assignment(fun, point, value)
        if fun.signature not in self.function_extensions:
            definition = self.function_extensions[fun.signature] = ExtensionalFunctionDefinition()
        else:
            definition = self.function_extensions[fun.signature]
            if not isinstance(definition, ExtensionalFunctionDefinition):
                raise err.SemanticError("Cannot define extension of intensional definition")

        definition.set(point, value)

    def add(self, predicate: Predicate, *args):
        if not isinstance(predicate, Predicate):
            raise err.SemanticError("Model.add() can only set the value of predicates")
        point = _check_assignment(predicate, args)
        # point = tuple(a.symbol for a in point)
        self.predicate_extensions[predicate.signature].add(point)

    def remove(self, predicate: Predicate, *args):
        # point = tuple(a.symbol for a in args)
        point = args

        # try:
        #
        # except TypeError:
        #     if point is None:
        #         entry = frozenset()
        #     elif isinstance(point, Constant):
        #         entry = frozenset([point.symbol])
        #     else :
        #         raise err.LanguageError('Model.remove() : arguments of tuple to add for predicate
        #  needs to be a tuple of constants or a constant')
        self.predicate_extensions[predicate.signature].remove(point)

    def value(self, fun: Function, point):
        """ Return the value of the given function on the given point in the current model """
        definition = self.function_extensions[fun.signature]
        return definition.get(point)

    def holds(self, predicate: Predicate, point):
        """ Return true iff the given predicate is true on the given point in the current model """
        # return tuple(c.symbol for c in point) in self.predicate_extensions[predicate.signature]
        return point in self.predicate_extensions[predicate.signature]

    def __getitem__(self, arg):
        try:
            expr, sigma = arg
            return self.evaluator(expr, self, sigma)
        except TypeError:
            return self.evaluator(arg, self)


def create(lang):
    return Model(lang)


class ExtensionalFunctionDefinition:
    def __init__(self):
        self.data = dict()

    def set(self, point, value):
        assert isinstance(point, tuple)
        assert isinstance(value, Constant)
        self.data[point] = value

    def get(self, point):
        return self.data[point]


# class IntensionalFunctionDefinition:
#     pass
