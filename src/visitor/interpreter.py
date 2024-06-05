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
from src.ast_tree.indexed_item import IndexedItem
from src.ast_tree.int_literal import IntLiteral
from src.ast_tree.less_than_expression import LessThanExpression
from src.ast_tree.less_than_or_equal_expression import LessThanOrEqualExpression
from src.ast_tree.minus_expression import MinusExpression
from src.ast_tree.multiplication_expression import MultiplicationExpression
from src.ast_tree.node import Node
from src.ast_tree.not_equal_expression import NotEqualExpression
from src.ast_tree.object_access import ObjectAccess
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

from src.visitor.environment import  AspectValue, FunctionValue, Args, Param

ITERATION_LIMIT = 100


class Interpreter(Visitor):

    def __init__(self, program: Program, start_function_name: str = "", *args) -> None:
        self.program = program

        self.functions = program.functions
        self.statements = program.statements
        self.aspects = program.aspects

        self.enabled_aspects = set(self.aspects.keys())

        self._program_root = start_function_name
        if self._program_root:
            self.input_parameters = list(args)

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
            AstType.TYPE_INT: lambda x: str(x),
            AstType.TYPE_FLOAT: lambda x: str(x),
            AstType.TYPE_BOOL: lambda x: "true" if x else "false",
            AstType.TYPE_STR: lambda x: x
        }

        content_to_print = self.get_last_result()
        if content_to_print is not None:
            node.set_arguments(content_to_print)
            string_to_print = "".join(
                print_conversions[argument.type](argument.value) if argument.type in print_conversions else str(argument.value)
                for argument in node.arguments
            )  # upewnić się potem czy obiekty klasy przechodzą to
            print(string_to_print)  # ? czy tak można?

    def _enable_aspect(self, aspect_name: str):  # jakie rozwiązanie lepsze - pole enabled w Aspect, czy zbiór enabled w interpreterze?
        if aspect_name not in self.enabled_aspects:
            self.aspects.get(aspect_name).enabled = True
            self.enabled_aspects.add(aspect_name)

    def _disable_aspect(self, aspect_name: str):
        if aspect_name in self.enabled_aspects:
            self.aspects.get(aspect_name).enabled = False
            self.enabled_aspects.remove(aspect_name)

    def _check_if_is_target(self, aspect: AspectDefinition,
                                     function_name: str):
        return function_name in aspect.target


    """
    PROGRAM
    """

    # * działa
    def visit_program(self, node: Program):

        if self._program_root:
            if self._program_root not in self.functions:
                raise FunctionNotFoundError(self._program_root)
            if self.input_parameters:
                self.set_last_result(self.input_parameters)
            self.functions.get(self._program_root).accept(self)  # sięgam po obiekt funkcji

        for statement in node.statements:
            statement.accept(self)

    """
    DEFINITIONS
    """

    def update_targeted_function(self, instance: FunctionValue, **kwargs):
        instance._set_updating(True)
        instance._increment_call_count()
        for attribute, new_value in kwargs.items():
            setattr(instance, attribute, new_value)
        instance._set_updating(False)

    def visit_aspect_definition(self, node: AspectDefinition):
        if not self._check_if_is_target(node.target, self._last_result[0]):
            return None
        (
            function_name,
            input_parameters,
            provided_arguments,
            return_value,
            return_type
        ) = self.get_last_result()  # czy te nawiasy nie popsują?

        arguments = Args(
            Param(param_name, provided_value, provided_value.type)
            for param_name, provided_value in zip(input_parameters,
                                                  provided_arguments)
        ) if input_parameters else None

        targeted_function = FunctionValue(
            name=function_name,
            args=arguments,
            return_value=return_value,
            return_type=return_type
        )

        if (aspect_value := self.environment.check_for_global_aspect(node.name)) is not None:
            if (targeted_function := aspect_value.targets.get(function_name)) is not None:
                targeted_function.accept_updater(self,
                                                 args=arguments,
                                                 return_type=return_value)
        else:
            self.environment.add_global_variable(
                AspectValue(node.name, {targeted_function}))

        for statement in node.block:
            if isinstance(statement, ReturnStatement):
                raise ReturnInAspectDefinitionError(statement.position,
                                                    node.name)
            statement.accept(self)

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
        self.set_last_result(provided_arguments)  # ? czy dobrze zmieniłam?

    def visit_function_definition(self, node: FunctionDefinition):

        self._check_input_parameters(node, self.get_last_result())
        provided_arguments = self.get_last_result()

        self.environment.enter_function_call(node.name, node.return_type)

        for aspect_name in self.enabled_aspects:
            if self.aspects.get(aspect_name).event == AstType.ASPECT_ON_START \
                 or \
                 self.aspects.get(aspect_name).event == AstType.ASPECT_ON_CALL:

                self.set_last_result([node.name, node.params,
                                      provided_arguments, None,
                                      node.return_type])

                self.visit_aspect_definition(self.aspects.get(aspect_name))

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

        self.set_last_result([node.name, return_value])

        for aspect_name in self.enabled_aspects:
            if self.aspects.get(aspect_name).event == AstType.ASPECT_ON_START:
                self.visit_active_on_end_aspect_definition(self.aspects.get(aspect_name))
        self.set_last_result(return_value)
        self.environment.exit_function_call()


    """
    STATEMENTS
    """

    # ? działa
    def visit_identifier(self, node: Identifier) -> None:
        # w variables przechowywać aspekty - nazwa aspektu: Value (value = ciało aspektu, type = aspektType) albo odpytywać czy to nie aspekt
        # self._check_if_aspect(node.name)
        value = self.environment.get_variable(node.name)
        self.set_last_result(value)

    def _in_functions_definitions(self, name: str) -> bool:
        return name in self.functions

    # * działa
    def prepare_arguments_for_function_call(self, arguments) -> list[Value]:

        input_parameters = []
        for argument in arguments:
            argument.accept(self)  # zwraca obiekt typu Value
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

    # ? działa
    def visit_assignment_statement(self, node: AssignmentStatement):
        # FIXME!
        node.object_access.accept(self)  # a.b = c;  # to powinno mi ZAWSZE zwracać Value()
        variable_value = self.get_last_result()
        if variable_value is not None:  # ten warunek, gdy dostajemy variable value zawsze jest true
            node.expression.accept(self)
            new_value = self.get_last_result()
            # node.object_access.set_value(new_value)
            variable_value.set_value(new_value)
            # self.environment.get_variable(variable_name).set_value(new_value)

