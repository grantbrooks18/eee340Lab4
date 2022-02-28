"""
Test cases for Nimble semantic analysis. See also the `testhelpers`
module.

Group members: TODO: your names

Date: TODO: completion date

"""

import unittest

from errorlog import Category
from symboltable import PrimitiveType, FunctionType, Scope
from testhelpers import do_semantic_analysis


class TypeAndStatementTests(unittest.TestCase):
    """
    Tests type inference for expressions, and constraint compliance for statements,
    other than function calls and return statements, which are handled by FunctionTests
    and ReturnTests, below.

    You should be able to re-use your tests from lab 3 here, adjusting for the new signature
    of `do_semantic_analysis`. All tests should succeed, except those using variables.
    """
    pass


class ScopeCreationTests(unittest.TestCase):
    """
    Tests that scopes are being correctly created and attached to the parse tree,
    with the correct enclosing relations and scope `return_type` attributes.

    Two example tests provided.
    """

    # def test_script_defines_global_scope(self):
    #     log, global_scope, inferred_types = do_semantic_analysis(
    #         '', 'script')  # , first_phase_only=True)
    #     self.assertIsNotNone(global_scope)
    #     self.assertIsInstance(global_scope, Scope)
    #     self.assertEqual('$global', global_scope.name)
    #     self.assertEqual(0, log.total_entries())
    #
    # def test_main_defines_scope(self):
    #     log, global_scope, inferred_types = do_semantic_analysis(
    #         '', 'script')  # , first_phase_only=True)
    #     self.assertEqual(1, len(global_scope.child_scopes))
    #     self.assertIsNotNone(global_scope.child_scope_named('$main'))
    #     main_scopes = global_scope.all_child_scopes_named('$main')
    #     self.assertEqual(1, len(main_scopes))
    #     self.assertIsInstance(main_scopes[0], Scope)



class FunctionSymbols(unittest.TestCase):
    """
    Tests that functions define appropriate symbols in the global scope and that
    duplicates are appropriately reported.
    """
    pass


class ParameterAndVariableSymbols(unittest.TestCase):
    """
    Tests that parameters and variables define appropriate symbols in
    appropriate scopes, and that duplicates are appropriately reported.
    """
    pass


class FunctionTests(unittest.TestCase):
    """
    Tests functions used as variables, successful function calls, and failed
    function calls.
    """
    pass


class ReturnTests(unittest.TestCase):
    """
    Tests valid and invalid return statements, in both functions and the main.
    """
    pass
