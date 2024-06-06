import io
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.source.source import Source
from src.visitor.interpreter import Interpreter
from src.visitor.interpreter_errors import DivisionByZeroError, CastingTypeError, NegatedTermError
import pytest


def create_parser_with_given_lexer_and_source(file_handler):
    return Parser(Lexer(Source(file_handler)))


def get_interpreter(input_file_name):
    with open(input_file_name, "r", encoding="utf-8") as file_handler:
        parser = create_parser_with_given_lexer_and_source(file_handler)
        program = parser.parse_program()
        interpreter = Interpreter(program)
        return interpreter, program


def test_interpreter_output(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/while_function.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()

    assert captured.out == "0\n1\n2\n3\n4\n"


def test_addition(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/math/addition.txt")
    interpreter.visit_program(program)

    captured = capsys.readouterr()
    assert captured.out == "5\n"


def test_string_concatenation(capsys):

    interpreter, program = get_interpreter("test/test_files_interpreter/math/string_concatenation.txt")
    interpreter.visit_program(program)

    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"


def test_subtraction(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/math/subtraction.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "3\n"


def test_multiplication(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/math/multiplication.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "12\n"


def test_division(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/math/division.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "5\n"


def test_division_by_zero_handling(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/math/division_by_zero.txt")
    with pytest.raises(DivisionByZeroError):
        interpreter.visit_program(program)


def test_or_expression(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/or_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_and_expression(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/and_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "false\n"


def test_equal_expression(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/equal_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_not_equal_expression(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/not_equal_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_greater_than_expression(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/greater_than_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_less_than_expression(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/less_than_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_greater_than_or_equal(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/greater_than_or_equal.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\nfalse\ntrue\n"


def test_less_than_or_equal(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/less_than_or_equal.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\nfalse\ntrue\n"


def test_compound_relational_with_variables(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/expressions/compound_expression.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\ntrue\ntrue\nfalse\n"


def test_cast_int_to_float(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/int_to_float.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "10.0\n"


def test_cast_float_to_int(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/float_to_int.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "5\n"


def test_cast_int_to_str(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/int_to_str.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "10\n"


def test_cast_str_to_int(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/str_to_int.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "123\n"


def test_cast_str_to_float(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/str_to_float.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "123.45\n"


def test_cast_float_to_str(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/float_to_str.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "123.45\n"


def test_cast_bool_to_str(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/bool_to_str.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_cast_str_to_bool(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/str_to_bool.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_cast_int_to_bool(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/int_to_bool.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_invalid_cast_str_to_int(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/invalid_str_to_int.txt")
    with pytest.raises(CastingTypeError):
        interpreter.visit_program(program)


def test_invalid_cast_str_to_float(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/cast/invalid_str_to_float.txt")
    with pytest.raises(CastingTypeError):
        interpreter.visit_program(program)


def test_negate_int(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/unary/negate_int.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "-10\n"


def test_negate_float(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/unary/negate_float.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "12.5\n"


def test_negate_bool_false(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/unary/negate_bool_false.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "true\n"


def test_negate_bool_true(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/unary/negate_bool_true.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "false\n"


def test_negate_invalid_type(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/unary/invalid_negate_str.txt")
    with pytest.raises(NegatedTermError):
        interpreter.visit_program(program)


def test_factorial_recursive(capsys):
    interpreter, program = get_interpreter("test/test_files_interpreter/factorial_recursive.txt")
    interpreter.visit_program(program)
    captured = capsys.readouterr()
    assert captured.out == "120\n"