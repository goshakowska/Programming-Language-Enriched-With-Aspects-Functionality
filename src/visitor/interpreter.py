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

from abc import ABC, abstractmethod

TYPE_CONVERSIONS = {
    (int, float): lambda x: float(x),
    (float, int): lambda x: int(x) if x.is_integer() else None,
    (int, str): lambda x: str(x),
    (float, str): lambda x: str(x),
    (str, bool): lambda x: bool({"true": 1, "false": 0}.get(x)),
    (int, bool): lambda x: bool(x) if x in {0, 1} else None
}


class ScopeContext:
    def __init__(self) -> None:
        self.variables = {}
        # self.parent_context  # ? czy potrzebne?
    
    def add_variable(self, name: str, value) -> None:
        self.variables[name] = value


class CallContext:  # handlery
    def __init__(self, return_type) -> None:
        self._count_nested = 0
        self._return_type = return_type
        self.scopes = []  # ! jako pierwszy scope mają być argumenty wywołania funkcji

    def push_scope(self) -> None:
        self.scopes.append(ScopeContext())

    def pop_scope(self) -> None:
        self.scopes.pop()

    def get_last_scope(self):
        return self.scopes[-1]


class Env:  # TODO: handlery, call_context, globalny_scope
    def __init__(self) -> None:
        self.call_contexts = []

    def push_context(self, call_context: CallContext) -> None:
        self.call_contexts.append(call_context)

    def pop_context(self) -> None:
        self.call_contexts.pop()

    def get_last_context(self) -> CallContext:
        return self.call_contexts[-1]


