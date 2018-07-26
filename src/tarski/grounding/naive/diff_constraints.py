# -*- coding: utf-8 -*-
import itertools
import copy

import tarski.fstrips as fs
import tarski.fstrips.hybrid as hybrid
from tarski.syntax.transform import TermSubstitution
from tarski.syntax.visitors import CollectVariables
from tarski.util import IndexDictionary
from . import instantiation
from .elements import process_expression

class DifferentialConstraintGrounder(object):

    def __init__(self, prob, index):
        self.problem = prob
        self.L = self.problem.language
        self.index = index
        self.problem.ground_differential_constraints = IndexDictionary()
        self.schemas = list(self.problem.differential_constraints.values())
        self.differential_constraints_generated = 0

    def __str__(self):
        return 'Reactions generated: {}'.format(self.differential_constraints_generated)

    def calculate_constraints(self):

        for ode_schema in self.schemas:
            k, syms, substs = instantiation.enumerate_groundings(self.L, ode_schema.parameters)
            for values in itertools.product(*substs):
                subst = {syms[k]: v for k, v in enumerate(values)}
                op = TermSubstitution(self.L, subst)
                g_cond = process_expression(self.L, ode_schema.condition, op)
                g_variate = process_expression(self.L, ode_schema.variate, op)
                g_ode = process_expression(self.L, ode_schema.ode, op)

                self.problem.ground_differential_constraints.add(\
                    hybrid.DifferentialConstraint(self.L, ode_schema.name, [], \
                    g_cond, g_variate, g_ode))
            self.differential_constraints_generated += k