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
        # todo add way to poll if there is already a name with that scope

    def enterScript(self, ctx: NimbleParser.ScriptContext):
        MyGlobal = Scope("$global", None, None)
        ctx.scope = MyGlobal
        self.current_scope = MyGlobal

    def enterFuncDef(self, ctx: NimbleParser.FuncDefContext):
        # adding testing to see if the function name as already been chosen
        test = self.current_scope.resolve(str(ctx.ID()))

        if test:
            print("A function with this name has already been created")
            return

        parameters = ctx.parameterDef()

        myfunc = FunctionType(parameters, ctx.TYPE())

        self.current_scope.define(ctx.ID(), myfunc)

        MyScope = Scope(str(ctx.ID()), ctx.TYPE(), self.current_scope)

        self.current_scope.define(str(ctx.ID()), ctx.TYPE())
        ctx.scope = MyScope
        self.current_scope = MyScope

        for parameter in parameters:
            self.current_scope.define(parameter.ID(), parameter.TYPE(), True)

    def exitFuncDef(self, ctx: NimbleParser.FuncDefContext):
        self.current_scope = ctx.parentCtx.scope

    def enterMain(self, ctx: NimbleParser.MainContext):
        MyMain = Scope("$main", None, self.current_scope)
        ctx.scope = MyMain
        self.current_scope = MyMain


