# -*- coding: utf-8 -*-

"""
    Creates a TaskIndex for a  planning task as given by Tarski's AST.
"""
from collections import OrderedDict
import itertools

from tarski import util
from .visitors import FluentSymbolCollector, FluentHeuristic

class TaskIndex(object):
    def __init__(self, domain_name, instance_name):
        self.domain_name = domain_name
        self.instance_name = instance_name
        self.all_symbols = util.UninitializedAttribute('all_symbols')
        self.static_symbols = util.UninitializedAttribute('static_symbols')
        self.fluent_symbols = util.UninitializedAttribute('fluent_symbols')
        self.initial_fluent_atoms = util.UninitializedAttribute('initial_fluent_atoms')
        self.initial_static_data = util.UninitializedAttribute('initial_static_data')
        self.state_variables = util.UninitializedAttribute('state_variables')

    def _check_static_not_fluents(self):
        """
            Sorts fluent and static sets, so that the only
            static expressions are those which haven't found
            under the scope of a X operator at least once.
        """
        #print('Fluents (before filtering): {}'.format(','.join([str(var) for var in self.fluent_symbols])))
        #print('Statics (before filtering): {}'.format(','.join([str(var) for var in self.static_symbols])))
        self.static_symbols = set([ x for x in self.static_symbols if x not in self.fluent_symbols])
        assert all([x not in self.static_symbols for x in self.fluent_symbols])
        #print('Fluents (after filtering): {}'.format(','.join([str(var) for var in self.fluent_symbols])))
        #print('Statics (after filtering): {}'.format(','.join([str(var) for var in self.static_symbols])))

    def process_symbols(self, P):

        self.fluent_symbols = set()
        self.static_symbols = set()

        prec_visitor = FluentSymbolCollector(P.language,self.fluent_symbols,self.static_symbols,FluentHeuristic.precondition)
        eff_visitor = FluentSymbolCollector(P.language,self.fluent_symbols,self.static_symbols,FluentHeuristic.action_effects)
        constraint_visitor = FluentSymbolCollector(P.language, self.fluent_symbols,self.static_symbols,FluentHeuristic.constraint)

        oF = len(self.fluent_symbols)
        oS = len(self.static_symbols)
        while True :
            for _, act in P.actions.items() :
                act.precondition.accept(prec_visitor)
                for eff in act.effects :

                    eff.accept(eff_visitor)
            for const in P.constraints :
                constraint_visitor.reset()
                const.accept(constraint_visitor)

            self._check_static_not_fluents()
            if len(self.fluent_symbols) == oF and\
                 len(self.static_symbols) == oS:
                 break
            oF = len(self.fluent_symbols)
            oS = len(self.static_symbols)

        self.all_symbols = self.fluent_symbols | self.static_symbols


    def is_fluent(self, symbol):
        return symbol_name in self.fluent_symbols

    def process_initial_state(self, I):
        raise NotImplementedError()