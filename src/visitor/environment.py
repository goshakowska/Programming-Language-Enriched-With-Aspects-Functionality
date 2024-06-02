from typing import Any
from src.ast_tree.function_definition import FunctionDefinition
from src.ast_tree.aspect_definition import AspectDefinition
from src.ast_tree.identifier import Identifier
from src.ast_tree.conditional_statement import ConditionalStatement
from src.ast_tree.function_call import FunctionCall
from src.ast_tree.variable_declaration import VariableDeclaration
from src.ast_tree.for_statement import ForStatement
from src.ast_tree.while_statement import WhileStatement
from src.ast_tree.return_statement import ReturnStatement
from src.ast_tree.assignment_statement import AssignmentStatement
from src.ast_tree.statements_block import StatementsBlock
from src.ast_tree.object_access import ObjectAccess
from src.ast_tree.indexed_item import IndexedItem
from src.ast_tree.unary_term import UnaryTerm
from src.ast_tree.casted_term import CastedTerm
from src.ast_tree.less_than_expression import LessThanExpression
from src.ast_tree.greater_than_expression import GreaterThanExpression
from src.ast_tree.equal_expression import EqualExpression
from src.ast_tree.not_equal_expression import NotEqualExpression
from src.ast_tree.less_than_or_equal_expression import\
      LessThanOrEqualExpression
from src.ast_tree.greater_than_or_equal_expression import\
      GreaterThanOrEqualExpression
from src.ast_tree.plus_expression import PlusExpression
from src.ast_tree.minus_expression import MinusExpression
from src.ast_tree.multiplication_expression import MultiplicationExpression
from src.ast_tree.division_expression import DivisionExpression
from src.ast_tree.or_expression import OrExpression
from src.ast_tree.and_expression import AndExpression
from src.ast_tree.ast_type import AstType
from src.ast_tree.program import Program
from src.ast_tree.bool_literal import BoolLiteral
from src.ast_tree.str_literal import StrLiteral
from src.ast_tree.int_literal import IntLiteral
from src.ast_tree.float_literal import FloatLiteral

class Value:
    def __init__(self, value: Any, type: Any) -> None:
        self.value = value
        self.type = type

    def set_value(self, value: Any) -> None:
        self.value = value

    def get_value(self) -> Any:
        return self.value

# class Variable:  # TODO!
#     def __init__(self, name: str, value: Value, type: Any) -> None:
#         self.name = name
#         self.value = value
#         self.type = type

#         self.TYPE_CONVERSIONS = {
#             (int, float): lambda x: float(x),
#             (float, int): lambda x: int(x) if x.is_integer() else None,
#             (int, str): lambda x: str(x),
#             (float, str): lambda x: str(x),
#             (str, bool): lambda x: bool({"true": 1, "false": 0}.get(x)),
#             (int, bool): lambda x: bool(x) if x in {0, 1} else None
#         }

#     def get_name(self) -> str:
#         return self.name

#     def set_value(self, value: any) -> None:
#         self.value = value

#     def set_type(self, type: Any) -> None:
#         self.type = type

#     def cast_variable_value(self, type_to_cast: Any):
#         type_conversion = self.TYPE_CONVERSIONS.get((self.type, type_to_cast))
#         if (new_type := type_conversion(self.value)) is not None:
#             self.type = new_type
#         else:
#             None  # w visit wyrzucam błąd!


class Scope:
    def __init__(self) -> None:
        # self.parent_scope = parent_scope
        self.variables = {}

    def find_and_set_old_variable(self, name: str):  # todo, aby sprawdzać czy zmienny różnych typów o tej samej nazwie
        if name in self.variables.keys():
            self.variables[variable.get_name()] = variable
            return True
        return False

    def add_variable(self, name: str, value: Value) -> None:
        if not self.find_and_set_old_variable(name):
            self.variables[name] = value

    def get_variable_value(self, variable_name: str) -> Any:  # czy to jest ok, że tu jest str a przy set obiekt
        scope = self
        while (value := scope.variables.get(variable_name)) is None and scope.parent_scope is not None:
            scope = scope.parent_scope
        return value


class CallContext:
    def __init__(self, function_name: str, expected_return_type: Any) -> None:
        self.function_name = function_name
        self.expected_return_type = expected_return_type
        self.scopes = [Scope()]

    def get_variable_value(self, variable_name: str) -> Any:
        for scope in reversed(self.scopes):
            value = scope.get_variable_value(variable_name)
            if value is not None:
                return value
        return None

    def add_variable(self, name: str, value: Value) -> None:
        # check_if_variable_exists
        self.scopes[-1].add_variable(name, value)


    # def get_function_definition(self, function_name: str):
    #     return self.functions.get(function_name)


    # def get_aspect_definition(self, aspect_name: str):
    #     return self.aspects.get(aspect_name)

    # def get_statement_definition(self, statement_name: str):
    #     return self.statements.get(statement_name)
    # czy potrzebne

class GlobalContext(Scope):
    def __init__(self, parent_scope: Scope = None):
        super().__init__(parent_scope)
        # self.functions = {}
        # self.aspects = {}
        # self.statements = {}

    def find_and_set_old_variable(self, variable: Variable):
        if variable.get_name() in self.variables.keys():
            self.variables[variable.get_name()] = variable
            return True
        return False


class Environment:
    def __init__(self) -> None:
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.call_contexts = []
        self.nesting_level = 0

    def enter_function_call(self, function_name: str, return_type: Any) -> None:
        self.nesting_level += 1
        self.call_contexts.append(CallContext(function_name, return_type))

    def exit_function_call(self) -> None:
        self.nesting_level -= 1
        self.call_contexts.pop()

    def enter_block(self) -> None:
        self.call_contexts[-1].add_new_scope()

    def exit_block(self) -> None:
        self.call_contexts[-1].delete_last_scope()

    def exit_function_context(self) -> None:
        self.current_scope = None
        self.nesting_level -= 1
        self.current_scope = self.call_contexts.pop() if len(self.call_contexts) != 0 else self.global_scope

    def get_variable(self, variable_name: str) -> Variable:
        return self.current_scope.get_variable(variable_name)

    def add_variable(self, name: str, value: Value) -> None:
        self.current_scope.add_variable(name, value)

    def create_parameters_scope(self, input_parameters: list, provided_arguments: list) -> None:
        initial_scope = Scope(self.current_scope)
        # błąd jeśli nie jest taka sama liczba parametrow i argumentów
        for parameter, argument in zip(input_parameters, provided_arguments):
            initial_scope.variables[parameter.name] = argument

        return initial_scope