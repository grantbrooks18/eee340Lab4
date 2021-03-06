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

VALID_EXPRESSIONS = [
    # Each entry is a pair: (expression source, expected type)
    # Due to the way the inferred_types are stored, using ctx.getText() as the key,
    # expressions must contain NO WHITE SPACE for the tests to work. E.g.,
    # '59+a' is fine, '59 + a' won't work.
    ('37', PrimitiveType.Int),
    ('-37', PrimitiveType.Int),

    ('true', PrimitiveType.Bool),
    ('false', PrimitiveType.Bool),

    ('!false', PrimitiveType.Bool),
    ('true', PrimitiveType.Bool),
    ('!true', PrimitiveType.Bool),

    ('(37)', PrimitiveType.Int),
    ('(-37)', PrimitiveType.Int),
    ('(true)', PrimitiveType.Bool),
    ('(!false)', PrimitiveType.Bool),

    ('"abcdef"', PrimitiveType.String),
    ('"Hel  l O  !"', PrimitiveType.String),
    ('"Hel  \\a\\nl"', PrimitiveType.String),

    ('1<2', PrimitiveType.Bool),
    ('(1==2)', PrimitiveType.Bool),
    ('(1==-2)', PrimitiveType.Bool),

    ('1+2', PrimitiveType.Int),
    ('(1--2)', PrimitiveType.Int),
    ('"HELLO"+"WORLD"', PrimitiveType.String),

    ('1*3', PrimitiveType.Int),
    ('(1/2*4)', PrimitiveType.Int),
    ('((1*2)/4*-2)', PrimitiveType.Int),

]

INVALID_EXPRESSIONS = [
    # Each entry is a pair: (expression source, expected error category)
    # As for VALID_EXPRESSIONS, there should be NO WHITE SPACE in the expressions.
    ('!37', Category.INVALID_NEGATION),
    ('!!37', Category.INVALID_NEGATION),

    ('-true', Category.INVALID_NEGATION),
    ('-false', Category.INVALID_NEGATION),

    ('true<3', Category.INVALID_BINARY_OP),
    ('true<!false', Category.INVALID_BINARY_OP),
    ('!true==false', Category.INVALID_BINARY_OP),

    ('"HELLO"-"WORLD"', Category.INVALID_BINARY_OP),
    ('true+false', Category.INVALID_BINARY_OP),
    ('true-4', Category.INVALID_BINARY_OP),
    ('"abc"+false', Category.INVALID_BINARY_OP),

    ('"HELLO"-"WORLD"', Category.INVALID_BINARY_OP),
    ('true+false', Category.INVALID_BINARY_OP),
    ('true-4', Category.INVALID_BINARY_OP),
    ('"abc"+false', Category.INVALID_BINARY_OP),

    ('"HELLO"/"WORLD"', Category.INVALID_BINARY_OP),
    ('true*false', Category.INVALID_BINARY_OP),
    ('true*4', Category.INVALID_BINARY_OP),
    ('"abc"/false', Category.INVALID_BINARY_OP),

]

VARDEC_TESTS = [

    ("var Apple : Int", PrimitiveType.Int, "Apple"),
    ("var Apple : Int = 1 ", PrimitiveType.Int, "Apple"),
    ("var Apple : Int = true ", PrimitiveType.ERROR, "Apple"),
    ("var Apple : Int = \"Hello\" ", PrimitiveType.ERROR, "Apple"),


    ("var Pear : Bool = true ", PrimitiveType.Bool, "Pear"),
    ("var Pear : Bool = false ", PrimitiveType.Bool, "Pear"),
    ("var Pear : Bool = \"Hello\" ", PrimitiveType.ERROR, "Pear"),
    ("var Pear : Bool = 654 ", PrimitiveType.ERROR, "Pear"),
    ("var Pear : Bool", PrimitiveType.Bool, "Pear"),


    ("var nectarine : String = 654 ", PrimitiveType.ERROR, "nectarine"),
    ("var nectarine : String = \"Hello\" ", PrimitiveType.String, "nectarine"),
    ("var nectarine : String = true ", PrimitiveType.ERROR, "nectarine"),
    ("var nectarine : String", PrimitiveType.String, "nectarine"),
]