# logParam.enable = True;
    def visit_object_access(self, node: Identifier | FunctionCall):

        parent = None
        if node.parent is not None:
            try:
                parent = self.environment.get_variable(node.parent)
            except NotInitializedVariableAccessError:
                NotInitializedVariableAccessError(node.position, node.parent, node.name)

            parent = self.get_last_result()
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
            # else:
            #     raise TypeError("Unsupported node type")

    # def visit_indexed_item(self, node: IndexedItem):
    #     ...
    #     # sprawdzić czy iterable
    #     # sprawdzić długość i czy indeks jest w range
    #     # last_result ma to, co jest pod danym indeksem

    def visit_conditional_statement(self, node: ConditionalStatement):

        node.expression.accept(self)
        condition_evaluation = self.get_last_result()
        # TODO: if, ze sprawdzeniem, czy jest to wartość boolowska bądź null
        if condition_evaluation.value:
            # self.environment.enter_block()
            node.if_block.accept(self)
            # self.environment.exit_block()
            if node.else_block:
                # self.environment.enter_block()
                node.else_block.accept(self)
                # self.environment.exit_block()

    def visit_for_statement(self, node: ForStatement):

        node.iterable.accept(self)
        iterable = self.get_last_result()
        node.iterator.accept(self)
        if isinstance(iterable, list):
            for _ in iterable:  # czy tu potrzebny jest iterable?
                # self.environment.enter_block()
                node.execution_block.accept(self)
                # self.environment.exit_block()
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

    # * działa
    def visit_variable_declaration(self, node: VariableDeclaration):

        value = Value(None, node.type)
        self.set_last_result(value)  # czy to dobrze?
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
    # *działa
    def visit_or_expression(self, node: OrExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        # left_value = self.environment.get_variable(left_term)
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, bool) and isinstance(right_term.value, bool):
            self.set_last_result(Value(left_term.value or right_term.value, AstType.TYPE_BOOL))
        else:
            raise OrExpressionError(node.position, left_term.value, right_term.value)

    # *działa
    def visit_and_expression(self, node: AndExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, bool) and isinstance(right_term.value, bool):
            self.set_last_result(Value(left_term.value and right_term.value, AstType.TYPE_BOOL))
        else:
            raise AndExpressionError(node.position, left_term.value, right_term.value)

    # * działa
    def visit_equal_expression(self, node: EqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value == right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))

    # * działa
    def visit_not_equal_expression(self, node: NotEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        self.set_last_result(Value(False, AstType.TYPE_BOOL)) if left_term.value == right_term.value else self.set_last_result(Value(True, AstType.TYPE_BOOL))

    # TODO: refactor expressions aby było bardziej wydajne
    # * działa
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

    # * działa
    def visit_greater_than_or_equal_expression(self, node: GreaterThanOrEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value >= right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise GreaterThanOrEqualExpressionError(node.position, left_term.value, right_term.value)

    # * działa
    def visit_less_than_expression(self, node: LessThanExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value < right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise LessThanExpressionError(node.position, left_term.value, right_term.value)

    # * działa
    def visit_less_than_or_equal_expression(self, node: LessThanOrEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            self.set_last_result(Value(True, AstType.TYPE_BOOL)) if left_term.value <= right_term.value else self.set_last_result(Value(False, AstType.TYPE_BOOL))
        else:
            raise LessThanOrEqualExpressionError(node.position, left_term.value, right_term.value)

    # * działa
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

    # * działa
    def visit_plus_expression(self, node: PlusExpression):  # TODO: dodanie możliwości agregowania stringów (bądź str + float/int)
        node.left_term.accept(self)  # Value
        left_term = self.get_last_result()
        node.right_term.accept(self)  # Value
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            result_value = left_term.value + right_term.value
            if isinstance(left_term.value, int) and isinstance(right_term.value, int): # czy automatycznie zamieniać na int w takiej sytuacji 5.5 + 6.5 = 12 (czy 12.0)
                result_type = AstType.TYPE_INT
            else:
                result_type = AstType.TYPE_FLOAT
            self.set_last_result(Value(result_value, result_type))
        else:
            raise AdditionExpressionError(node.position, left_term.value, right_term.value)

    # * działa
    def visit_division_expression(self, node: DivisionExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term.value, (int, float)) and isinstance(right_term.value, (int, float)):
            if right_term.value == 0:
                raise DivisionByZeroError(node.position, left_term)
            result_value = left_term.value / right_term.value
            if isinstance(left_term.value, int) and isinstance(right_term.value, int):
                result_type = AstType.TYPE_INT
            else:
                result_type = AstType.TYPE_FLOAT
            self.set_last_result(Value(result_value, result_type))
        else:
            raise DivisionExpressionError(node.position, left_term.value, right_term.value)

    # * działa
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
    OTHER
    """

    """
    TERMS
    """

    # * działa
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
            # value.set_value(Value(negated_value, value.type))
            self.set_last_result(Value(negated_value, value.type))
        else:
            raise NegatedTermError(node.position, value)

    # * działa
    def visit_casted_term(self, node: CastedTerm):
        TYPE_CONVERSIONS = {
                (AstType.TYPE_INT, AstType.TYPE_FLOAT): lambda x: float(x),
                (AstType.TYPE_FLOAT, AstType.TYPE_INT): lambda x: int(x) if x.is_integer() else None,
                (AstType.TYPE_INT, AstType.TYPE_STR): lambda x: str(x),
                (AstType.TYPE_STR, AstType.TYPE_INT): lambda x: int(x) if x.is_integer() else None,
                (AstType.TYPE_STR, AstType.TYPE_FLOAT): lambda x: float(x) if x.replace('.', '', 1).isdigit() and x.count('.') <= 1 else None,
                (AstType.TYPE_FLOAT, AstType.TYPE_STR): lambda x: str(x),
                (AstType.TYPE_BOOL, AstType.TYPE_STR): lambda x: str(x),
                (AstType.TYPE_STR, AstType.TYPE_BOOL): lambda x: bool({"true": 1, "false": 0}.get(x)),
                (AstType.TYPE_INT, AstType.TYPE_BOOL): lambda x: bool(x) if x in {0, 1} else None
            }
        node.term.accept(self)  # jak to mądrze zrobić?
        term = self.get_last_result()
        type_conversion = TYPE_CONVERSIONS.get((term.type, node.casted_type))
        if type_conversion is not None:
            self.set_last_result(Value(type_conversion(term.value), node.casted_type))
        else:
            raise CastingTypeError(node.position, term, term.type, node.casted_type)

    """
    LITERALS
    """
    # * działa
    def visit_str_literal(self, node: StrLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_STR))

    # * działa
    def visit_int_literal(self, node: IntLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_INT))

    # * działa
    def visit_float_literal(self, node: FloatLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_FLOAT))

    # * działa
    def visit_bool_literal(self, node: BoolLiteral):
        self.set_last_result(Value(node.term, AstType.TYPE_BOOL))
