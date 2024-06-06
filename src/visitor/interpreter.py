from typing import Any
from src.visitor.interpreter_errors import AdditionExpressionError
from src.visitor.interpreter_errors import SubtractionExpressionError
from src.visitor.interpreter_errors import DivisionExpressionError
from src.visitor.interpreter_errors import MultiplicationExpressionError
from src.visitor.interpreter_errors import GreaterThanExpressionError
from src.visitor.interpreter_errors import LessThanExpressionError
from src.visitor.interpreter_errors import GreaterThanOrEqualExpressionError
from src.visitor.interpreter_errors import LessThanOrEqualExpressionError
from src.visitor.interpreter_errors import OrExpressionError
from src.visitor.interpreter_errors import AndExpressionError
from src.visitor.interpreter_errors import NegatedTermError
from src.visitor.interpreter_errors import CastingTypeError
from src.visitor.interpreter_errors import EmbeddedFunctionOverrideError
from src.visitor.interpreter_errors import FunctionNotFoundError
from src.visitor.interpreter_errors import WrongNumberOfArgumentsError
from src.visitor.interpreter_errors import WrongArgumentTypeError
from src.visitor.interpreter_errors import ReturnOutsideFunctionCallError
from src.visitor.interpreter_errors import DivisionByZeroError
from src.visitor.interpreter_errors import IncorrectReturnTypeError
from src.visitor.interpreter_errors import UndefinedFunctionError
from src.visitor.interpreter_errors import ReturnInAspectDefinitionError
from src.visitor.interpreter_errors import ObjectAttributeError
from src.visitor.interpreter_errors import NotInitializedVariableAccessError
from src.visitor.interpreter_errors import UnsupportedObjectAccessTypeError

from src.visitor.visitor import Visitor
from src.ast_tree.and_expression import AndExpression
from src.ast_tree.aspect_definition import AspectDefinition
from src.ast_tree.assignment_statement import AssignmentStatement
from src.ast_tree.bool_literal import BoolLiteral
from src.ast_tree.casted_term import CastedTerm
from src.ast_tree.conditional_statement import ConditionalStatement
from src.ast_tree.division_expression import DivisionExpression
from src.ast_tree.equal_expression import EqualExpression
from src.ast_tree.float_literal import FloatLiteral
from src.ast_tree.for_statement import ForStatement
from src.ast_tree.function_call import FunctionCall
from src.ast_tree.function_definition import FunctionDefinition
from src.ast_tree.greater_than_expression import GreaterThanExpression
from src.ast_tree.greater_than_or_equal_expression import GreaterThanOrEqualExpression
from src.ast_tree.identifier import Identifier
from src.ast_tree.int_literal import IntLiteral
from src.ast_tree.less_than_expression import LessThanExpression
from src.ast_tree.less_than_or_equal_expression import LessThanOrEqualExpression
from src.ast_tree.minus_expression import MinusExpression
from src.ast_tree.multiplication_expression import MultiplicationExpression
from src.ast_tree.not_equal_expression import NotEqualExpression
from src.ast_tree.or_expression import OrExpression
from src.ast_tree.plus_expression import PlusExpression
from src.ast_tree.program import Program
from src.ast_tree.return_statement import ReturnStatement
from src.ast_tree.statements_block import StatementsBlock
from src.ast_tree.str_literal import StrLiteral
from src.ast_tree.unary_term import UnaryTerm
from src.ast_tree.variable_declaration import VariableDeclaration
from src.ast_tree.while_statement import WhileStatement
from src.ast_tree.ast_type import AstType

from src.visitor.visitable import PrintFunction
from src.visitor.environment import Environment, Value

from src.visitor.environment import AspectValue, FunctionValue, Args, Param

ITERATION_LIMIT = 100