VARASSIGN_TESTS_valid = [
    ("Apple = 1", PrimitiveType.Int, "Apple",{"Apple" : PrimitiveType.Int} ),
    ("Pear = true", PrimitiveType.Bool,"Pear", {"Pear" : PrimitiveType.Bool}),
    ("nectarine = \"The Best Fruit\"", PrimitiveType.String,"nectarine", {"nectarine": PrimitiveType.String }),
]

VARASSIGN_TESTS_invalid = [
    ("Apple = true", PrimitiveType.ERROR,  "Apple",{"Apple" : PrimitiveType.Int}),
    ("Apple = \"Hello\"", PrimitiveType.ERROR,  "Apple",{"Apple" : PrimitiveType.Int}),
    ("Apple = 1", PrimitiveType.ERROR,  "Apple",{"Apple" : PrimitiveType.ERROR}),

    ("Pear = 5", PrimitiveType.ERROR, "Pear", {"Pear": PrimitiveType.Bool}),
    ("Pear = \"Hello\"", PrimitiveType.ERROR, "Pear", {"Pear": PrimitiveType.Bool}),
    ("Pear = true", PrimitiveType.ERROR, "Pear", {"Pear": PrimitiveType.ERROR}),

    ("nectarine = 5", PrimitiveType.ERROR, "nectarine", {"nectarine": PrimitiveType.String}),
    ("nectarine = true", PrimitiveType.ERROR, "nectarine", {"nectarine": PrimitiveType.String}),
    ("nectarine = \"Hello\"", PrimitiveType.ERROR, "nectarine", {"nectarine": PrimitiveType.ERROR}),

]



class TypeAndStatementTests(unittest.TestCase):
    """
    Tests type inference for expressions, and constraint compliance for statements,
    other than function calls and return statements, which are handled by FunctionTests
    and ReturnTests, below.

    You should be able to re-use your tests from lab 3 here, adjusting for the new signature
    of `do_semantic_analysis`. All tests should succeed, except those using variables.
    """



    def test_valid_expressions(self):
        """
        For each pair (expression source, expected type) in VALID_EXPRESSIONS, verifies
        that the expression's inferred type is as expected, and that there are no errors
        in the error log.
        """
        for expression, expected_type in VALID_EXPRESSIONS:
            log, global_scope, inferred_types = do_semantic_analysis(expression, 'expr')
            # if expression == '-37':
            #     print_debug_info(expression, inferred_types, log)
            with self.subTest(expression=expression, expected_type=expected_type):
                self.assertEqual(expected_type, inferred_types[1][expression])
                self.assertEqual(0, log.total_entries())

    def test_invalid_expressions(self):
        """
        For each pair (expression source, expected error category) in INVALID_EXPRESSIONS,
        verifies that the expression is assigned the ERROR type and that there is a logged
        error of the expected category relating to the expression.
        """
        for expression, expected_category in INVALID_EXPRESSIONS:
            log, global_scope, inferred_types = do_semantic_analysis(expression, 'expr')
            # if expression == '!!37':
            #     print_debug_info(expression, inferred_types, log)
            with self.subTest(expression=expression,
                              expected_category=expected_category):
                self.assertEqual(PrimitiveType.ERROR, inferred_types[1][expression])
                self.assertTrue(log.includes_exactly(expected_category, 1, expression))

    # def test_variable_Declaration(self):
    #     """
    #     This was stolen from the above examples to rapidly loop through variables and see if they match their types.
    #
    #     This testcase uses a third field that is just the ID to allow for lookup of the
    #     variable in the variable dictionary
    #     """
    #
    #     for expression, expected_type, ID in VARDEC_TESTS:
    #         log, global_scope, inferred_types = do_semantic_analysis(expression, 'varDec')
    #         # if expression == '-37':
    #         #     print_debug_info(expression, inferred_types, log)
    #         with self.subTest(expression=expression, expected_type=expected_type):
    #             self.assertEqual(expected_type, variables[ID])
    #
    # def test_variable_assignment(self):
    #     """
    #     This was stolen from the above examples to rapidly loop through variables and see if they match their types.
    #
    #     This testcase uses a third field that is just the ID to allow for lookup of the
    #     variable in the variable dictionary
    #     """
    #
    #     for expression, expected_type, ID, setup in VARASSIGN_TESTS_valid:
    #         log, global_scope, inferred_types = do_semantic_analysis_initial_condition(expression, 'statement', setup)
    #         with self.subTest(expression=expression, expected_type=expected_type):
    #             self.assertEqual(expected_type, variables[ID])
    #             self.assertEqual(0, log.total_entries())
    #
    #     for expression, expected_type, ID, setup in VARASSIGN_TESTS_invalid:
    #         log, global_scope, inferred_types = do_semantic_analysis_initial_condition(expression, 'statement', setup)
    #         with self.subTest(expression=expression, expected_type=expected_type):
    #             self.assertEqual(expected_type, variables[ID])
    #             self.assertEqual(1, log.total_entries())

    def test_print_primitive(self):
        log, global_scope, inferred_types = do_semantic_analysis("print 123", 'main')
        self.assertEqual(0, log.total_entries())

        log, global_scope, inferred_types = do_semantic_analysis('print "hello"', 'main')
        self.assertEqual(0, log.total_entries())

        log, global_scope, inferred_types = do_semantic_analysis("print true", 'main')
        self.assertEqual(0, log.total_entries())

    def test_if_while_primitive(self):
        log, global_scope, inferred_types = do_semantic_analysis("if true { }", 'main')
        self.assertEqual(0, log.total_entries())

        log, global_scope, inferred_types = do_semantic_analysis('if true { } else { }', 'main')
        self.assertEqual(0, log.total_entries())

        log, global_scope, inferred_types = do_semantic_analysis("while true { }", 'main')
        self.assertEqual(0, log.total_entries())


