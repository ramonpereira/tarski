"""
 This tests the type-handling module
"""
import pytest
import tarski
import tarski.model
from tarski.model import Model
from tarski import errors

from ..common import blocksworld, numeric
from tarski.evaluators.simple import evaluate
from tarski.syntax import Constant


def test_interpretation_instance():
    lang = numeric.generate_numeric_instance()
    tarski.model.create(lang)


def test_numeric_function_set():
    lang = numeric.generate_numeric_instance()
    lang.get_sort('particle')
    p1 = lang.get_constant('p1')
    x = lang.get_function('x')
    model = tarski.model.create(lang)
    model.set(x, p1, 1.0)


def test_numeric_builtin_addition():
    lang = numeric.generate_numeric_instance()
    p1 = lang.get_constant('p1')
    x = lang.get_function('x')
    model = tarski.model.create(lang)
    model.evaluator = evaluate
    model.set(x, p1, 1.0)

    expr = model[x(p1) + 1.0]

    assert isinstance(expr, Constant)
    assert expr.symbol == 2.0


def test_numeric_rel_formula_evaluation():
    lang = numeric.generate_numeric_instance()
    p1 = lang.get_constant('p1')
    p2 = lang.get_constant('p2')
    x = lang.get_function('x')
    model = tarski.model.create(lang)
    model.evaluator = evaluate
    model.set(x, p1, 1.0)
    model.set(x, p2, 2.0)

    assert model[x(p1) < x(p2)]


def test_blocksworld_set():
    lang = blocksworld.generate_small_fstrips_bw_language()
    model = Model(lang)
    loc = lang.get_function('loc')
    b1, table = (lang.get_constant(s) for s in ('b1', 'table'))
    model.set(loc, b1, table)

    assert evaluate(loc(b1), model) == table


def test_blocksworld_set_via_square_brackets():
    lang = blocksworld.generate_small_fstrips_bw_language()
    model = Model(lang)
    model.evaluator = evaluate
    loc = lang.get_function('loc')
    b1, table = (lang.get_constant(s) for s in ('b1', 'table'))
    model.set(loc, b1, table)

    assert model[loc(b1)] == table


def test_blocksworld_add():
    lang = blocksworld.generate_small_fstrips_bw_language()
    model = Model(lang)
    clear = lang.get_predicate('clear')
    b1 = lang.get_constant('b1')
    model.add(clear, b1)
    assert evaluate(clear(b1), model) is True


def test_blocksworld_add_and_remove():
    lang = blocksworld.generate_small_fstrips_bw_language()
    model = Model(lang)

    clear = lang.get_predicate('clear')
    b1 = lang.get_constant('b1')

    model.add(clear, b1)
    model.remove(clear, b1)
    assert evaluate(clear(b1), model) is False


def test_zero_ary_predicate_set():
    L = tarski.language()

    P = L.predicate('P')

    M = Model(L)
    M.add(P)

    assert evaluate(P(), M) is True


def test_predicate_extensions():
    lang = tarski.language()
    pred = lang.predicate('pred', lang.Object, lang.Object)

    o1 = lang.constant("o1", lang.Object)
    o2 = lang.constant("o2", lang.Object)

    model = Model(lang)

    with pytest.raises(errors.ArityMismatch):
        # This should raise an error, as the predicate is binary
        model.add(pred)

    with pytest.raises(ValueError):
        # This should raise an error, as the predicate sort does not coincide with the sort of the parameters
        model.add(pred, 1, 2)

    model.add(pred, o1, o2)
    assert not model.holds(pred, (o2, o1))  # Make sure the order in which the elements were added is respected!
    assert model.holds(pred, (o1, o2))

    with pytest.raises(KeyError):
        # This should raise an error, as the tuple does not belong to the predicate's extension
        model.remove(pred, o2, o1)

    model.remove(pred, o1, o2)
    with pytest.raises(KeyError):
        # This should raise an error, as the tuple has been removed
        model.remove(pred, o1, o2)




