import io
from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.source.source import Source
from src.ast_tree.ast_type import AstType


def create_parser_with_given_lexer_and_source(string):
    return Parser(Lexer(Source(io.StringIO(string))))


def test_parser_assignment_program():
    parser = create_parser_with_given_lexer_and_source("int myInt = 6;")
    assignment_program = parser.parse_program("assignment_program.asp")
    assert assignment_program.name == "assignment_program.asp"
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
    parser = create_parser_with_given_lexer_and_source("float myFloat = 6.1 as int;")
    casted_term_program = parser.parse_program("object_casted_program.asp")
    assert casted_term_program.name == "object_casted_program.asp"
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
    parser = create_parser_with_given_lexer_and_source("int myInt = -6;")  #TODO!
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
    assert function_declaration_program.name == "function_declaration.asp"
    assert function_declaration_program.type == AstType.PROGRAM
    assert len(function_declaration_program.aspects) == 0
    assert len(function_declaration_program.statements) == 1
    assert function_declaration_program.statements[0].type ==\
        AstType.ASSIGNMENT_STATEMENT
    assert function_declaration_program.statements[0].expression.name == "myInt"
    assert function_declaration_program.statements[0].expression.type == AstType.INT_TYPE
    assert function_declaration_program.statements[0].object_access.type == AstType.INT
    assert function_declaration_program.statements[0].object_access.term == 6