OneFunctiontorulethemall = "func fone(){var Apple : Int = 1 }fone()"


class ScopeCreationTests(unittest.TestCase):
    """
    Tests that scopes are being correctly created and attached to the parse tree,
    with the correct enclosing relations and scope `return_type` attributes.

    Two example tests provided.
    """

    def test_script_defines_global_scope(self):
        log, global_scope, inferred_types = do_semantic_analysis(
            '', 'script', first_phase_only=True)
        self.assertIsNotNone(global_scope)
        self.assertIsInstance(global_scope, Scope)
        self.assertEqual('$global', global_scope.name)
        self.assertEqual(0, log.total_entries())

    def test_main_defines_scope(self):
        log, global_scope, inferred_types = do_semantic_analysis(
            '', 'script')  # , first_phase_only=True)
        self.assertEqual(1, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('$main'))
        main_scopes = global_scope.all_child_scopes_named('$main')
        self.assertEqual(1, len(main_scopes))
        self.assertIsInstance(main_scopes[0], Scope)

    def test_one_function_scope(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneFunctiontorulethemall, 'script')
        self.assertEqual(2, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('fone'))
        funcscope = global_scope.all_child_scopes_named('fone')
        self.assertEqual(global_scope, funcscope[0].enclosing_scope)
        self.assertIsInstance(funcscope[0], Scope)
        self.assertEqual(1, len(funcscope))


OneFunctiontofindthem = "func fone(){var Apple : Int = 1 } " \
                        "func fone(){var nectarine : String = \"Hello\"} " \
                        "var Pear : Bool = true "
ThreeFunctionsfortheElvenkingsunderthessky = "func fone(){var Apple : Int = 1 } " \
                                             "func ftwo(){var nectarine : String = \"Hello\"} " \
                                             "func fthree(){var nectarine : String = \"Hello\"} " \
                                             "var Pear : Bool = true "

OneFunctiononeparam = "func fone(Banana : Int ){var Apple : Int = 1 }fone()"
OneFunctionmanyparam = "func fone(Banana : Int, Pear : Int, Pineapple : Int ){var Apple : Int = 1 }fone()"
OneFunctionBadparam = "func fone(Banana : Int, Banana : String, Pineapple : Int ){var Apple : Int = 1 }fone()"



class FunctionSymbols(unittest.TestCase):
    """
    Tests that functions define appropriate symbols in the global scope and that
    duplicates are appropriately reported.
    """

    def test_duplicate_function_name(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneFunctiontofindthem, 'script')
        self.assertEqual(3, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('fone'))
        funcscope = global_scope.all_child_scopes_named('fone')
        self.assertEqual(global_scope, funcscope[0].enclosing_scope)
        self.assertIsNotNone(log)

    def test_multiple_function_name(self):
        log, global_scope, inferred_types = do_semantic_analysis(ThreeFunctionsfortheElvenkingsunderthessky, 'script')
        self.assertEqual(4, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('fone'))
        self.assertIsNotNone(global_scope.child_scope_named('ftwo'))
        self.assertIsNotNone(global_scope.child_scope_named('fthree'))

    def test_function_one_parameter(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneFunctiononeparam, 'script')
        self.assertEqual(2, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('fone'))
        funcscope = global_scope.all_child_scopes_named('fone')

        self.assertEqual(1, funcscope[0].parameter_index)

    def test_function_many_parameter(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneFunctionmanyparam, 'script')
        self.assertEqual(2, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('fone'))
        funcscope = global_scope.all_child_scopes_named('fone')

        self.assertEqual(3, funcscope[0].parameter_index)

    def test_duplicate_parameters(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneFunctionBadparam, 'script')
        self.assertEqual(2, len(global_scope.child_scopes))
        self.assertIsNotNone(global_scope.child_scope_named('fone'))
        funcscope = global_scope.all_child_scopes_named('fone')[0]
        self.assertEqual(3, funcscope.parameter_index)
        self.assertIsNotNone(log)




