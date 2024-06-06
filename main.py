import sys
import argparse
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
    cmdline_parser.add_argument("input_file", type=str, help="File to execute")
    cmdline_parser.add_argument("-p", "--print", action="store_true", help="Print program structure")
    args = cmdline_parser.parse_args(arguments[1:])
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
        interpreter = Interpreter(program)
        interpreter.visit_program(program)


if __name__ == "__main__":
     main(["main.py", "program.txt", "-p"])
    #  main(sys.argv)
