import io

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.source.source import Source
from src.ast_tree.ast_type import AstType

from src.ast_tree.function_definiton import FunctionDefinition
from src.ast_tree.aspect_definition import AspectDefinition
from src.ast_tree.identifier import Identifier

from src.ast_tree.variable_declaration import VariableDeclaration

from src.ast_tree.return_statement import ReturnStatement
from src.ast_tree.assignment_statement import AssignmentStatement
from src.ast_tree.statements_block import StatementsBlock
from src.ast_tree.int_literal import IntLiteral
from src.ast_tree.multiplication_expression import MultiplicationExpression

from src.ast_tree.program import Program


def create_parser_with_given_lexer_and_source(string):
    return Parser(Lexer(Source(io.StringIO(string))))


def get_program(input_file_name):
    file_handler = open(input_file_name, "r", encoding="utf-8")
    parser = create_parser_with_given_lexer_and_source(file_handler.read())
    return parser.parse_program(input_file_name)


def test_parser_assignment_program():
    assignment_program = get_program("test/test_files/assignment.txt")
    assert assignment_program.name == "test/test_files/assignment.txt"
    assert assignment_program.type == AstType.PROGRAM
    assert len(assignment_program.functions) == 0
    assert len(assignment_program.aspects) == 0
    assert len(assignment_program.statements) == 1
    assert assignment_program.statements[0].type ==\
        AstType.ASSIGNMENT_STATEMENT
    assert assignment_program.statements[0].expression.name == "myInt"
    assert assignment_program.statements[0].expression.type == AstType.INT_TYPE
    assert assignment_program.statements[0].object_access.type == AstType.INT
    assert assignment_program.statements[0].object_access.term == 6


def test_parser_casted_term_program():
    casted_term_program = get_program("test/test_files/casted_term.txt")
    assert casted_term_program.name == "test/test_files/casted_term.txt"
    assert casted_term_program.type == AstType.PROGRAM
    assert len(casted_term_program.functions) == 0
    assert len(casted_term_program.aspects) == 0
    assert len(casted_term_program.statements) == 1
    assert casted_term_program.statements[0].type ==\
        AstType.ASSIGNMENT_STATEMENT
    assert casted_term_program.statements[0].expression.name == "myFloat"
    assert casted_term_program.statements[0].expression.type == AstType.FLOAT_TYPE
    assert casted_term_program.statements[0].object_access.type == AstType.CASTED_TERM
    casted_term = casted_term_program.statements[0].object_access
    assert casted_term.casted_type == AstType.INT_TYPE
    literal = casted_term.term
    assert literal.type == AstType.FLOAT
    assert literal.term == 6.1


def test_parser_unary_term_program():
    parser = create_parser_with_given_lexer_and_source("int myInt = -6;")
    unary_term_program = parser.parse_program("unary_term_program.asp")
    assert unary_term_program.name == "unary_term_program.asp"
    assert unary_term_program.type == AstType.PROGRAM
    assert len(unary_term_program.functions) == 0
    assert len(unary_term_program.aspects) == 0
    assert len(unary_term_program.statements) == 1
    assert unary_term_program.statements[0].type == AstType.ASSIGNMENT_STATEMENT
    assert unary_term_program.statements[0].expression.name == "myInt"
    assert unary_term_program.statements[0].expression.type == AstType.INT_TYPE
    assert unary_term_program.statements[0].object_access.type == AstType.UNARY_TERM
    unary_term = unary_term_program.statements[0].object_access
    assert unary_term.term.type == AstType.INT
    assert unary_term.term.term == 6


def test_parser_function_declaration_program():
    parser = create_parser_with_given_lexer_and_source("int myInt = 6;\nfunc myFunc(int intParam) : int\n{\n int outputInt = 6*2;\n return outputInt;\n}\n")
    function_declaration_program = parser.parse_program("function_declaration.asp")
    expected_program = Program("function_declaration.asp",
                               [
                                 FunctionDefinition(
                                     (2, 1),
                                     'myFunc',
                                     [
                                         VariableDeclaration(
                                          (2, 13),
                                          'intParam',
                                          AstType.INT_TYPE)
                                     ],
                                     StatementsBlock(
                                         (3, 1),
                                         [
                                             AssignmentStatement(
                                                 (4, 16),
                                                 VariableDeclaration(
                                                     (4, 2),
                                                     'outputInt',
                                                     AstType.INT_TYPE
                                                 ),
                                                 MultiplicationExpression(
                                                     (4, 19),
                                                     IntLiteral(
                                                         (4, 18),
                                                         6
                                                     ),
                                                     IntLiteral(
                                                         (4, 20),
                                                         2
                                                     ),
                                                 )
                                             ),
                                             ReturnStatement(
                                                 (5, 2),
                                                 Identifier(
                                                     (5, 9),
                                                     'outputInt'),
                                             )
                                         ]
                                     ),
                                     AstType.INT_TYPE,
                                 )
                               ],
                               [

                               ],
                               [
                                 AssignmentStatement(
                                     (1, 11),
                                     VariableDeclaration(
                                         (1, 1),
                                         'myInt',
                                         AstType.INT_TYPE
                                        ),
                                     IntLiteral(
                                            (1, 13),
                                            6
                                        )
                                    )
                                ])
    assert function_declaration_program == expected_program


def test_parser_from_source_file_simple_program():
    program = get_program("test/test_files/assignment.txt")
    assert program.name == "test/test_files/assignment.txt"
    assert program.type == AstType.PROGRAM
    assert len(program.functions) == 0
    assert len(program.aspects) == 0
    assert len(program.statements) == 1
    assert program.statements[0].type == AstType.ASSIGNMENT_STATEMENT
    assert program.statements[0].expression.name == "myInt"
    assert program.statements[0].expression.type == AstType.INT_TYPE
    assert program.statements[0].object_access.type == AstType.INT
    assert program.statements[0].object_access.term == 6


def test_parser_from_source_file_aspect_declaration():
    # parser = create_parser_with_given_lexer_and_source("aspect logParams: on func start like write {\n int counter = 1; \n  return counter;  \n}")
    # program = parser.parse_program("aspect_declaration.asp")
    program = get_program("test/test_files/aspect_definition.txt")
    assert program.name == "test/test_files/aspect_definition.txt"
    expected_program = Program("test/test_files/aspect_definition.txt",
                               [],
                               [
                                   AspectDefinition(
                                       (1, 1),
                                       'logParams',
                                       AstType.FUNCTION,
                                       AstType.ASPECT_ON_START,
                                       Identifier((1, 38),
                                                  'write'),
                                       StatementsBlock((1, 44),
                                                       [
                                                        AssignmentStatement(
                                                            (2, 14),
                                                            VariableDeclaration(
                                                                (2, 2),
                                                                "counter",
                                                                AstType.INT_TYPE
                                                            ),
                                                            IntLiteral((2, 16),
                                                                       1)
                                                        ),
                                                        ReturnStatement(
                                                            (3, 3),
                                                            Identifier((3, 10),
                                                                       "counter")
                                                        )
                                                       ])),
                               ],
                               []
                               )
    assert program == expected_program
