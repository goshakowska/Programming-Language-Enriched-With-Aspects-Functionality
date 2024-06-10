from src.lexer.lexer import Lexer
from src.token.token_type import TokenType
from src.token.token import Token
from src.ast_tree.function_definition import FunctionDefinition
from src.ast_tree.aspect_definition import AspectDefinition
from src.ast_tree.identifier import Identifier
from src.ast_tree.conditional_statement import ConditionalStatement
from src.ast_tree.function_call import FunctionCall
from src.ast_tree.variable_declaration import VariableDeclaration
from src.ast_tree.for_statement import ForStatement
from src.ast_tree.while_statement import WhileStatement
from src.ast_tree.return_statement import ReturnStatement
from src.ast_tree.assignment_statement import AssignmentStatement
from src.ast_tree.statements_block import StatementsBlock
# from src.ast_tree.object_access import ObjectAccess
# from src.ast_tree.indexed_item import IndexedItem
from src.ast_tree.unary_term import UnaryTerm
from src.ast_tree.casted_term import CastedTerm
from src.ast_tree.less_than_expression import LessThanExpression
from src.ast_tree.greater_than_expression import GreaterThanExpression
from src.ast_tree.equal_expression import EqualExpression
from src.ast_tree.not_equal_expression import NotEqualExpression
from src.ast_tree.less_than_or_equal_expression import\
      LessThanOrEqualExpression
from src.ast_tree.greater_than_or_equal_expression import\
      GreaterThanOrEqualExpression
from src.ast_tree.plus_expression import PlusExpression
from src.ast_tree.minus_expression import MinusExpression
from src.ast_tree.multiplication_expression import MultiplicationExpression
from src.ast_tree.division_expression import DivisionExpression
from src.ast_tree.or_expression import OrExpression
from src.ast_tree.and_expression import AndExpression
from src.ast_tree.ast_type import AstType
from src.ast_tree.program import Program
from src.ast_tree.bool_literal import BoolLiteral
from src.ast_tree.str_literal import StrLiteral
from src.ast_tree.int_literal import IntLiteral
from src.ast_tree.float_literal import FloatLiteral

from src.parser.parser_errors import UnexpectedTokenTypeError
from src.parser.parser_errors import FunctionRedefinitionError
# from src.parser.parser_errors import StatementRedefinitionError
from src.parser.parser_errors import AspectRedefinitionError
from src.parser.parser_errors import MissingOpeningParenthesisError
from src.parser.parser_errors import MissingClosingParenthesisError
from src.parser.parser_errors import MissingSemicolonError
from src.parser.parser_errors import NoReturnTypeError
from src.parser.parser_errors import NoExecutionBlockError
from src.parser.parser_errors import InvalidAspectDefinitionSyntaxError
from src.parser.parser_errors import InvalidAspectTargetError
from src.parser.parser_errors import InvalidAspectEventError
from src.parser.parser_errors import UncompleteOrExpressionError
from src.parser.parser_errors import UncompleteAndExpressionError
from src.parser.parser_errors import UncompleteRelationExpressionError
from src.parser.parser_errors import UncompleteAdditiveExpressionError
from src.parser.parser_errors import UncompleteMultiplicativeExpressionError
from src.parser.parser_errors import UncompleteUnaryExpressionError
from src.parser.parser_errors import UncompleteCastedExpressionError
from src.parser.parser_errors import InvalidParameterError
from src.parser.parser_errors import InvalidObjectAccessSyntaxError
from src.parser.parser_errors import InvalidArgumentError
from src.parser.parser_errors import NoConditionBlockError
from src.parser.parser_errors import NoAssignmentExpressionError
from src.parser.parser_errors import NoIndexExpressionError
from src.parser.parser_errors import NoIteratorError
from src.parser.parser_errors import NoIterableError
from src.parser.parser_errors import InvalidExpressionError
from src.parser.parser_errors import InvalidAspectPatternError

