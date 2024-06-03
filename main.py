import argparse
# import sys
from src.ast_tree.program import Program
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.source.source import Source
from src.visitor.printer import Printer
from src.visitor.interpreter import Interpreter


def parse_cmdline_parameters(arguments):
    cmdline_parser = argparse.ArgumentParser(prog='Aspecto',
                                             description="General purpose language enhanced with aspect functionality.",
                                             epilog="Copyright (c) 2024, Małgorzata Kozłowska")
    cmdline_parser.add_argument("input_file", type=str, help=" file to execute")
    cmdline_parser.add_argument("-p", "--print", action="store_true", help="print program structure")
    cmdline_parser.add_argument("-a", "--arguments", type=str, help="arguments for program")
    cmdline_parser.add_argument("-fun", "--function", type=str, help="function to execute")
    args = cmdline_parser.parse_args(arguments[1:])
    if not args.function and args.arguments:
        cmdline_parser.error("Arguments can only be used with function. Use -fun or --function to provide the function to execute.")
    return args


def print_program_structure(program: Program):
    printer = Printer()
    program.accept(printer)


def main(arguments_to_parse):
    args = parse_cmdline_parameters(arguments_to_parse)
    with open(args.input_file, "r", encoding="utf-8") as file_handler:
        source = Source(file_handler)
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program(args.input_file)
        if args.print:
            print_program_structure(program)
        interpreter = Interpreter(program, args.function, args.arguments)
        interpreter.visit_program(program)


if __name__ == "__main__":
    main(["main.py", "program.txt", "-p"])