class Interpreter(Visitor):

    def __init__(self, program: Program, start_function_name: str = "", *args) -> None:
        self.program = program
        self._program_root = start_function_name
        self._last_result = None
        if self.program_root:  # ? czy to jakoś inaczej zrealizować?
            self.input_parameters = list(args)
        # dorzucić embedded functions do programu
        # self._stack = Stack()  # class Env
        # self._global_scope = CallContext()

    def get_last_result(self):
        last_result = self._last_result
        self._last_result = None
        return last_result

    def set_last_result(self, result):
        self._last_result = result  # * ma móc przechowywać listy


    class EmbeddedFunction(ABC):
        # def __init__(self, name: str) -> None:  # ? czy potrzebne?
        #     self._name = name

        def name(self):
            return self._name

        @abstractmethod
        def __call__(self, *args):
            pass
        # print, enabled, count, name

    class PrintFunction(EmbeddedFunction):

        def __call__(self, node: Identifier):
            element_to_print = node.accept(self)
            if isinstance(element_to_print, str):
                print(element_to_print)

    # czy aby na pewno?
    class CountFunction(EmbeddedFunction):  # <nazwa_aspektu>.enabled

        def __call__(self, *args):  # ! args typu param
            return len(args)

    class EnableFunction(EmbeddedFunction):

        def __call__(self, *args):
            return True
    # koniec czy aby na pewno?

    """
    PROGRAM
    """

    def visit_program(self, node: Program):
        """
        1) sprawdzam czy program_root znajduje się w zbiorze nazw funkcji:
            - jeżeli nie, to mamy błąd semantyczny
            - jeżeli tak, to sprawdza czy są argumenty do naszego interpretera
        """
        # env
        if self.program_root and self.program_root in self.program.functions:  # TODO: po nazwie odnaleźć programu
            if self.input_parameters:
                self.set_last_result(self.input_parameters)
            self.program_root.accept(self)

        for statement in node.statements:
            statement.accept(self)

        
        pass

    """
    DEFINITIONS
    """
    def visit_aspect_definition(self, node: AspectDefinition):
        pass

    def visit_function_definition(self, node: FunctionDefinition):
        # jak przekazać argumenty wywołania?
        # porównanie arguments a parametry


    """
    STATEMENTS
    """

    def visit_identifier(self, node: Identifier):
        pass

    def visit_function_call(self, node: FunctionCall):
        function_name = node.name
        if function_name not in self.program.functions:
            pass  # TODO: błąd semantyczny

        function_scope = ScopeContext(self.get_last_result())
        function_call_context = CallContext()
        self._stack.push_context()

        arguments = node.arguments

        for argument in arguments:
            argument.accept(self)
            function_scope.variables = self.get_last_result()
            self.reset_last_result()

    def visit_statements_block(self, node: StatementsBlock):
        for statement in node.statements:
            statement.accept(self)
            ...

    def visit_assignment_statement(self, node: AssignmentStatement):
        pass

    def visit_object_access(self, node: ObjectAccess):
        pass

    def visit_indexed_item(self, node: IndexedItem):
        pass

    def visit_conditional_statement(self, node: ConditionalStatement):
        if_scope = ScopeContext()
        self._stack.push_context(if_scope)

        pass

    def visit_for_statement(self, node: ForStatement):
        pass

    def visit_while_statement(self, node: WhileStatement):
        pass

    def visit_variable_declaration(self, node: VariableDeclaration):
        pass

    def visit_return_statement(self, node: ReturnStatement):
        return_expression = node.expression
        

    """
    EXPRESSIONS
    """
    def visit_or_expression(self, node: OrExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, bool) and isinstance(right_term, bool):
            self.set_last_result(left_term or right_term)
        else:
            raise OrExpressionError(node.position, left_term, right_term)

    def visit_and_expression(self, node: AndExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, bool) and isinstance(right_term, bool):
            self.set_last_result(left_term and right_term)
        else:
            raise AndExpressionError(node.position, left_term, right_term)

    def visit_equal_expression(self, node: EqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        self.set_last_result(True) if left_term == right_term else self.set_last_result(False)

    def visit_not_equal_expression(self, node: NotEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        self.set_last_result(False) if left_term == right_term else self.set_last_result(True)

    def visit_greater_than_expression(self, node: GreaterThanExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(True) if left_term > right_term else self.set_last_result(False)
        else:
            raise GreaterThanExpressionError(node.position, left_term, right_term)

    def visit_greater_than_or_equal_expression(self, node: GreaterThanOrEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(True) if left_term >= right_term else self.set_last_result(False)
        else:
            raise GreaterThanOrEqualExpressionError(node.position, left_term, right_term)

    def visit_less_than_expression(self, node: LessThanExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(True) if left_term < right_term else self.set_last_result(False)
        else:
            raise LessThanExpressionError(node.position, left_term, right_term)

    def visit_less_than_or_equal_expression(self, node: LessThanOrEqualExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(True) if left_term <= right_term else self.set_last_result(False)
        else:
            raise LessThanOrEqualExpressionError(node.position, left_term, right_term)

    def visit_minus_expression(self, node: MinusExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(left_term - right_term)
        else:
            raise SubtractionExpressionError(node.position, left_term, right_term)

    def visit_plus_expression(self, node: PlusExpression):  # TODO: dodanie możliwości agregowania stringów (bądź str + float/int)
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(left_term + right_term)
        else:
            raise AdditionExpressionError(node.position, left_term, right_term)

    def visit_division_expression(self, node: DivisionExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(left_term / right_term)
        else:
            raise DivisionExpressionError(node.position, left_term, right_term)

    def visit_multiplication_expression(self, node: MultiplicationExpression):
        node.left_term.accept(self)
        left_term = self.get_last_result()
        node.right_term.accept(self)
        right_term = self.get_last_result()
        if isinstance(left_term, (int, float)) and isinstance(right_term, (int, float)):
            self.set_last_result(left_term * right_term)
        else:
            raise MultiplicationExpressionError(node.position, left_term, right_term)

    """
    OTHER
    """
    def visit_node(self, node: Node):  # TODO: Czy jest to potrzebne?
        pass

    """
    TERMS
    """
    def visit_unary_term(self, node: UnaryTerm):
        term = node.term.accept(self)
        negation_functions = {
            int: lambda x: -x,
            float: lambda x: -x,
            bool: lambda x: not x
        }
        if negation_conversion := negation_functions.get(type(term)):
            self.set_last_result(negation_conversion(term))
        else:
            raise NegatedTermError(node.position, term)

    def visit_casted_term(self, node: CastedTerm):
        node.term.accept(self)
        term = self.get_last_result()
        node.casted_type.accept(self)
        type_to_cast = self.get_last_result()
        node.casted_type.term.type.accept(self)
        previous_type = self.get_last_result()
        type_conversion = TYPE_CONVERSIONS.get()
        if (previous_type, type_to_cast) in TYPE_CONVERSIONS:
            if (result := type_conversion(term)) is not None:
                self.set_last_result(result)
            else:
                raise CastingTypeError(node.position, term, previous_type, type_to_cast)

    """
    LITERALS
    """
    def visit_str_literal(self, node: StrLiteral):
        self.set_last_result(node.term)

    def visit_int_literal(self, node: IntLiteral):
        self.set_last_result(node.term)

    def visit_float_literal(self, node: FloatLiteral):
        self.set_last_result(node.term)

    def visit_bool_literal(self, node: BoolLiteral):
        self.set_last_result(node.term)
