"""
Group members: TODO: your names

Date: TODO: completion date

TODO: read this description, implement to make it true.

The nimblesemantics module contains classes sufficient to perform a semantic analysis
of Nimble programs.

The analysis has two major tasks:

- to infer the types of all expressions in a Nimble program and to add appropriate type
annotations to the program's ANTLR-generated syntax tree by monkey-patching a `type`
attribute (a `symboltable.PrimitiveType`) onto each expression node; and

- to identify and flag all violations of the Nimble semantic specification
using the errorlog module.

There are two phases to the analysis:

1. DefineScopesAndSymbols, and

2. InferTypesAndCheckSemantics.

In the first phase, `symboltable.Scope` objects are created for all scope-defining parse
tree nodes: the script, each function definition, and the main. These are monkey-patched
onto the tree nodes as `scope` attributes. Also in this phase, all declared function,
parameter, and variable types are recorded in the appropriate scope. Restrictions on
duplicate definitions are enforced.

In the second phase, type inference is performed and all other semantic constraints are
checked.
"""

from errorlog import ErrorLog, Category
from nimble.NimbleListener import NimbleListener
from nimble.NimbleParser import NimbleParser
from symboltable import Scope, FunctionType, PrimitiveType


class DefineScopesAndSymbols(NimbleListener):

    def __init__(self, error_log: ErrorLog):
        self.error_log = error_log
        self.current_scope = None


class InferTypesAndCheckConstraints(NimbleListener):

    def __init__(self, error_log: ErrorLog):
        self.error_log = error_log
        self.current_scope = None