# Used to test the functions.
OneInt = "var apple : Int"
OneStr = "var pear : String"
OneBool = "var apple : Bool"
ThreVars = "var apple : Int var pear : String var apple : Bool"
DoubleVars = "var apple : Int var apple : String"


class ParameterAndVariableSymbols(unittest.TestCase):
    """
    Tests that parameters and variables define appropriate symbols in
    appropriate scopes, and that duplicates are appropriately reported.
    """

    def test_One_Int(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneInt, 'script')
        testing = global_scope.all_child_scopes_named('$main')[0]

        self.assertEqual(1, testing.variable_index)
        testvar = testing.resolve('apple')
        self.assertEqual(PrimitiveType.Int, testvar.type)

    def test_One_string(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneStr, 'script')
        testing = global_scope.all_child_scopes_named('$main')[0]

        self.assertEqual(1, testing.variable_index)
        testvar = testing.resolve('pear')
        self.assertEqual(PrimitiveType.String, testvar.type)

    def test_One_Bool(self):
        log, global_scope, inferred_types = do_semantic_analysis(OneBool, 'script')
        testing = global_scope.all_child_scopes_named('$main')[0]

        self.assertEqual(1, testing.variable_index)
        testvar = testing.resolve('apple')
        self.assertEqual(PrimitiveType.Bool, testvar.type)

    def test_Three_Vars(self):
        log, global_scope, inferred_types = do_semantic_analysis(ThreVars, 'script')
        testing = global_scope.all_child_scopes_named('$main')[0]

        self.assertEqual(3, testing.variable_index)
        # //Not testing if individual variables make it in because we know that they all make it individually

    def test_Eliminate_duplicates(self):
        log, global_scope, inferred_types = do_semantic_analysis(DoubleVars, 'script')
        testing = global_scope.all_child_scopes_named('$main')[0]

        self.assertEqual(2, testing.variable_index)
        self.assertIsNotNone(log)


CorrectFunctionWithParameters = "func fone(apple : Int) {var pear : Int = apple } fone(5)"


# OneFunctiononeparam = "func fone(Banana : Int ){var Apple : Int = 1 }fone()"
class FunctionTests(unittest.TestCase):
    """
    Tests functions used as variables, successful function calls, and failed
    function calls.
    """

    def test_function_using_parameters(self):
        log, global_scope, inferred_types = do_semantic_analysis(CorrectFunctionWithParameters, 'script')
        testing = global_scope.all_child_scopes_named('fone')[0]

        self.assertEqual(1, testing.parameter_index)
        self.assertEqual(1, testing.variable_index)
        test = testing.parameters()[0]
        test = test.type.value

        self.assertEqual(5, testing.parameters()[1])


ReturnTest = "func fone(Para1 : Int, Banana : Int, Pineapple : Int ) -> Int {var Apple : Bool = 1 return 1}fone()"
ReturnTest1 = "func fone(Para1 : Int, Banana : Int, Pineapple : Int ) -> Int {var Apple : Int = 1 return Apple}fone()"


class ReturnTests(unittest.TestCase):
    """
    Tests valid and invalid return statements, in both functions and the main.
    """

    # Todo Fix this one, as it has zero errors
    def test_function_return_type(self):
        log, global_scope, inferred_types = do_semantic_analysis(ReturnTest, 'script')
        self.assertEqual(0, log.total_entries())  # Bool returned as Int

    def test_function_return_type2(self):
        log, global_scope, inferred_types = do_semantic_analysis(ReturnTest1, 'script')
        self.assertEqual(0, log.total_entries())
