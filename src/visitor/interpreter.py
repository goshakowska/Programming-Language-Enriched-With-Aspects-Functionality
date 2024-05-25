from visitor.visitor import Visitor

from ast_tree.and_expression import AndExpression
from ast_tree.aspect_definition import AspectDefinition
from ast_tree.assignment_statement import AssignmentStatement
from ast_tree.bool_literal import BoolLiteral
from ast_tree.casted_term import CastedTerm
from ast_tree.conditional_statement import ConditionalStatement
from ast_tree.division_expression import DivisionExpression
from ast_tree.equal_expression import EqualExpression
from ast_tree.float_literal import FloatLiteral
from ast_tree.for_statement import ForStatement
from ast_tree.function_call import FunctionCall
from ast_tree.function_definition import FunctionDefinition
from ast_tree.greater_than_expression import GreaterThanExpression
from ast_tree.greater_than_or_equal_expression import GreaterThanOrEqualExpression
from ast_tree.identifier import Identifier
from ast_tree.indexed_item import IndexedItem
from ast_tree.int_literal import IntLiteral
from ast_tree.less_than_expression import LessThanExpression
from ast_tree.less_than_or_equal_expression import LessThanOrEqualExpression
from ast_tree.minus_expression import MinusExpression
from ast_tree.multiplication_expression import MultiplicationExpression
from ast_tree.node import Node
from ast_tree.not_equal_expression import NotEqualExpression
from ast_tree.object_access import ObjectAccess
from ast_tree.or_expression import OrExpression
from ast_tree.plus_expression import PlusExpression
from ast_tree.program import Program
from ast_tree.return_statement import ReturnStatement
from ast_tree.statements_block import StatementsBlock
from ast_tree.str_literal import StrLiteral
from ast_tree.unary_term import UnaryTerm
from ast_tree.variable_declaration import VariableDeclaration
from ast_tree.while_statement import WhileStatement
'''
Interpreter(Visitor):

self.last_result = None


'''


class Interpreter(Visitor):

    def visit_and_expression(self, node: AndExpression):
        pass

    def visit_aspect_definition(self, node: AspectDefinition):
        pass

    def visit_assignment_statement(self, node: AssignmentStatement):
        pass

    def visit_bool_literal(self, node: BoolLiteral):
        pass

    def visit_casted_term(self, node: CastedTerm):
        pass

    def visit_conditional_statement(self, node: ConditionalStatement):
        pass

    def visit_division_expression(self, node: DivisionExpression):
        pass

    def visit_equal_expression(self, node: EqualExpression):
        pass

    def visit_float_literal(self, node: FloatLiteral):
        pass

    def visit_for_statement(self, node: ForStatement):
        pass

    def visit_function_call(self, node: FunctionCall):
        pass

    def visit_function_definition(self, node: FunctionDefinition):
        pass

    def visit_greater_than_expression(self, node: GreaterThanExpression):
        pass

    def visit_greater_than_or_equal_expression(self, node: GreaterThanOrEqualExpression):
        pass

    def visit_identifier(self, node: Identifier):
        pass

    def visit_indexed_item(self, node: IndexedItem):
        pass

    def visit_int_literal(self, node: IntLiteral):
        pass

    def visit_less_than_expression(self, node: LessThanExpression):
        pass

    def visit_less_than_or_equal_expression(self, node: LessThanOrEqualExpression):
        pass

    def visit_minus_expression(self, node: MinusExpression):
        pass

    def visit_multiplication_expression(self, node: MultiplicationExpression):
        pass

    def visit_node(self, node: Node):  # TODO: Czy jest to potrzebne?
        pass

    def visit_not_equal_expression(self, node: NotEqualExpression):
        pass

    def visit_object_access(self, node: ObjectAccess):
        pass

    def visit_or_expression(self, node: OrExpression):
        pass

    def visit_plus_expression(self, node: PlusExpression):
        pass

    def visit_program(self, node: Program):
        pass

    def visit_return_statement(self, node: ReturnStatement):
        pass

    def visit_statements_block(self, node: StatementsBlock):
        pass

    def visit_str_literal(self, node: StrLiteral):
        pass

    def visit_unary_term(self, node: UnaryTerm):
        pass

    def visit_variable_declaration(self, node: VariableDeclaration):
        pass

    def visit_while_statement(self, node: WhileStatement):
        pass