RELATION_OPERATORS = {TokenType.LESS_THAN_OPERATOR: LessThanExpression,
                      TokenType.GREATER_THAN_OPERATOR: GreaterThanExpression,
                      TokenType.EQUAL: EqualExpression,
                      TokenType.NOT_EQUAL: NotEqualExpression,
                      TokenType.LESS_THAN_OR_EQUAL_OPERATOR:
                      LessThanOrEqualExpression,
                      TokenType.GREATER_THAN_OR_EQUAL_OPERATOR:
                      GreaterThanOrEqualExpression}

ADDITIVE_OPERATORS = {TokenType.PLUS: PlusExpression,
                      TokenType.MINUS: MinusExpression}

MULTIPLICATIVE_OPERATORS = {TokenType.MULTIPLICATION: MultiplicationExpression,
                            TokenType.DIVISION: DivisionExpression}

VARIABLE_TYPES = {TokenType.TYPE_BOOL: AstType.TYPE_BOOL,
                  TokenType.TYPE_FLOAT: AstType.TYPE_FLOAT,
                  TokenType.TYPE_INT: AstType.TYPE_INT,
                  TokenType.TYPE_STR: AstType.TYPE_STR}

RETURN_TYPES = {
    TokenType.TYPE_BOOL: AstType.TYPE_BOOL,
    TokenType.TYPE_FLOAT: AstType.TYPE_FLOAT,
    TokenType.TYPE_INT: AstType.TYPE_INT,
    TokenType.TYPE_STR: AstType.TYPE_STR,
    TokenType.NULL: AstType.NULL
}

ASPECT_TARGETS = {TokenType.TYPE_FUNCTION: AstType.TYPE_FUNCTION}

ASPECT_EVENTS = {TokenType.ASPECT_ON_START: AstType.ASPECT_ON_START,
                 TokenType.ASPECT_ON_END: AstType.ASPECT_ON_END,
                 TokenType.ASPECT_ON_CALL: AstType.ASPECT_ON_CALL}

