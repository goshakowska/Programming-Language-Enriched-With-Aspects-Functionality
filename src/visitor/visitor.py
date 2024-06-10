from abc import abstractmethod
import typing
if typing.TYPE_CHECKING:
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


class Visitor:
    # def __init__(self, node: Node) -> None:
    #     pass

    @abstractmethod
    def visit_and_expression(self, node: "AndExpression"):
        pass

    @abstractmethod
    def visit_active_on_start_aspect_definition(self, node: "AspectDefinition"):
        pass

    @abstractmethod
    def visit_active_on_end_aspect_definition(self, node: "AspectDefinition"):
        pass

    @abstractmethod
    def visit_active_on_count_aspect_definition(self, node: "AspectDefinition"):
        pass

    @abstractmethod
    def visit_assignment_statement(self, node: "AssignmentStatement"):
        pass

    @abstractmethod
    def visit_bool_literal(self, node: "BoolLiteral"):
        pass

    @abstractmethod
    def visit_casted_term(self, node: "CastedTerm"):
        pass

    @abstractmethod
    def visit_conditional_statement(self, node: "ConditionalStatement"):
        pass

    @abstractmethod
    def visit_division_expression(self, node: "DivisionExpression"):
        pass

    @abstractmethod
    def visit_equal_expression(self, node: "EqualExpression"):
        pass

    @abstractmethod
    def visit_float_literal(self, node: "FloatLiteral"):
        pass

    @abstractmethod
    def visit_for_statement(self, node: "ForStatement"):
        pass

    @abstractmethod
    def visit_function_call(self, node: "FunctionCall"):
        pass

    @abstractmethod
    def visit_function_definition(self, node: "FunctionDefinition"):
        pass

    @abstractmethod
    def visit_greater_than_expression(self, node: "GreaterThanExpression"):
        pass

    @abstractmethod
    def visit_greater_than_or_equal_expression(self, node: "GreaterThanOrEqualExpression"):
        pass

    @abstractmethod
    def visit_identifier(self, node: "Identifier"):
        pass

    @abstractmethod
    def visit_indexed_item(self, node: "IndexedItem"):
        pass

    @abstractmethod
    def visit_int_literal(self, node: "IntLiteral"):
        pass

    @abstractmethod
    def visit_less_than_expression(self, node: "LessThanExpression"):
        pass

    @abstractmethod
    def visit_less_than_or_equal_expression(self, node: "LessThanOrEqualExpression"):
        pass

    @abstractmethod
    def visit_minus_expression(self, node: "MinusExpression"):
        pass

    @abstractmethod
    def visit_multiplication_expression(self, node: "MultiplicationExpression"):
        pass

    @abstractmethod
    def visit_node(self, node: "Node"):  # TODO: Czy jest to potrzebne?
        pass

    @abstractmethod
    def visit_not_equal_expression(self, node: "NotEqualExpression"):
        pass

    # @abstractmethod
    # def visit_object_access(self, node: "ObjectAccess"):
    #     pass

    @abstractmethod
    def visit_or_expression(self, node: "OrExpression"):
        pass

    @abstractmethod
    def visit_plus_expression(self, node: "PlusExpression"):
        pass

    @abstractmethod
    def visit_program(self, node: "Program"):
        pass

    @abstractmethod
    def visit_return_statement(self, node: "ReturnStatement"):
        pass

    @abstractmethod
    def visit_statements_block(self, node: "StatementsBlock"):
        pass

    @abstractmethod
    def visit_str_literal(self, node: "StrLiteral"):
        pass

    @abstractmethod
    def visit_unary_term(self, node: "UnaryTerm"):
        pass

    @abstractmethod
    def visit_variable_declaration(self, node: "VariableDeclaration"):
        pass

    @abstractmethod
    def visit_while_statement(self, node: "WhileStatement"):
        pass
