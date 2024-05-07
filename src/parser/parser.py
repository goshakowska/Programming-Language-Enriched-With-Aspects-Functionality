from lexer.lexer import Lexer
from token.token_type import TokenType
from token.token import Token
from invalid_syntax_error import InvalidSyntaxError
from ast.function_definiton import FunctionDefinition
from ast.aspect_definition import AspectDefinition
from ast.identifier import Identifier
from ast.selection_statement import SelectionStatement
from ast.function_call import FunctionCall
from ast.variable_declaration import VariableDeclaration
from ast.for_statement import ForStatement
from ast.while_statement import WhileStatement
from ast.return_statement import ReturnStatement

from ast.less_than_expression import LessThanExpression
from ast.greater_than_expression import GreaterThanExpression
from ast.equal_expression import EqualExpression
from ast.not_equal_expression import NotEqualExpression
from ast.less_than_or_equal_expression import LessThanOrEqualExpression
from ast.greater_than_or_equal_expression import GreaterThanOrEqualExpression

from ast.plus_expression import PlusExpression
from ast.minus_expression import MinusExpression

from ast.multiplication_expression import MultiplicationExpression
from ast.division_expression import DivisionExpression

from ast.or_expression import OrExpression
from ast.and_expression import AndExpression

from ast.assignment_statement import AssignmentStatement
from ast.ast_type import AstType
from ast.program import Program

# from ast.aspect_trigger import AspectTrigger  # czy potrzebna klasa aspect trigger?



# TYPE_SPECIFIERS = [TokenType.ASPECT_TYPE, TokenType.BOOL_TYPE,  TokenType.FLOAT_TYPE, TokenType.FUNCTION_TYPE, TokenType.INT_TYPE, TokenType.STR_TYPE]

RELATION_OPERATORS = [TokenType.LESS_THAN_OPERATOR, TokenType.GREATER_THAN_OPERATOR, TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN_OR_EQUAL_OPERATOR, TokenType.GREATER_THAN_OR_EQUAL_OPERATOR]

ASPECT_TARGETS = [TokenType.FUNCTION_TYPE]  # rozszerzalne?

ASPECT_EVENTS = [TokenType.ASPECT_ON_START, TokenType.ASPECT_ON_END, TokenType.ASPECT_ON_CALL]

# VARIABLE_TYPES = [TokenType.BOOL_TYPE, TokenType.FLOAT_TYPE, TokenType.INT_TYPE, TokenType.STR_TYPE]

LITERALS = [TokenType.BOOL, TokenType.FLOAT, TokenType.INT, TokenType.STR]

# UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA UWAGA 
# Początek dobrych słowników:
# TYPE_SPECIFIERS = {TokenType.BOOL_TYPE: AST.BOOL_TYPE,  TokenType.FLOAT_TYPE: AST.FLOAT_TYPE, TokenType.INT_TYPE: AST.INT_TYPE, TokenType.STR_TYPE: AST.STR_TYPE} TODO: DONE!

RELATION_OPERATORS = {TokenType.LESS_THAN_OPERATOR: LessThanExpression, TokenType.GREATER_THAN_OPERATOR: GreaterThanExpression, TokenType.EQUAL: EqualExpression, TokenType.NOT_EQUAL: NotEqualExpression, TokenType.LESS_THAN_OR_EQUAL_OPERATOR: LessThanOrEqualExpression, TokenType.GREATER_THAN_OR_EQUAL_OPERATOR: GreaterThanOrEqualExpression}  # TODO: DONE!

ADDITIVE_OPERATORS = {TokenType.PLUS: PlusExpression, TokenType.MINUS: MinusExpression}  # TODO: DONE!

MULTIPLICATIVE_OPERATORS = {TokenType.MULTIPLICATION: MultiplicationExpression, TokenType.DIVISION: DivisionExpression}  # TODO: DONE!

VARIABLE_TYPES = {TokenType.BOOL_TYPE: AstType.BOOL_TYPE, TokenType.FLOAT_TYPE: AstType.FLOAT_TYPE, TokenType.INT_TYPE: AstType.INT_TYPE, TokenType.STR_TYPE: AstType.STR_TYPE}  # TODO: DONE!