class Interpreter(Visitor):

    def __init__(self, program: Program) -> None:
        self.program = program

        self.functions = program.functions
        self.statements = program.statements
        self.aspects = program.aspects

        self.enabled_aspects = set(self.aspects.keys())

        self._last_result = None
        self._return_flag = False

        self.EMBEDDED_FUNCTIONS = {"print": PrintFunction()}
        self.add_embedded_functions_to_program(self.EMBEDDED_FUNCTIONS)

        self.environment = Environment()

    def get_last_result(self):
        last_result = self._last_result
        self._last_result = None
        return last_result

    def set_last_result(self, result):
        self._last_result = result

    def add_embedded_functions_to_program(self, embedded_functions: dict):
        for name, function in embedded_functions.items():
            if name not in self.functions.keys():
                self.functions[name] = function
            else:
                raise EmbeddedFunctionOverrideError(name)

    def visit_print_function(self, node: PrintFunction):

        print_conversions = {
            AstType.TYPE_INT: str,
            AstType.TYPE_FLOAT: str,
            AstType.TYPE_BOOL: lambda x: "true" if x else "false",
            AstType.TYPE_STR: lambda x: x
        }

        content_to_print = self.get_last_result()
        if content_to_print is not None:
            node.set_arguments(content_to_print)
            string_to_print = "".join(
                print_conversions[argument.type](argument.value) if argument.type in print_conversions else str(argument.value)
                for argument in node.arguments
            )
            print(string_to_print)

    def _enable_aspect(self, aspect_name: str):
        if aspect_name not in self.enabled_aspects:
            self.aspects.get(aspect_name).enabled = True
            self.enabled_aspects.add(aspect_name)

    def _disable_aspect(self, aspect_name: str):
        if aspect_name in self.enabled_aspects:
            self.aspects.get(aspect_name).enabled = False
            self.enabled_aspects.remove(aspect_name)

    def _check_if_is_target(self, aspect: AspectDefinition,
                            function_name: str):
        return aspect.regular_expression.name in function_name

    """
    PROGRAM
    """

    def visit_program(self, node: Program):

        for statement in node.statements:
            statement.accept(self)

    """
    DEFINITIONS
    """

    def update_targeted_function(self, instance: FunctionValue, **kwargs):
        instance._set_updating(True)
        instance.increment_call_count()
        for attribute, new_value in kwargs.items():
            setattr(instance, attribute, new_value)
        instance._set_updating(False)

    def visit_aspect_definition(self, node: AspectDefinition):
        AST_TYPE_TO_STR = {
            AstType.TYPE_INT: "int",
            AstType.TYPE_FLOAT: "float",
            AstType.TYPE_BOOL: "bool",
            AstType.TYPE_STR: "str",
            AstType.NULL: "null"
        }
        if not self._check_if_is_target(node, self._last_result[0]):
            return None
        (
            function_name,
            input_parameters,
            provided_arguments,
            return_value,
            return_type
        ) = self.get_last_result()

        provided_params = [Param(Value(param_name.name, param_name.type), provided_value, Value(AST_TYPE_TO_STR.get(provided_value.type), provided_value.type)) for param_name, provided_value in zip(input_parameters, provided_arguments)]

        arguments = Args(provided_params) if provided_params else None

        targeted_function = FunctionValue(
            name=Value(function_name, AstType.TYPE_STR),
            args=arguments if arguments else None,
            return_value=return_value if return_value else None,
            return_type=Value(AST_TYPE_TO_STR.get(return_type),
                              AstType.TYPE_STR)
        )

        if (
            aspect_value := self.environment.check_for_global_aspect(node.name)
             ) is not None:
            if aspect_value.targets.get(function_name) is not None:
                targeted_function = aspect_value.targets.get(function_name)
                targeted_function.accept_updater(self,
                                                 args=arguments,
                                                 return_type=return_value)
            else:
                aspect_value.targets.update({function_name: targeted_function})
        else:
            self.environment.add_global_variable(node.name,
                                                 AspectValue(function_name,
                                                             targeted_function))

        self.environment.enter_aspect_block(targeted_function)
        node.block.accept(self)
        if self._return_flag is True:
            raise ReturnInAspectDefinitionError(node.block.position,
                                                node.name)
        self.environment.exit_block()

    def _check_input_parameters(self,
                                function: FunctionDefinition,
                                provided_arguments: list):
        if len(provided_arguments) != len(function.params):
            raise WrongNumberOfArgumentsError(function.position,
                                              function.name,
                                              len(function.params),
                                              len(provided_arguments))
        for provided_argument, input_parameter in zip(provided_arguments,
                                                      function.params):
            if input_parameter.type != provided_argument.type:
                raise WrongArgumentTypeError(function.position,
                                             input_parameter.name,
                                             input_parameter.type,
                                             provided_argument.type)
            self.environment.add_variable(input_parameter.name,
                                          provided_argument)
        self.set_last_result(provided_arguments)

    def _update_enabled_aspects(self):
        current_enabled_aspects = set()
        for var_name, var_value in self.environment.global_scope.variables.items():
            if isinstance(var_value, AspectValue):
                if var_value.enabled:
                    current_enabled_aspects.add(self.aspects.get(var_name))

        self.enabled_aspects = current_enabled_aspects

    def _check_and_visit_aspects(self,
                                 node: FunctionDefinition,
                                 aspect_types: set[AstType],
                                 provided_arguments: list,
                                 return_value: Any = None):

        # self._update_enabled_aspects()
        for aspect_name in self.enabled_aspects:
            if self.aspects.get(aspect_name).event in aspect_types:
                self.set_last_result(
                    [node.name,
                     node.params,
                     provided_arguments,
                     return_value,
                     node.return_type])

                self.visit_aspect_definition(self.aspects.get(aspect_name))

    def visit_function_definition(self, node: FunctionDefinition):

        self.environment.enter_function_call(node.name, node.return_type)

        self._check_input_parameters(node, self.get_last_result())
        provided_arguments = self.get_last_result()

        # self._update_enabled_aspects()
        self._check_and_visit_aspects(node,
                                      {AstType.ASPECT_ON_START,
                                       AstType.ASPECT_ON_CALL},
                                      provided_arguments,
                                      None)

        for statement in node.block.statements:
            statement.accept(self)
            if self._return_flag is True:
                break

        return_value = None
        if self._return_flag is True:
            return_value = self.get_last_result()
            self._return_flag = False
        if not return_value.type == node.return_type:
            raise IncorrectReturnTypeError(node.position, node.name,
                                           node.return_type, return_value)

        self._check_and_visit_aspects(node,
                                      {AstType.ASPECT_ON_END},
                                      provided_arguments,
                                      return_value)

        self.set_last_result(return_value)
        self.environment.exit_function_call()

    """
    STATEMENTS
    """
    def visit_identifier(self, node: Identifier) -> None:
        value = self.environment.get_variable(node.name)
        self.set_last_result(value)

    def _in_functions_definitions(self, name: str) -> bool:
        return name in self.functions

    def prepare_arguments_for_function_call(self, arguments) -> list[Value]:
        input_parameters = []
        for argument in arguments:
            argument.accept(self)
            input_parameters.append(self.get_last_result())
        self.set_last_result(input_parameters)

    def visit_function_call(self, node: FunctionCall):
        if not (function := self.functions.get(node.name)):
            raise UndefinedFunctionError(node.position, node.name)
        self.prepare_arguments_for_function_call(node.arguments)
        function.accept(self)

    def visit_statements_block(self, node: StatementsBlock):

        self.environment.enter_block()
        for statement in node.statements:
            statement.accept(self)
            if self._return_flag is True:
                break
        self.environment.exit_block()

    def visit_assignment_statement(self, node: AssignmentStatement):
        node.object_access.accept(self)
        variable_value = self.get_last_result()
        if variable_value is not None:
            node.expression.accept(self)
            new_value = self.get_last_result()
            variable_value.set_value(new_value)

    def visit_object_access(self, node: Identifier | FunctionCall):

        parent = None
        if node.parent is not None:
            try:
                parent = self.environment.get_variable(node.parent.name)
            except NotInitializedVariableAccessError:
                NotInitializedVariableAccessError(node.position,
                                                  node.parent,
                                                  node.name)

            if hasattr(parent, node.name):
                attribute = getattr(parent, node.name)
                self.set_last_result(attribute)
            else:
                raise ObjectAttributeError(node.position, parent, node.name)
        else:
            if isinstance(node, Identifier):
                self.visit_identifier(node)
            elif isinstance(node, FunctionCall):
                self.visit_function_call(node)
            else:
                raise UnsupportedObjectAccessTypeError(node.position,
                                                       node.parent,
                                                       node.name)

    def visit_conditional_statement(self, node: ConditionalStatement):

        node.expression.accept(self)
        condition_evaluation = self.get_last_result()
        if condition_evaluation.value:
            node.if_block.accept(self)
            if node.else_block:
                node.else_block.accept(self)

    def visit_for_statement(self, node: ForStatement):

        node.iterable.accept(self)
        iterable = self.get_last_result()
        node.iterator.accept(self)
        if isinstance(iterable, list):
            for _ in iterable:
                node.execution_block.accept(self)
                if self._return_flag is True:
                    break

    def visit_while_statement(self, node: WhileStatement):

        node.condition.accept(self)
        condition_evaluation = self.get_last_result()
        iteration_counter = 0
        while condition_evaluation.value:
            if iteration_counter == ITERATION_LIMIT:
                raise RuntimeError(node.position, ITERATION_LIMIT)
            node.execution_block.accept(self)
            if self._return_flag is True:
                break
            node.condition.accept(self)
            condition_evaluation = self.get_last_result()
            iteration_counter += 1

    def visit_variable_declaration(self, node: VariableDeclaration):

        value = Value(None, node.type)
        self.set_last_result(value)
        self.environment.add_variable(node.name, value)

    def visit_return_statement(self, node: ReturnStatement):

        if not self.environment.check_if_in_call_context():
            raise ReturnOutsideFunctionCallError(node.position)
        if node.expression is None:
            self.set_last_result(Value(None, AstType.NULL))
        else:
            node.expression.accept(self)
        self._return_flag = True

    """
    EXPRESSIONS
    """
    def visit_or_expression(self, node: OrExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, bool) and isinstance(right_term.value, bool):
            self.set_last_result(Value(left_term.value or right_term.value, AstType.TYPE_BOOL))
        else:
            raise OrExpressionError(node.position, left_term.value, right_term.value)

    def visit_and_expression(self, node: AndExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, bool) and isinstance(right_term.value, bool):
            self.set_last_result(Value(left_term.value and right_term.value, AstType.TYPE_BOOL))
        else:
            raise AndExpressionError(node.position, left_term.value, right_term.value)

    def visit_equal_expression(self, node: EqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value == right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))

    def visit_not_equal_expression(self, node: NotEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        self.set_last_result(Value(False, AstType.TYPE_BOOL)) if left_term.value == right_term.value else self.set_last_result(Value(True, AstType.TYPE_BOOL))

    def visit_greater_than_expression(self, node: GreaterThanExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value > right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise GreaterThanExpressionError(node.position,
                                             left_term.value,
                                             right_term.value)

    def visit_greater_than_or_equal_expression(self, node: GreaterThanOrEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value >= right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise GreaterThanOrEqualExpressionError(node.position, left_term.value, right_term.value)

    def visit_less_than_expression(self, node: LessThanExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value < right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise LessThanExpressionError(node.position, left_term.value, right_term.value)

    def visit_less_than_or_equal_expression(self, node: LessThanOrEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value <= right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise LessThanOrEqualExpressionError(node.position, left_term.value, right_term.value)

    def visit_minus_expression(self, node: MinusExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            result_value = left_term.value - right_term.value
            if isinstance(left_term.value, int) and isinstance(right_term.value, int):
                result_type = AstType.TYPE_INT
            else:
                result_type = AstType.TYPE_FLOAT
            self.set_last_result(Value(result_value, result_type))
        else:
            raise SubtractionExpressionError(node.position, left_term.value, right_term.value)

    def visit_plus_expression(self, node: PlusExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, str) and isinstance(right_term.value, str):
            result_value = left_term.value + right_term.value
            result_type = AstType.TYPE_STR
            self.set_last_result(Value(result_value, result_type))
        elif isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            result_value = left_term.value + right_term.value
            if isinstance(left_term.value, int) and isinstance(right_term.value, int):
                result_type = AstType.TYPE_INT
            else:
                result_type = AstType.TYPE_FLOAT
            self.set_last_result(Value(result_value, result_type))
        else:
            raise AdditionExpressionError(node.position, left_term.value, right_term.value)

    def visit_division_expression(self, node: DivisionExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            if right_term.value == 0:
                raise DivisionByZeroError(node.position, left_term)
            result_value = int(left_term.value / right_term.value)
            if isinstance(left_term.value, int) and isinstance(right_term.value, int):
                result_type = AstType.TYPE_INT
            else:
                result_type = AstType.TYPE_FLOAT
            self.set_last_result(Value(result_value, result_type))
        else:
            raise DivisionExpressionError(node.position, left_term.value, right_term.value)

    def visit_multiplication_expression(self, node: MultiplicationExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            result_value = left_term.value * right_term.value
            if isinstance(left_term.value, int) and isinstance(right_term.value, int):
                result_type = AstType.TYPE_INT
            else:
                result_type = AstType.TYPE_FLOAT
            self.set_last_result(Value(result_value, result_type))
        else:
            raise MultiplicationExpressionError(node.position, left_term.value, right_term.value)

    """
    TERMS
    """

    def visit_unary_term(self, node: UnaryTerm):
        node.term.accept(self)
        value = self.get_last_result()
        negation_functions = {
            AstType.TYPE_INT: lambda x: -x,
            AstType.TYPE_FLOAT: lambda x: -x,
            AstType.TYPE_BOOL: lambda x: not x
        }
        if negation_conversion := negation_functions.get(value.type):
            negated_value = negation_conversion(value.value)
            self.set_last_result(Value(negated_value, value.type))
        else:
            raise NegatedTermError(node.position, value)

    def visit_casted_term(self, node: CastedTerm):
        TYPE_CONVERSIONS = {
                (AstType.TYPE_INT, AstType.TYPE_FLOAT): lambda x: float(x),
                (AstType.TYPE_FLOAT, AstType.TYPE_INT): lambda x: int(x) if x.is_integer() else None,
                (AstType.TYPE_INT, AstType.TYPE_STR): lambda x: str(x),
                (AstType.TYPE_STR, AstType.TYPE_INT): lambda x: int(x) if x.isdigit() else None,
                (AstType.TYPE_STR, AstType.TYPE_FLOAT): lambda x: float(x) if x.replace('.', '', 1).isdigit() and x.count('.') <= 1 else None,
                (AstType.TYPE_FLOAT, AstType.TYPE_STR): lambda x: str(x),
                (AstType.TYPE_BOOL, AstType.TYPE_STR): lambda x: str(x).lower(),
                (AstType.TYPE_STR, AstType.TYPE_BOOL): lambda x: bool({"true": 1, "false": 0}.get(x)),
                (AstType.TYPE_INT, AstType.TYPE_BOOL): lambda x: bool(x) if x in {0, 1} else None
            }
        node.term.accept(self)
        term = self.get_last_result()
        type_conversion = TYPE_CONVERSIONS.get((term.type,
                                                node.casted_type))
        if type_conversion is not None and type_conversion(term.value) is not None:
            self.set_last_result(Value(type_conversion(term.value),
                                       node.casted_type))
        else:
            raise CastingTypeError(node.position,
                                   term,
                                   term.type,
                                   node.casted_type)

    """
    LITERALS
    """
    def visit_str_literal(self, node: StrLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_STR))

    def visit_int_literal(self, node: IntLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_INT))

    def visit_float_literal(self, node: FloatLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_FLOAT))

    def visit_bool_literal(self, node: BoolLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_BOOL))
