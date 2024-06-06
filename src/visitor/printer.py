from src.visitor.visitor import Visitor
from src.ast_tree.identifier import Identifier
from src.ast_tree.function_call import FunctionCall
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

    from src.ast_tree.function_definition import FunctionDefinition
    from src.ast_tree.greater_than_expression import GreaterThanExpression
    from src.ast_tree.greater_than_or_equal_expression import GreaterThanOrEqualExpression

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


class Printer(Visitor):
    def __init__(self) -> None:
        self.depth = 0

    def _show_node(self, node_representation: str = None) -> None:
        print("--->" * self.depth + node_representation, end="\n")

    def visit_program(self, node: "Program"):
        program_label = "Program " + node.name if node.name is not None else "Program"
        self._show_node(program_label)
        self.depth += 1
        for function in node.functions.keys():
            node.functions[function].accept(self)
        for aspect in node.aspects.keys():
            node.aspects[aspect].accept(self)
        for statement in node.statements:
            statement.accept(self)
        self.depth -= 1

    def visit_aspect_definition(self, node: "AspectDefinition"):
        self._show_node("AspectDefinition " + str(node.position) + " " + node.name)
        self.depth += 1
        self._show_node("Aspect trigger " + str(node.target) + " " + str(node.event) + " " + str(node.regular_expression))
        node.block.accept(self)
        self.depth -= 1

    def visit_function_definition(self, node: "FunctionDefinition"):
        self._show_node("FunctionDefinition " + str(node.position) + " " + node.name)
        for parameter in node.params:
            parameter.accept(self)
        self.depth += 1
        node.block.accept(self)
        self.depth -= 1
        print(node.return_type)

    def visit_identifier(self, node: "Identifier"):
        self._show_node("Identifier " + str(node.position) + " " + node.name)
        node.parent.accept(self) if node.parent else None

    def visit_function_call(self, node: "FunctionCall"):
        self._show_node("FunctionCall " + str(node.position) + " " + node.name)
        self.depth += 1
        for argument in node.arguments:
            argument.accept(self)
        self.depth -= 1
        node.parent.accept(self) if node.parent else None

    def visit_statements_block(self, node: "StatementsBlock"):
        self._show_node("StatementsBlock: " + str(node.position))
        self.depth += 1
        for statement in node.statements:
            statement.accept(self)
        self.depth -= 1

    def visit_assignment_statement(self, node: "AssignmentStatement"):
        self._show_node("AssignmentStatement: " + str(node.position))
        self.depth += 1
        node.expression.accept(self)
        node.object_access.accept(self)
        self.depth -= 1

    def visit_object_access(self, node):
        if isinstance(node, Identifier):
            self.visit_identifier(node)
        elif isinstance(node, FunctionCall):
            self.visit_function_call(node)
        else:
            pass

    def visit_conditional_statement(self, node: "ConditionalStatement"):
        self._show_node("ConditionalStatement: " + str(node.position))
        self.depth += 1
        node.expression.accept(self)
        node.if_block.accept(self)
        if node.else_block:
            node.else_block.accept(self)
        self.depth -= 1

    def visit_for_statement(self, node: "ForStatement"):
        self._show_node("ForStatement: " + str(node.position))
        self.depth += 1
        node.iterator.accept(self)
        node.iterable.accept(self)
        node.execution_block.accept(self)
        self.depth -= 1

    def visit_while_statement(self, node: "WhileStatement"):
        self._show_node("WhileStatement: " + str(node.position))
        self.depth += 1
        node.condition.accept(self)
        node.execution_block.accept(self)
        self.depth -= 1

    def visit_variable_declaration(self, node: "VariableDeclaration"):
        self.depth += 1
        self._show_node("VariableDeclaration " + str(node.position) + " " + node.name + " : " + str(node.type))
        self.depth -= 1

    def visit_return_statement(self, node: "ReturnStatement"):
        self._show_node("ReturnStatement: " + str(node.position))
        self.depth += 1
        self._show_node(str(node.expression))
        self.depth -= 1

    def visit_or_expression(self, node: "OrExpression"):
        self._show_node("OrExpression: " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_and_expression(self, node: "AndExpression"):
        self._show_node("AndExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_equal_expression(self, node: "EqualExpression"):
        self._show_node("EqualExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_not_equal_expression(self, node: "NotEqualExpression"):
        self._show_node("NotEqualExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_greater_than_expression(self, node: "GreaterThanExpression"):
        self._show_node("GreaterThanExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_greater_than_or_equal_expression(self, node: "GreaterThanOrEqualExpression"):
        self._show_node("GreaterThanOrEqualExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_less_than_expression(self, node: "LessThanExpression"):
        self._show_node("LessThanExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_less_than_or_equal_expression(self, node: "LessThanOrEqualExpression"):
        self._show_node("LessThanOrEqualExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_minus_expression(self, node: "MinusExpression"):
        self._show_node("MinusExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_plus_expression(self, node: "PlusExpression"):
        self._show_node("PlusExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_division_expression(self, node: "DivisionExpression"):
        self._show_node("DivisionExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_multiplication_expression(self, node: "MultiplicationExpression"):
        self._show_node("MultiplicationExpression " + str(node.position))
        self.depth += 1
        node.left_term.accept(self)
        node.right_term.accept(self)
        self.depth -= 1

    def visit_unary_term(self, node: "UnaryTerm"):
        self._show_node("UnaryTerm " + str(node.position))
        self.depth += 1
        node.term.accept(self)
        self.depth -= 1

    def visit_casted_term(self, node: "CastedTerm"):
        self._show_node("CastedTerm: " + str(node.position))
        self.depth += 1
        node.term.accept(self)
        self.depth -= 1
        print(str(node.casted_type))

    def visit_str_literal(self, node: "StrLiteral"):
        self.depth += 1        
        self._show_node("StrLiteral " + node.term)
        self.depth -= 1

    def visit_int_literal(self, node: "IntLiteral"):
        self.depth += 1
        self._show_node("IntLiteral " + str(node.term))
        self.depth -= 1

    def visit_float_literal(self, node: "FloatLiteral"):
        self.depth += 1
        self._show_node("FloatLiteral " + str(node.term))
        self.depth -= 1

    def visit_bool_literal(self, node: "BoolLiteral"):
        self.depth += 1
        self._show_node("BoolLiteral " + str(node.term))
        self.depth -= 1
