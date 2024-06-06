
from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.source.source import Source
from src.ast_tree.ast_type import AstType

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

from src.visitor.printer import Printer


def create_parser_with_given_lexer_and_source(file_handler):
    return Parser(Lexer(Source(file_handler)))


def get_program(input_file_name):
    file_handler = open(input_file_name, "r", encoding="utf-8")
    parser = create_parser_with_given_lexer_and_source(file_handler)
    return parser.parse_program(input_file_name)


def test_parser_assignment_program():
    assignment_program = get_program("test/test_files/assignment.txt")
    printer = Printer()
    assignment_program.accept(printer)
    expected_program = Program(
        "test/test_files/assignment.txt",
        {},
        {},
        [
            AssignmentStatement(
                (1, 11),
                                IntLiteral(
                    (1, 13),
                    6
                ),
                VariableDeclaration(
                    (1, 1),
                    "myInt",
                    AstType.TYPE_INT
                )

            )
        ]
    )

    assert assignment_program == expected_program


def test_parser_casted_term_program():
    casted_term_program = get_program("test/test_files/casted_term.txt")
    printer = Printer()
    casted_term_program.accept(printer)
    expected_program = Program(
        "test/test_files/casted_term.txt",
        {},
        {},
        [
            AssignmentStatement(
                (1, 15),
                CastedTerm(
                    (1, 21),
                    FloatLiteral(
                        (1, 21),
                        6.1
                    ),
                    AstType.TYPE_INT
                ),
                VariableDeclaration(
                    (1, 1),
                    "myFloat",
                    AstType.TYPE_FLOAT
                )
            )
        ]
    )
    assert casted_term_program == expected_program



def test_parser_unary_term_program():
    and_expression_program = get_program("test/test_files/and_expression.txt")
    printer = Printer()
    and_expression_program.accept(printer)
    expected_program = Program(
        "test/test_files/and_expression.txt",
        {},
        {},
        [
            AssignmentStatement(
                (1, 13),
                AndExpression(
                    (1, 21),
                    LessThanExpression(
                        (1, 17),
                        IntLiteral((1, 15), 5),
                        IntLiteral((1, 19), 6)
                    ),
                    LessThanExpression(
                        (1, 26),
                        IntLiteral((1, 24), 6),
                        IntLiteral((1, 28), 7)
                    )
                ),
                VariableDeclaration(
                    (1, 1),
                    "myBool",
                    AstType.TYPE_BOOL
                )
            )
        ]
    )
    assert and_expression_program == expected_program


def test_parser_function_declaration_program():
    function_declaration_program = get_program("test/test_files/function_definition.txt")
    printer = Printer()
    function_declaration_program.accept(printer)
    expected_program = Program(
        "test/test_files/function_definition.txt",
        {
            "myFunc": FunctionDefinition(
                (2, 1),
                'myFunc',
                [
                    VariableDeclaration(
                        (2, 13),
                        'intParam',
                        AstType.TYPE_INT
                    )
                ],
                StatementsBlock(
                    (3, 1),
                    [
                        AssignmentStatement(
                            (4, 19),
                            MultiplicationExpression(
                                (4, 30),
                                Identifier(
                                    (4, 21),
                                    "intParam",
                                    None
                                ),
                                IntLiteral(
                                    (4, 32),
                                    2
                                ),
                            ),
                            VariableDeclaration(
                                (4, 5),
                                'outputInt',
                                AstType.TYPE_INT
                            )
                        ),
                        ReturnStatement(
                            (5, 5),
                            Identifier(
                                (5, 12),
                                'outputInt',
                                None
                            ),
                        )
                    ]
                ),
                AstType.TYPE_INT,
            )
        },
        {},
        [
            AssignmentStatement(
                (1, 11),
                IntLiteral(
                    (1, 13),
                    6
                ),
                VariableDeclaration(
                    (1, 1),
                    'myInt',
                    AstType.TYPE_INT
                ),
            )
        ]
    )
    assert function_declaration_program == expected_program


def test_parser_from_source_file_simple_program():
    program = get_program("test/test_files/and_expression.txt")
    printer = Printer()
    program.accept(printer)
    expected_program = Program(
        "test/test_files/and_expression.txt",
        {},
        {},
        [
            AssignmentStatement(
                (1, 13),
                AndExpression(
                    (1, 21),
                    LessThanExpression(
                        (1, 17),
                        IntLiteral((1, 15), 5),
                        IntLiteral((1, 19), 6)
                    ),
                    LessThanExpression(
                        (1, 26),
                        IntLiteral((1, 24), 6),
                        IntLiteral((1, 28), 7)
                    )
                ),
                VariableDeclaration(
                    (1, 1),
                    "myBool",
                    AstType.TYPE_BOOL
                )
            )
        ]
    )
    assert program == expected_program



def test_parser_from_source_file_aspect_definition(): #* sprawdzane jest tu również tworzenie Identifier, StatementsBlock, ReturnStatement
    program = get_program("test/test_files/aspect_definition.txt")
    printer = Printer()
    program.accept(printer)
    assert program.name == "test/test_files/aspect_definition.txt"
    expected_program = Program(
        "test/test_files/aspect_definition.txt",
        {},
        {
            "logParams": AspectDefinition(
                (1, 1),
                'logParams',
                AstType.TYPE_FUNCTION,
                AstType.ASPECT_ON_START,
                Identifier((1, 38), 'write', None),
                StatementsBlock(
                    (1, 44),
                    [
                        AssignmentStatement(
                            (2, 17),
                            IntLiteral((2, 19), 1),
                            VariableDeclaration((2, 5), "counter", AstType.TYPE_INT)
                        ),
                        ReturnStatement(
                            (3, 5),
                            Identifier((3, 12), "counter", None)
                        )
                    ]
                )
            )
        },
        []
    )
    assert program == expected_program


def test_parser_and_expression():  # * sprawdzane jest tu również tworzenie AssignmentStatement, VariableDeclaration, AndExpression, LessThanExpression, IntLiteral
    program = get_program("test/test_files/and_expression.txt")
    printer = Printer()
    program.accept(printer)
    expected_program = Program(
        "test/test_files/and_expression.txt",
        {},
        {},
        [
            AssignmentStatement(
                (1, 13),
                AndExpression(
                    (1, 21),
                    LessThanExpression(
                        (1, 17),
                        IntLiteral((1, 15), 5),
                        IntLiteral((1, 19), 6)
                    ),
                    LessThanExpression(
                        (1, 26),
                        IntLiteral((1, 24), 6),
                        IntLiteral((1, 28), 7)
                    )
                ),
                VariableDeclaration(
                    (1, 1),
                    "myBool",
                    AstType.TYPE_BOOL
                )
            )
        ]
    )
    assert program == expected_program