class InferTypesAndCheckConstraints(NimbleListener):

    def __init__(self, error_log: ErrorLog):
        self.error_log = error_log
        self.current_scope = None

    # --------------------------------------------------------
    # Program structure
    # Deliberately left blank because the examples shown in class did not
    # have any tests in these areas, as there is no type to assign.
    # --------------------------------------------------------

    def exitScript(self, ctx: NimbleParser.ScriptContext):
        pass

    def exitMain(self, ctx: NimbleParser.MainContext):
        pass

    def exitBody(self, ctx: NimbleParser.BodyContext):
        pass

    def exitVarBlock(self, ctx: NimbleParser.VarBlockContext):
        pass

    def exitBlock(self, ctx: NimbleParser.BlockContext):
        pass

    # --------------------------------------------------------
    # Variable declarations
    # --------------------------------------------------------

    # def exitVarDec(self, ctx: NimbleParser.VarDecContext):
    #     vartype = ctx.TYPE().getSymbol()
    #     vartype = vartype.text
    #
    #     if vartype == "Int":
    #         if ctx.expr():
    #             if ctx.expr().type == PrimitiveType.Int:
    #                 ctx.type = PrimitiveType.Int
    #             else:
    #                 ctx.type = PrimitiveType.ERROR
    #                 self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                                    f"{ctx.ID()} is declared type {vartype}\n\t"
    #                                    f"you tried to assigning a {ctx.expr().type} to it\n\t"
    #                                    f"This is an illegal operation. Straight to jail")
    #
    #         else:
    #             ctx.type = PrimitiveType.Int
    #
    #     elif vartype == "Bool":
    #
    #         if ctx.expr():
    #             if ctx.expr().type == PrimitiveType.Bool:
    #                 ctx.type = PrimitiveType.Bool
    #             else:
    #                 ctx.type = PrimitiveType.ERROR
    #                 self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                                    f"{ctx.ID()} is declared type {vartype}\n\t"
    #                                    f"you tried to assigning a {ctx.expr().type} to it\n\t"
    #                                    f"This is an illegal operation. Straight to jail")
    #
    #
    #         else:
    #             ctx.type = PrimitiveType.Bool
    #
    #
    #     elif vartype == "String":
    #         if ctx.expr():
    #             if ctx.expr().type == PrimitiveType.String:
    #                 ctx.type = PrimitiveType.String
    #             else:
    #                 ctx.type = PrimitiveType.ERROR
    #                 self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                                    f"{ctx.ID()} is declared type {vartype}\n\t"
    #                                    f"you tried to assigning a {ctx.expr().type} to it\n\t"
    #                                    f"This is an illegal operation. Straight to jail")
    #         else:
    #             ctx.type = PrimitiveType.String
    #
    #     newkey = str(ctx.ID())
    #
    #     self.variables[newkey] = ctx.type

    # print(self.variables)

    # --------------------------------------------------------
    # Statements
    # --------------------------------------------------------

    # def exitAssignment(self, ctx: NimbleParser.AssignmentContext):
    #     vartype = self.variables[str(ctx.ID())]
    #
    #     if vartype == PrimitiveType.Int:
    #         if ctx.expr().type == PrimitiveType.Int:
    #             ctx.type = PrimitiveType.Int
    #             ctx.valid = True
    #         else:
    #             ctx.type = PrimitiveType.ERROR
    #             self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                                f"{ctx.ID()} is declared type {vartype}\n\t"
    #                                f"you tried to assigning a {ctx.expr().type} to it\n\t"
    #                               f"This is an illegal operation. Straight to jail")
    #
    #
    #     elif vartype == PrimitiveType.Bool:
    #
    #         if ctx.expr().type == PrimitiveType.Bool:
    #             ctx.type = PrimitiveType.Bool
    #             ctx.valid = True
    #        else:
    #             ctx.type = PrimitiveType.ERROR
    #             ctx.valid = False
    #             self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                                f"{ctx.ID()} is declared type {vartype}\n\t"
    #                                f"you tried to assigning a {ctx.expr().type} to it\n\t"
    #                                f"This is an illegal operation. Straight to jail")
    #     elif vartype == PrimitiveType.String:
    #         if ctx.expr().type == PrimitiveType.String:
    #             ctx.type = PrimitiveType.String
    #             ctx.valid = True
    #         else:
    #             ctx.type = PrimitiveType.ERROR
    #             ctx.valid = False
    #          self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                                f"{ctx.ID()} is declared type {vartype}\n\t"
    #                                f"you tried to assigning a {ctx.expr().type} to it\n\t"
    #                                f"This is an illegal operation. Straight to jail")
    #
    #     else:
    #         ctx.type = PrimitiveType.ERROR
    #         ctx.valid = False
    #         self.error_log.add(ctx, Category.ASSIGN_TO_WRONG_TYPE,
    #                            f"{ctx.ID()} has previously been missassigned\n\t")
    #
    #      newkey = str(ctx.ID())
    #      self.variables[newkey] = ctx.type

    def exitWhile(self, ctx: NimbleParser.WhileContext):
        if ctx.expr().type != PrimitiveType.Bool:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.CONDITION_NOT_BOOL,
                               f"Expression {ctx.expr().text} not boolean")
            return

    def exitIf(self, ctx: NimbleParser.IfContext):

        if ctx.expr().type != PrimitiveType.Bool:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.CONDITION_NOT_BOOL,
                               f"Expression {ctx.expr().text} not boolean")
            return

    def exitPrint(self, ctx: NimbleParser.PrintContext):

        if ctx.expr().type == PrimitiveType.ERROR:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.UNPRINTABLE_EXPRESSION,
                               f"Can't print {ctx.op.text} ")

    # --------------------------------------------------------
    # Expressions
    # --------------------------------------------------------

    def exitIntLiteral(self, ctx: NimbleParser.IntLiteralContext):
        ctx.type = PrimitiveType.Int

    def exitNeg(self, ctx: NimbleParser.NegContext):

        if ctx.op.text == '-' and ctx.expr().type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
        elif ctx.op.text == '-':  # if !is used on non ints
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_NEGATION,
                               f"Can't apply {ctx.op.text} to {ctx.expr().type.name}")

        if ctx.op.text == '!' and ctx.expr().type == PrimitiveType.Bool:
            ctx.type = PrimitiveType.Bool
        elif ctx.op.text == '!':  # if ! is used on non bools
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_NEGATION,
                               f"Can't apply {ctx.op.text} to {ctx.expr().type.name}")

    def exitParens(self, ctx: NimbleParser.ParensContext):
        ctx.type = ctx.expr().type

    def exitMulDiv(self, ctx: NimbleParser.MulDivContext):
        if ctx.expr(0).type == PrimitiveType.Int and ctx.expr(1).type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
        else:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                               f"Can't apply {ctx.op.text} to {ctx.expr(0).type.name} and {ctx.expr(1).type.name}")

    def exitAddSub(self, ctx: NimbleParser.AddSubContext):

        if ctx.expr(0).type == PrimitiveType.Int and ctx.expr(1).type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
            return
        elif ctx.expr(0).type == PrimitiveType.String and ctx.expr(
                1).type == PrimitiveType.String and ctx.op.text == '+':
            ctx.type = PrimitiveType.String
            return

        ctx.type = PrimitiveType.ERROR
        self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                           f"Can't apply {ctx.op.text} to {ctx.expr(0).type.name} and {ctx.expr(1).type.name}")

    def exitCompare(self, ctx: NimbleParser.CompareContext):

        if ctx.expr(0).type == PrimitiveType.Int and ctx.expr(1).type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Bool
        else:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                               f"Can't apply {ctx.op.text} to {ctx.expr(0).type.name} and {ctx.expr(1).type.name}")

    # def exitVariable(self, ctx: NimbleParser.VariableContext):
    #   if str(ctx.ID()) in self.variables:
    #      ctx.type = self.variables[str(ctx.ID())]
    #
    #       else:
    #          self.error_log.add(ctx,Category.UNDEFINED_NAME,
    #                            f"This {str(ctx.ID())} has not been defined")

    def exitStringLiteral(self, ctx: NimbleParser.StringLiteralContext):
        ctx.type = PrimitiveType.String

    def exitBoolLiteral(self, ctx: NimbleParser.BoolLiteralContext):
        ctx.type = PrimitiveType.Bool