LITERALS = {TokenType.BOOL: BoolLiteral,
            TokenType.FLOAT: FloatLiteral,
            TokenType.INT: IntLiteral,
            TokenType.STR: StrLiteral}


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
        self.consume_token()

    def consume_token(self):
        new_token = self.lexer.try_to_build_next_token()
        self.current_token = new_token

    def _must_be_and_consume(self, token_type: TokenType, exception) -> Token:
        if self.current_token.get_type() != token_type:
            raise exception
        token = self.current_token
        self.consume_token()
        return token

    def _must_be_in_set_and_consume(self, token_types: list[TokenType],
                                    exception) -> Token:
        if self.current_token.get_type() not in token_types:
            raise exception
        token = self.current_token
        self.consume_token()
        return token

    def _should_be_in_set_and_consume(self, token_types: list[TokenType]):
        if self.current_token.get_type() not in token_types:
            return None
        token = self.current_token
        self.consume_token()
        return token

    def _should_be_and_consume(self, token_type: TokenType):
        if self.current_token.get_type() != token_type:
            return None
        token = self.current_token
        self.consume_token()
        return token

    # program::= { declaration_statement |
    #              function_declaration  |
    #              aspect_declaration}
    def parse_program(self, name=None):
        functions = {}
        aspects = {}
        # declarations = []
        # declaration_names = set()
        statements = []

        def raise_(provided_error):
            raise provided_error

        while \
                self._parse_statement(
                lambda statement_to_add:
                statements.append(statement_to_add)
                    ) \
                or self._parse_function_declaration(
                lambda function_to_add:
                functions.setdefault(function_to_add.name, function_to_add)
                if function_to_add.name not in functions
                else raise_(FunctionRedefinitionError(
                    self.current_token.get_position(),
                function_to_add.name))
                    ) \
                or self._parse_aspect_declaration(
                lambda aspect_to_add:
                aspects.setdefault(aspect_to_add.name, aspect_to_add)
                if aspect_to_add.name not in aspects
                else raise_(AspectRedefinitionError(
                self.current_token.get_position(),
                aspect_to_add.name))
                    ):
            continue
        if self.current_token.get_type() != TokenType.ETX:
            raise SyntaxError
        else:
            return Program(name, functions, aspects, statements)

    # declaration_statement ::= declaration, [ "=", expression ]
    def _parse_declaration_statement(self, statement_handler=None):
        if declaration := self._parse_declaration():
            if self.current_token.type == TokenType.ASSIGN:
                position = self.current_token.get_position()
                self.consume_token()
                expression = self._parse_expression()
                self._must_be_and_consume(TokenType.SEMICOLON,
                                          MissingSemicolonError(
                                            self.current_token.get_position()))
                if statement_handler:
                    declaration = AssignmentStatement(position,
                                                      expression,
                                                      declaration)

                    statement_handler(declaration)
                    return True
                return AssignmentStatement(position, expression, declaration)
            if statement_handler:

                statement_handler(declaration)
                return True
            return declaration
        return None

    # function_declaration ::= "func", identifier, "(", [ parameters ], ")",
    # ":", return_type, block;
    def _parse_function_declaration(self, function_handler):
        if self.current_token.type != TokenType.TYPE_FUNCTION:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        token = self._must_be_and_consume(TokenType.IDENTIFIER,
                                          UnexpectedTokenTypeError
                                          (self.current_token.get_position(),
                                           TokenType.IDENTIFIER,
                                           self.current_token.get_type()))
        name = token.get_value()
        self._must_be_and_consume(TokenType.OPENING_BRACKET,
                                  MissingOpeningParenthesisError
                                  (self.current_token.get_position(), name))
        params = self._parse_parameters()
        self._must_be_and_consume(TokenType.CLOSING_BRACKET,
                                  MissingClosingParenthesisError
                                  (self.current_token.get_position(), name))
        self._must_be_and_consume(TokenType.COLON,
                                  UnexpectedTokenTypeError
                                  (self.current_token.get_position(),
                                   TokenType.COLON,
                                   self.current_token.get_type()))
        return_type = self._parse_return_type()
        if not return_type:
            raise NoReturnTypeError(self.current_token.get_position(), name)
        block = self._parse_block()
        if not block:
            raise NoExecutionBlockError(self.current_token.get_position(),
                                        name)
        function_handler(
            FunctionDefinition(position, name, params, block, return_type))
        return True

    # aspect_declaration ::= "aspect", identifier, ":", aspect_trigger, block;
    # regular_expression ::= string;
    def _parse_aspect_declaration(self, aspect_handler) -> AspectDefinition:
        if self.current_token.type != TokenType.TYPE_ASPECT:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        token = self._must_be_and_consume(TokenType.IDENTIFIER,
                                          UnexpectedTokenTypeError
                                          (self.current_token.get_position(),
                                           TokenType.IDENTIFIER,
                                           self.current_token.get_type()))
        name = token.get_value()
        self._must_be_and_consume(TokenType.COLON,
                                  UnexpectedTokenTypeError
                                  (self.current_token.get_position(),
                                   TokenType.COLON,
                                   self.current_token.get_type()))
        target, event, regular_expression = self._parse_aspect_trigger(name)
        block = self._parse_block()
        if not block:
            raise NoExecutionBlockError(self.current_token.get_position(),
                                        name)
        aspect_handler(
            AspectDefinition(position, name, target, event,
                             regular_expression, block)
            )
        return True

    # aspect_trigger ::= "on", aspect_target, aspect_event, "like",
    # regular_expression;
    def _parse_aspect_trigger(self, aspect_name):
        self._must_be_and_consume(TokenType.ON,
                                  InvalidAspectDefinitionSyntaxError
                                  (self.current_token.get_position(),
                                   aspect_name,
                                   TokenType.ON))
        if (target := self._parse_aspect_target()) is None:
            raise InvalidAspectTargetError(
                self.current_token.get_position(),
                aspect_name,
                ASPECT_TARGETS.keys()
                )
        target = ASPECT_TARGETS.get(target)
        if (event := self._parse_aspect_event()) is None:
            raise InvalidAspectEventError(
                self.current_token.get_position(),
                aspect_name,
                ASPECT_EVENTS.keys()
                )
        event = ASPECT_EVENTS.get(event)
        self._must_be_and_consume(TokenType.LIKE,
                                  InvalidAspectDefinitionSyntaxError(
                                      self.current_token.get_position(),
                                      aspect_name,
                                      TokenType.LIKE
                                  ))
        if (regular_expression := self._parse_identifier_or_call(None)) is None:
            raise InvalidAspectPatternError(
                self.current_token.get_position(),
                aspect_name)
        return target, event, regular_expression

    # aspect_target ::= "func";
    def _parse_aspect_target(self):
        if (token := self._should_be_in_set_and_consume(ASPECT_TARGETS)) \
             is None:
            return None
        aspect_target = token.get_type()
        return aspect_target

    # aspect_event ::= "start" | "end" | "call";
    def _parse_aspect_event(self):  # ? czy tutaj jest dobrze
        if (token := self._should_be_in_set_and_consume(ASPECT_EVENTS)) \
             is None:
            return None
        aspect_event = token.get_type()
        return aspect_event

    # declaration ::= type, identifier;
    def _parse_declaration(self):
        if self.current_token.get_type() not in VARIABLE_TYPES.keys():
            return None
        position = self.current_token.get_position()
        token = \
            self._must_be_in_set_and_consume(VARIABLE_TYPES.keys(), # ? czy tutaj jest dobrze
                                             UnexpectedTokenTypeError(
                                                self.current_token
                                                    .get_position(),
                                                VARIABLE_TYPES.keys(),
                                                self.current_token.get_type()
                                                ))
        token_type = VARIABLE_TYPES.get(token.get_type())
        token = self._must_be_and_consume(TokenType.IDENTIFIER,
                                          UnexpectedTokenTypeError
                                          (self.current_token.get_position(),
                                           TokenType.IDENTIFIER,
                                           self.current_token.get_type()))
        name = token.get_value()
        return VariableDeclaration(position, name, token_type)

    # type ::= "int" | "float" | "string" | "bool";
    def _parse_type(self):
        if (token := self._should_be_in_set_and_consume(VARIABLE_TYPES.keys() # ? czy tutaj jest dobrze
                                                        )) is None:
            return None
        token_type = token.get_type()
        return token_type

    # identifier ::= letter, {alphanumeric};
    def _parse_identifier(self):
        token = self._must_be_and_consume(TokenType.IDENTIFIER,
                                          UnexpectedTokenTypeError
                                          (self.current_token.get_position(),
                                           TokenType.IDENTIFIER,
                                           self.current_token.get_type()))
        return Identifier(token.get_position(), token.get_value())

    # expression ::= and_term, {"||", and_term};
    def _parse_expression(self):
        left_or_factor = self._parse_and_term()
        if left_or_factor is None:
            return None
        while self.current_token.get_type() == TokenType.OR:
            position = self.current_token.get_position()
            self.consume_token()
            right_or_factor = self._parse_and_term()
            if right_or_factor is None:
                raise UncompleteOrExpressionError(
                    self.current_token.get_position(),
                    left_or_factor
                )
            left_or_factor = OrExpression(
                position,
                left_or_factor,
                right_or_factor)
        return left_or_factor

    # and_term ::= relation_term, { "&&", relation_term};
    def _parse_and_term(self):
        left_and_factor = self._parse_relation_term()
        if left_and_factor is None:
            return None
        while self.current_token.get_type() == TokenType.AND:
            position = self.current_token.get_position()
            self.consume_token()
            right_and_factor = self._parse_relation_term()
            if right_and_factor is None:
                raise UncompleteAndExpressionError(
                    self.current_token.get_position(),
                    # AstType.AND,
                    left_and_factor
                )
            left_and_factor = AndExpression(
                position,
                left_and_factor,
                right_and_factor)
        return left_and_factor  # czy to potrzebne?

    # relation_term ::= additive_term, [relation_operator, additive_term];
    # relation_operator ::= ">=" | ">" | "<=" | "<" | "==" | "!=";
    def _parse_relation_term(self):
        left_additive_factor = self._parse_additive_term()
        if left_additive_factor is None:
            return None
        if (relation_constructor := RELATION_OPERATORS.get(
             self.current_token.get_type())):
            position = self.current_token.get_position()
            self.consume_token()
            right_additive_factor = self._parse_additive_term()
            if right_additive_factor is None:
                raise UncompleteRelationExpressionError(
                    self.current_token.get_position(),
                    left_additive_factor
                )
            left_additive_factor = relation_constructor(
                position,
                left_additive_factor,
                right_additive_factor
                )
        return left_additive_factor

    # additive_term ::= multiplicative_term, { ("+" | "-"),
    # multiplicative_term};
    def _parse_additive_term(self):
        left_multiplicative_factor = self._parse_multiplicative_term()
        if left_multiplicative_factor is None:
            return None
        while additive_constructor := ADDITIVE_OPERATORS.get(
             self.current_token.get_type()):
            position = self.current_token.get_position()
            self.consume_token()
            right_multiplicative_factor = self._parse_multiplicative_term()
            if right_multiplicative_factor is None:
                raise UncompleteAdditiveExpressionError(
                    self.current_token.get_position(),
                    left_multiplicative_factor
                )
            left_multiplicative_factor = additive_constructor(
                position,
                left_multiplicative_factor,
                right_multiplicative_factor
                )
        return left_multiplicative_factor

    # multiplicative_term ::= unary_term, { ("*" | "/" ), unary_term};
    def _parse_multiplicative_term(self):
        left_unary_term = self._parse_unary_term()
        if left_unary_term is None:
            return None
        while multiplicative_constructor := MULTIPLICATIVE_OPERATORS.get(
             self.current_token.get_type()):
            position = self.current_token.get_position()
            self.consume_token()
            right_unary_term = self._parse_unary_term()
            if right_unary_term is None:
                raise UncompleteMultiplicativeExpressionError(
                    self.current_token.get_position(),
                    left_unary_term
                )
            left_unary_term = multiplicative_constructor(
                position,
                left_unary_term,
                right_unary_term)
        return left_unary_term

    # parameters ::= [parameter, { ",", parameter }];
    # parameter ::= declaration;
    def _parse_parameters(self) -> list:  # lista parametrów
        parameters = []
        if (parameter := self._parse_declaration()) is None:
            return parameters
        parameters.append(parameter)
        while self.current_token.get_type() == TokenType.COMMA:
            self.consume_token()
            parameter = self._parse_declaration()
            if not parameter:
                raise InvalidParameterError(
                    self.current_token.get_position(),
                    parameters[-1].get_name()
                    )
            parameters.append(parameter)
        return parameters

    # return_type ::= type | "null";
    def _parse_return_type(self):  # typ z AST
        if self.current_token.get_type() not in VARIABLE_TYPES.keys():
            if self.current_token.get_type() == TokenType.NULL:
                self.consume_token()
                return_type = AstType.NULL
                return return_type
            else:
                raise UnexpectedTokenTypeError(
                    self.current_token.get_position(),
                    VARIABLE_TYPES.keys(),
                    self.current_token.get_type()
                    )
        return_type = VARIABLE_TYPES.get(self._parse_type())  #
        return return_type

    # block ::= "{", { statement }, "}";
    def _parse_block(self):
        if self.current_token.get_type() != TokenType.OPENING_CURLY_BRACKET:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        statements = []
        while statement := self._parse_statement():
            statements.append(statement)
        self._must_be_and_consume(TokenType.CLOSING_CURLY_BRACKET,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.CLOSING_CURLY_BRACKET,
                                      self.current_token.get_type()
                                  ))
        return StatementsBlock(position, statements)  #

    # statement ::= selection_statement | declaration_statement
    # | assignment_or_call_statement | iteration_statement | return_statement;
    def _parse_statement(self, statement_handler=None):  #
        return self._parse_condition_statement(statement_handler) or\
               self._parse_declaration_statement(statement_handler) or\
               self._parse_assignment_or_call_statement(statement_handler) or\
               self._parse_iteration_statement(statement_handler) or\
               self._parse_return_statement(statement_handler) or\
               None

    # selection_statement ::= "if", "(", condition, ")", block,
    # ["else", block];
    # condition ::= expression;
    def _parse_condition_statement(self, statement_handler=None):
        if self.current_token.get_type() != TokenType.IF:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        self._must_be_and_consume(TokenType.OPENING_BRACKET,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.OPENING_BRACKET,
                                      self.current_token.get_type()
                                  ))
        condition = self._parse_expression()
        if not condition:
            raise NoConditionBlockError(
                position,
                "'if'"
            )  #
        self._must_be_and_consume(TokenType.CLOSING_BRACKET,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.CLOSING_BRACKET,
                                      self.current_token.get_type()
                                  ))
        if_block = self._parse_block()
        if not if_block:
            raise NoExecutionBlockError(position, "'if'")
        else_block = None
        if self.current_token.get_type() == TokenType.ELSE:  #
            self.consume_token()
            else_block = self._parse_block()
            if not else_block:
                raise NoExecutionBlockError(position, "'else'")
        if statement_handler:
            statement = ConditionalStatement(position,
                                             condition,
                                             if_block,
                                             else_block)
            statement_handler(statement)
            return True
        return ConditionalStatement(position, condition, if_block, else_block)

    # assignment_or_call_statement ::= object_access, ["=", expression ] ";";
    def _parse_assignment_or_call_statement(self, statement_handler=None):
        position = self.current_token.get_position()
        result = self._parse_object_access()
        if not result:
            return None
        if self.current_token.get_type() == TokenType.ASSIGN:
            self.consume_token()
            expression = self._parse_expression()
            if not expression:
                raise NoAssignmentExpressionError(position)
            result = AssignmentStatement(position, expression, result)
        self._must_be_and_consume(TokenType.SEMICOLON,
                                  MissingSemicolonError(
                                          self.current_token.get_position()))
        if statement_handler:
            statement_handler(result)
            return True
        return result

    # object_access ::= item, {".", item};
    def _parse_object_access(self):
        position = self.current_token.get_position()
        if (item := self._parse_identifier_or_call(None)) is None:
            return None
        while self.current_token.get_type() == TokenType.DOT:
            self.consume_token()
            if (dot_item := self._parse_identifier_or_call(item)) is None:
                raise InvalidObjectAccessSyntaxError(
                    position,
                    item.name
                )
            item = dot_item 
        return item

    # identifier_or_call ::= identifier, [ "(", arguments, ")" ];
    def _parse_identifier_or_call(self, parent):
        if self.current_token.get_type() != TokenType.IDENTIFIER:
            return None
        name = self.current_token.get_value()
        position = self.current_token.get_position()
        self.consume_token()
        if result := self._parse_function_call(position, name, parent):
            return result
        return Identifier(position, name, parent)

    def _parse_function_call(self, position, name, parent):
        if self.current_token.get_type() != TokenType.OPENING_BRACKET:
            return None
        self.consume_token()
        arguments = self._parse_arguments()
        self._must_be_and_consume(TokenType.CLOSING_BRACKET,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.CLOSING_BRACKET,
                                      self.current_token.get_type()))
        return FunctionCall(position, name, arguments, parent)

    # arguments ::= expression, {",", expression};
    def _parse_arguments(self):
        arguments = []
        argument = self._parse_expression()
        if not argument:
            return arguments
        arguments.append(argument)
        while self.current_token.get_type() == TokenType.COMMA:
            self.consume_token()
            argument = self._parse_expression()
            if not argument:
                raise InvalidArgumentError(
                    self.current_token.get_position(),
                    arguments[-1].name)
            arguments.append(argument)
        return arguments

    # iteration_statement ::= "for", identifier, "in", expression, block |
    # "while", "(", condition, ")", block;
    # condition ::= expression;
    def _parse_iteration_statement(self, statement_handler=None):
        return self._parse_for_statement(statement_handler)\
            or self._parse_while_statement(statement_handler)

    def _parse_for_statement(self, statement_handler=None):
        if self.current_token.get_type() != TokenType.FOR:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        iterator = self._parse_identifier_or_call(None)
        if not iterator:
            raise NoIteratorError(position)  #
        self._must_be_and_consume(TokenType.IN,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.IN,
                                      self.current_token.get_type()))
        iterable = self._parse_expression()
        if not iterable:
            raise NoIterableError(position, iterator)  #
        execution_block = self._parse_block()
        if not execution_block:
            raise NoExecutionBlockError(position, "for")  #
        if statement_handler:
            statement = ForStatement(position,
                                     iterator,
                                     iterable,
                                     execution_block)
            statement_handler(statement)
            return True
        return ForStatement(position, iterator, iterable, execution_block)

    def _parse_while_statement(self, statement_handler=None):
        if self.current_token.get_type() != TokenType.WHILE:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        self._must_be_and_consume(TokenType.OPENING_BRACKET,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.OPENING_BRACKET,
                                      self.current_token.get_type()))
        condition = self._parse_expression()
        if not condition:
            raise NoConditionBlockError(position, "while")  #
        self._must_be_and_consume(TokenType.CLOSING_BRACKET,
                                  UnexpectedTokenTypeError(
                                      self.current_token.get_position(),
                                      TokenType.CLOSING_BRACKET,
                                      self.current_token.get_type()))
        execution_block = self._parse_block()
        if not execution_block:
            raise NoExecutionBlockError(position, "while")  #
        if statement_handler:
            statement = WhileStatement(position, condition, execution_block)
            statement_handler(statement)
            return True
        return WhileStatement(position, condition, execution_block)

    # return_statement ::= "return", [expression], ";";
    def _parse_return_statement(self,  statement_handler=None):
        if self.current_token.get_type() != TokenType.RETURN:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        expression = self._parse_expression()
        self._must_be_and_consume(TokenType.SEMICOLON,
                                  MissingSemicolonError(
                                      self.current_token.get_position()))
        if statement_handler:
            statement = ReturnStatement(position, expression)
            statement_handler(statement)
            return True
        return ReturnStatement(position, expression)

    # unary_term ::= ["-"], casted_term;
    def _parse_unary_term(self):
        negated = False
        position = self.current_token.get_position()
        if self.current_token.get_type() == TokenType.MINUS:
            # position = self.current_token.get_position()
            self.consume_token()
            negated = True
        casted_term = self._parse_casted_term()
        if negated and casted_term:
            return UnaryTerm(position, casted_term)
        if negated and not casted_term:
            raise UncompleteUnaryExpressionError(
                self.current_token.get_position())
        return casted_term

    # casted_term ::= term, ["as", type];
    def _parse_casted_term(self):
        term = self._parse_term()
        if not term:
            return None
        if self.current_token.get_type() == TokenType.AS:
            position = self.current_token.get_position()
            self.consume_token()
            if (casted_type := self._parse_type()) is None:
                raise UncompleteCastedExpressionError(
                    self.current_token.get_position(),
                    term)
            casted_type = VARIABLE_TYPES.get(casted_type)
            return CastedTerm(position, term, casted_type)
        return term

    # term ::= literal | object_access | "(", expression, ")";
    def _parse_term(self):
        if term := self._parse_literal():
            return term
        elif term := self._parse_object_access():
            return term
        elif self.current_token.get_type() == TokenType.OPENING_BRACKET:
            self.consume_token()
            term = self._parse_expression()
            if not term:
                raise InvalidExpressionError(self.current_token.get_position())
            self._must_be_and_consume(TokenType.CLOSING_BRACKET,
                                      UnexpectedTokenTypeError(
                                          self.current_token.get_position(),
                                          TokenType.CLOSING_BRACKET,
                                          self.current_token.get_type()))
            return term

    # literal ::= int | float | bool | string;
    def _parse_literal(self):
        if literal_constructor := LITERALS.get(self.current_token.get_type()):
            position = self.current_token.get_position()
            value = self.current_token.get_value()
            self.consume_token()
            return literal_constructor(position, value)
        return None