# ASPECT_TARGETS = {TokenType.FUNCTION_TYPE: AstType.FUNCTION}  # rozszerzalne?

# ASPECT_EVENTS = {TokenType.ASPECT_ON_START: AstType.ASPECT_ON_START, TokenType.ASPECT_ON_END: AstType.ASPECT_ON_END, TokenType.ASPECT_ON_CALL: AstType.ASPECT_ON_CALL}  # TODO: DONE!

# LITERALS = {TokenType.BOOL: AstType.BOOL, TokenType.FLOAT: AstType.FLOAT, TokenType.INT: AstType.INT, TokenType.STR: AstType.STR}



# w error handlerze będą odkładane informacje o błędach - podobnie, jak mam to zrobić z lekserem, czyli np. jak błąd jest nieterminalny - wrzucam go do error handlera i potem on tę linijkę z błędem wypluwa. nie trzeba tego robić - można po prostu przekazać błąd do głównej pętli i zatrzymać program

class Parser:
    def __init__(self, lexer: Lexer, token: Token, error_handler) -> None:
        self.lexer = lexer
        self.error_handler = error_handler
        self.lexer.try_to_build_next_token()
        self.current_token = self.lexer.get_token()

        # tak, jak przy analizie leksykalnej zasysamy pierwszy token
        self.consume_token()  # zawsze mamy token nie obrobiony jeszcze, czyli nasz parser trzyma token nieobrobiony

    def consume_token(self):
        new_token = self.lexer.try_to_build_next_token()
        self.current_token = new_token

    def _must_be_and_consume(self, token_type: TokenType, exception) -> Token:
        if self.current_token.get_type() != token_type:
            raise InvalidSyntaxError(self.current_token.get_position, self.current_token)  # TODO: zamiast error handlera throw Error i tyle
        # value = self.current_token.value  # zmieniam z oryginalnej implementacji na tę z całym tokenem
        token = self.current_token
        self.consume_token()
        return token
    
    def _must_be_in_set_and_consume(self, token_types: list[TokenType], exception) -> Token:
        if self.current_token.get_type() not in token_types:
            raise InvalidSyntaxError(self.current_token.get_position, self.current_token)
        token = self.current_token
        self.consume_token()
        return token
        # self._must_be(token_type)
        # return self.consume_token()  # czy tu return czy po prostu self.consume_token()
        # pass

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

    # jedyna publiczna metoda takiego parsera

    # program::= { declaration_statement | function_declaration | aspect_declaration}
    # {} ebnfa odpowiada pętla while
    def parse_program(self):  # TODO: utworzyć klasę program
        functions = set()
        aspects = set()
        statements = []
        # functions = {
        #     "declaration_statement": self._parse_declaration_statement(),  # todo
        #     "function_declaration": self._parse_function_declaration(),
        #     "aspect_declaration": self._parse_aspect_declaration(),
        # }
        def raise_(provided_error):
            raise provided_error
        
        while self._parse_declaration_statement(lambda statement_to_add: statements.append(statement_to_add) if statement_to_add not in statements else raise_(SyntaxError)) or self._parse_function_declaration(lambda function_to_add: functions.append(function_to_add) if function_to_add.name() not in functions else raise_(SyntaxError)) or self._parse_aspect_declaration(lambda aspect_to_add: aspects.add(aspect_to_add) if aspect_to_add.name() not in aspects else raise_(SyntaxError)):
            continue
        if self.current_token.get_type() != TokenType.ETX:
            raise SyntaxError
        else:
            return Program(functions, aspects, statements)
        # dopóki definicja funkcji
        # while 
    
    ######## ALTERNATYWA LAMBD
    # def function_adder(function_to_add: FunctionDefinition, function_set: set):
    #     if function_to_add.name() not in function_set:
    #         function_set.add(function_to_add)
    #     else:
    #         raise SyntaxError
        
    # def aspect_adder(aspect_to_add: AspectDefinition, aspect_set: set):
    #     if aspect_to_add.name() not in aspect_set:
    #         aspect_set.add(aspect_to_add)
    #     else:
    #         raise SyntaxError
        
    # def declaration_statement_adder(declaration_statement_to_add: VariableDeclaration, statements_list: list):
    #     if declaration_statement_to_add not in statements_list:
    #         statements_list.append(declaration_statement_to_add)
    #     else:
    #         raise SyntaxError
    ######## ALTERNATYWA LAMBD

    # definicje funkcji muszą być unikalne - unikalność na poziomie nazwy - nie chcemy mieć redefiniowanych funkcji

    # declaration_statement ::= declaration, [ "=", expression ]
    def _parse_declaration_statement(self):
        if declaration := self._parse_declaration():
            if self.current_token.type == TokenType.ASSIGN:
                position = self.current_token.get_position()
                self.consume_token()
                expression = self._parse_expression()
                return AssignmentStatement(position, declaration, expression)
            return declaration
        return None

    # function_declaration ::= "func", identifier, "(", [ parameters ], ")", ":", return_type, block; 
    def _parse_function_declaration(self, function_handler) -> FunctionDefinition:
        if self.current_token.type != TokenType.FUNCTION_TYPE:
            return None  # to nie jest jeszcze błąd - po prostu nie widzę tu jeszcze funkcji
        position = self.current_token.get_position()  # jeżeli chcemy, aby pozycja definicji funkcji była zgodna z pozycją pierwszego tokenu
        self.consume_token()
        token = self._must_be_and_consume(TokenType.IDENTIFIER, SyntaxError)  # nazwy z tokenType'a
        name = token.get_value()
        self._must_be_and_consume(TokenType.OPENING_BRACKET, SyntaxError)
        params = self._parse_parameters()
        self._must_be_and_consume(TokenType.CLOSING_BRACKET, SyntaxError)
        self._must_be_and_consume(TokenType.COLON, SyntaxError)
        return_type = self._parse_return_type()
        if not return_type:
            raise SyntaxError
        block = self._parse_block()
        if not block:
            raise SyntaxError  # brak bloku - błąd składniowy
        # return FunctionDefinition(position, name, params, return_type)
        function_handler(FunctionDefinition(position, name, params, return_type))
        return True

    # aspect_declaration ::= "aspect", identifier, ":", aspect_trigger, block;
    # regular_expression ::= string;
    def _parse_aspect_declaration(self, aspect_handler) -> AspectDefinition:
        if self.current_token.type != TokenType.ASPECT_TYPE:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        token = self._must_be_and_consume(TokenType.IDENTIFIER, SyntaxError)
        name = token.get_value()
        self._must_be_and_consume(TokenType.COLON, SyntaxError)
        target, event, regular_expression = self._parse_aspect_trigger()
        self._parse_block()
        aspect_handler(AspectDefinition(position, name, target, event, regular_expression))
        return True  # TODO: DONE!

    # aspect_trigger ::= "on", aspect_target, aspect_event, "like", regular_expression;
    def _parse_aspect_trigger(self):
        self._must_be_and_consume(TokenType.ON, SyntaxError)
        if target := self._parse_aspect_target() is None:
            raise SyntaxError
             # TODO z przypisaniem, aby tutaj wyrzucać błędy!
        if event := self._parse_aspect_event() is None:
            raise SyntaxError
        self._must_be_and_consume(TokenType.LIKE, SyntaxError)
        regular_expression = self._parse_identifier()
        return target, event, regular_expression

    # aspect_target ::= "func";
    def _parse_aspect_target(self):
        if token := self._should_be_in_set_and_consume(ASPECT_TARGETS) is None:
            return None  # TODO: should_be_in_set_and_consume DONE!
        aspect_target = token.get_type()
        # aspect_target = self.lexer.key_words.keys()[ self.lexer.key_words.values().index(token.get_type())]  # zwraca func
        return aspect_target

    # aspect_event ::= "start" | "end" | "call";
    def _parse_aspect_event(self):
        if token := self._should_be_in_set_and_consume(ASPECT_EVENTS) is None:
            return None
        aspect_event = token.get_type()
        # aspect_event = self.lexer.key_words.keys()[ self.lexer.key_words.values().index(token.get_type())] # zwraca "start" | "end" | "call"
        return aspect_event

    # declaration ::= type, identifier;
    def _parse_declaration(self):
        if self.current_token.get_type() not in VARIABLE_TYPES.keys():  # TODO: Typ w AST!
            return None
        position = self.current_token.get_position()
        token = self._must_be_in_set_and_consume(VARIABLE_TYPES, InvalidSyntaxError)  
        token_type = token.get_type()
        token = self._must_be_and_consume(TokenType.IDENTIFIER, SyntaxError)
        name = token.get_value()
        return VariableDeclaration(position, token_type, name)

    # type ::= "int" | "float" | "string" | "bool";
    def _parse_type(self):
        if token := self._should_be_in_set_and_consume(VARIABLE_TYPES.keys()) is None:
            return None  # TODO:can_be_in_set_and_consume(VARIABLE_TYPES, None) DONE!
        token_type = token.get_type()
        return token_type

    # identifier ::= letter, {alphanumeric};
    def _parse_identifier(self):
        token = self._must_be_and_consume(TokenType.IDENTIFIER, SyntaxError)
        return Identifier(token.get_position(), token.get_value())

    # tu kilka, and, or, +, -, *, / itd itd  ?

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
                return InvalidSyntaxError()
            left_or_factor = OrExpression(position, left_or_factor, right_or_factor)

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
                return InvalidSyntaxError()
            left_and_factor = AndExpression(position, left_and_factor, right_and_factor)

    # relation_term ::= additive_term, [relation_operator, additive_term];
    def _parse_relation_term(self): 
        left_additive_factor = self._parse_additive_term()
        if left_additive_factor is None:
            return None
        if relation_constructor := RELATION_OPERATORS.get(self.current_token.get_type()):
            position = self.current_token.get_position()
            self.consume_token()
            # relation_operator = self._parse_relation_operator()
            right_additive_factor = self._parse_additive_term()
            if right_additive_factor is None:
                return InvalidSyntaxError()
            left_additive_factor = relation_constructor(position, left_additive_factor, right_additive_factor)  # czy robić tutaj rozróżnienie na różne >=, <= itd
        return left_additive_factor

    # relation_operator ::= ">=" | ">" | "<=" | "<" | "==" | "!=";

    # additive_term ::= multiplicative_term, { ("+" | "-"), multiplicative_term};
    def _parse_additive_term(self):
        left_multiplicative_factor = self._parse_multiplicative_term()
        if left_multiplicative_factor is None:
            return None
        while additive_constructor := ADDITIVE_OPERATORS.get(self.current_token.get_type()):
        # while self.current_token.get_type() in (TokenType.PLUS, TokenType.MINUS):
            position = self.current_token.get_position()
            self.consume_token()
            right_multiplicative_factor = self._parse_multiplicative_term()
            if right_multiplicative_factor is None:
                return InvalidSyntaxError()
            left_multiplicative_factor = additive_constructor(position, left_multiplicative_factor, right_multiplicative_factor)
        return left_multiplicative_factor

    # multiplicative_term ::= unary_term, { ("*" | "/" ), unary_term};
    def _parse_multiplicative_term(self):  # TODO: DONE!
        left_unary_term = self._parse_unary_term()
        if left_unary_term is None:
            return None
        while multiplicative_constructor := MULTIPLICATIVE_OPERATORS.get(self.current_token.get_type()):
        # while self.current_token.get_type() in (TokenType.MULTIPLICATION, TokenType.DIVISION):
            position = self.current_token.get_position()
            self.consume_token()
            right_unary_term = self._parse_unary_term()
            if right_unary_term is None:
                return InvalidSyntaxError()
            left_unary_term = multiplicative_constructor(position, left_unary_term, multiplicative_operator, right_unary_term)
        return left_unary_term

    # parameters ::= [parameter, { ",", parameter }];
    # parameter ::= declaration;
    def _parse_parameters(self, parameter) -> list:  # lista parametrów
        parameters = []
        if parameter := self._parse_declaration() is None:
            return parameters
        parameters.append(parameter)
        while self.current_token.get_type() == TokenType.COMMA:
            self.consume_token()
            parameter = self._parse_declaration()
            if not parameter:
                raise InvalidSyntaxError(self.current_token.get_position, self.current_token)  # TODO: DONE!
            parameters.append(parameter)
        return parameters


    # return_type ::= type | "null";
    def _parse_return_type(self):  # typ z AST
        if self.current_token.get_type() not in VARIABLE_TYPES:
            if self.current_token.get_type() == TokenType.NULL:
                return None
            else:
                raise InvalidSyntaxError(self.current_token.get_position, self.current_token)
        return self._parse_type()

    # block ::= "{", { statement }, "}";
    def _parse_block(self):
        if self.current_token.get_type() != TokenType.OPENING_CURLY_BRACKET:
            return None
        self.consume_token()
        statements = []
        while statement := self._parse_statement():
            statements.append(statement)
        self._must_be_and_consume(TokenType.CLOSING_CURLY_BRACKET)
        return statements

    # statement ::= selection_statement | declaration_statement | assignment_or_call_statement | iteration_statement | return_statement;
    def _parse_statement(self): 
        if statement := self._parse_selection_statement() is None:
            if statement := self._parse_declaration_statement() is None:
                if statement := self._parse_assignment_or_call_statement() is None:
                    if statement := self._parse_iteration_statement() is None:
                        if statement := self._parse_return_statement() is None:
                            return None
        return statement

    # selection_statement ::= "if", "(", condition, ")", block, ["else", block];
    # condition ::= expression;
    def _parse_selection_statement(self):
        if self.current_token.get_type() != TokenType.IF:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        self._must_be_and_consume(TokenType.OPENING_BRACKET, InvalidSyntaxError())
        condition = self._parse_expression()
        self._must_be_and_consume(TokenType.CLOSING_BRACKET, InvalidSyntaxError())
        if_block = self._parse_block()
        if not if_block:
            pass  # brak bloku - błąd składniowy - TODO
        if self.current_token.get_type() != TokenType.ELSE:
            return SelectionStatement(position, condition, if_block, else_block=None)
        self.consume_token()
        else_block = self._parse_block()
        if not else_block:
            pass # brak bloku - błąd składniowy  - TODO
        return SelectionStatement(position, condition, if_block, else_block)

    # assignment_or_call_statement ::= object_access, ["=", expression ] ";";
    def _parse_assignment_or_call_statement(self):
        position = self.current_token.get_position()
        object_access = self._parse_object_access()
        if self.current_token.get_type() == TokenType.ASSIGNMENT:
            self.consume_token()
            expression = self._parse_expression()
            self._must_be_and_consume(TokenType.SEMICOLON, InvalidSyntaxError())
            return AssignmentStatement(position, object_access, expression)
        self._must_be_and_consume(TokenType.SEMICOLON, InvalidSyntaxError())
        return object_access

    # object_access ::= item, {".", item};
    def _parse_object_access(self):
        position = self.current_token.get_position()
        if item := self._parse_item() is None:
            return None
        while self.current_token.get_type() == TokenType.DOT:
            self.consume_token()
            if dot_item := self._parse_item() is None:
                raise SyntaxError
            item = ObjectAccess(position, item, dot_item)
        return item

    # item ::= identifier_or_call, {"[", expression, "]"};
    def _parse_item(self):
        position = self.current_token.get_position()
        tmp_item = self._parse_identifier_or_call()
        while self.current_token.get_type() == TokenType.OPENING_SQUARE_BRACKET:
            self.consume_token()
            index = self._parse_expression()
            self._must_be_and_consume(TokenType.CLOSING_SQUARE_BRACKET, InvalidSyntaxError())
            tmp_item = IndexedItem(position, tmp_item, index)
        return tmp_item

    # identifier_or_call ::= identifier, [ "(", arguments, ")" ];

    def _parse_identifier_or_call(self):
        if self.current_token.get_type() != TokenType.IDENTIFIER:
            return None
        name = self.current_token.get_value()
        position = self.current_token.get_position()
        self.consume_token()
        if result := self._parse_function_call(name):
            return result
        return Identifier(position, name)

    def _parse_function_call(self, name: str):
        if self.current_token.get_type() != TokenType.OPENING_BRACKET:
            return None
        self.consume_token()
        arguments = self._parse_arguments()
        self._must_be_and_consume(TokenType.CLOSING_BRACKET, InvalidSyntaxError())
        return FunctionCall(name, arguments)

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
                raise SyntaxError
            arguments.append(argument)
        return arguments
    # TODO: DONE! [ "(", parameters, ")" ] funkcja function_call, na start name 

    # iteration_statement ::= "for", identifier, "in", expression, block | "while", "(", condition, ")", block;
    # condition ::= expression;

    def _parse_iteration_statement(self):
        if for_statement := self._parse_for_statement():
            return for_statement
        elif while_statement := self._parse_while_statement():
            return while_statement
        else:
            return None

    def _parse_for_statement(self):
        if self.current_token.get_type() != TokenType.FOR:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        iterator = self._parse_identifier(TokenType.IDENTIFIER, SyntaxError)
        self._must_be_and_consume(TokenType.IN, SyntaxError)
        iterable = self._parse_expression()
        execution_block = self._parse_block()
        return ForStatement(position, iterator, iterable, execution_block)

    def _parse_while_statement(self):
        if self.current_token.get_type() != TokenType.WHILE:
            return None
        position = self.current_token.get_position()
        self.consume_token()
        self._must_be_and_consume(TokenType.OPENING_BRACKET, SyntaxError)
        condition = self._parse_expression()
        self._must_be_and_consume(TokenType.CLOSING_BRACKET, SyntaxError)
        execution_block = self._parse_block()
        return WhileStatement(position, condition, execution_block)    

    # return_statement ::= "return", [expression], ";";
    def _parse_return_statement(self):
        if self.current_token.get_type() != TokenType.RETURN:
            return None  # czy None czy nie wyrzucić errora?
        position = self.current_token.get_position()
        self.consume_token
        expression = self._parse_expression()
        self._must_be_and_consume(TokenType.SEMICOLON, InvalidSyntaxError())
        return ReturnStatement(position, expression)

    # unary_term ::= ["-"], casted_term;
    def _parse_unary_term(self):
        negated = False
        if self.current_token.get_type() == TokenType.MINUS:
            self.consume_token()
            negated = True
        casted_term = self._parse_casted_term()
        if negated and casted_term:
            return UnaryTerm(casted_term)
        if negated and not casted_term:
            raise SyntaxError
        return casted_term

    # casted_term ::= term, ["as", type];
    def _parse_casted_term(self):
        term = self._parse_term()
        if not term:
            return None
        if self.current_token.get_type() == TokenType.AS:
            self.consume_token()
            if type := self._parse_type() is None:
                raise SyntaxError
            return CastedTerm(term, type)
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
            self._must_be_and_consume(TokenType.CLOSING_BRACKET, InvalidSyntaxError())
            return term  # co tutaj zwracać? literal ma inną konstrukcję niż expression(?)


    # literal ::= int | float | bool | string;
    def _parse_literal(self):
        token = self._must_be_in_set_and_consume(LITERALS, None)  # tutaj nie wyrzuca błędu
        if token:
            literal = token.get_value()
            return literal
        return None


    # jeżeli chcemy, żeby coś tam było to sprawdzamy, czy coś tam jest, wyciągamy to co trzeba i konsumujemy
    # czasami sprawdzamy, czy coś tam jest, ale nie wyciągamy z tego wartości - np. nawias otwierający - jak jest - dobrze, jak nie - błąd, ale nie musimy nic z niego wyciągać!
    # tworzone obiekty - nie mutowalne, mają akceptować tylko wizytację

# tartar

        # if self.current_token.get_type() == TokenType.FOR:  # _parse_for_statement() TODO: DONE!
        #     position = self.current_token.get_position()
        #     self.consume_token()
        #     iterator = self._parse_identifier(TokenType.IDENTIFIER, SyntaxError)
        #     self._must_be_and_consume(TokenType.IN, SyntaxError)
        #     iterable = self._parse_expression()
        #     execution_block = self._parse_block()
        #     return ForStatement(position, iterator, iterable, execution_block)
        # elif self.current_token.get_type() == TokenType.WHILE:  # _parse_while_statement() TODO: DONE!
        #     position = self.current_token.get_position()
        #     self.consume_token()
        #     self._must_be_and_consume(TokenType.OPENING_BRACKET, SyntaxError)
        #     condition = self._parse_expression()
        #     self._must_be_and_consume(TokenType.CLOSING_BRACKET, SyntaxError)
        #     execution_block = self._parse_block()
        #     return WhileStatement(position, condition, execution_block)
        # else:
        #     return None