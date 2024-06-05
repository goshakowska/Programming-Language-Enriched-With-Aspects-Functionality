from src.ast_tree.ast_type import AstType
from src.visitor.interpreter_errors import TypeAssignmentError
from src.visitor.interpreter_errors import VariableNameConflictError
from typing import Any


class Value:
    def __init__(self, value: Any, type: AstType) -> None:
        self.value = value
        self.type = type

    def set_value(self, value: 'Value') -> None:
        if value.type == self.type:  # tu i w linijce 28
            self.value = value.value
        else:
            raise TypeAssignmentError(self.value, value, self.type, type(value))

    def get_value(self) -> Any:
        return self.value


class FunctionValue:
    def __init__(self,
                 value: "Args",
                 type: AstType = AstType.TYPE_FUNCTION,
                 return_value: AstType = AstType.NULL) -> None:

        self.value = value
        self.type = type
        self.call_count = 1
        self.return_value = return_value

    @property
    def args(self) -> "Args":
        return self.value

    @property
    def return_value(self) -> AstType:
        return self._return_value


class Args:

    def __init__(self,
                 value: list['Param']) -> None:

        self.value = value

    @property
    def count(self) -> int:
        return len(self.value)


class Param:
    def __init__(self,
                 name: str,
                 value: Any,
                 type: AstType) -> None:

        self.name = name
        self.value = value
        self.type = type

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    @property
    def type(self) -> AstType:
        return self._type


class Scope:
    def __init__(self) -> None:

        self.variables = {}

    def find_and_set_old_variable(self, name: str,  value: Value):  # todo, aby sprawdzać czy zmienny różnych typów o tej samej nazwie
        if name in self.variables.keys():  # two
            if self.variables[name].type == value.type:  # dwa razy sprawdzam to 
                self.variables[name].set_value(value)
                return True
            else:
                existing_variable_type = self.variables[name].type
            raise VariableNameConflictError(name,
                                            value.type,
                                            existing_variable_type)
        return False

    def add_variable(self,
                     name: str,
                     value: Value) -> None:
        if not self.find_and_set_old_variable(name, value):
            self.variables[name] = value

    def get_variable(self,
                     variable_name: str) -> Value:
        if (value := self.variables.get(variable_name)):
            return value
        return None


class CallContext:
    def __init__(self,
                 function_name: str,
                 expected_return_type: Any) -> None:

        self.function_name = function_name
        self.expected_return_type = expected_return_type
        self.scopes = [Scope()]

    def get_variable(self,
                     variable_name: str) -> Value | None:
        for scope in reversed(self.scopes):
            if (value := scope.get_variable(variable_name)) is not None:
                return value
        return None

    def add_variable(self,
                     name: str,
                     value: Value) -> None:
        # check_if_variable_exists
        self.scopes[-1].add_variable(name, value)

    def add_scope(self) -> None:

        self.scopes.append(Scope())

    def delete_scope(self) -> None:

        self.scopes.pop()


class Environment:
    def __init__(self) -> None:

        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.call_contexts = []
        self.nesting_level = 0

    def enter_function_call(self,
                            function_name: str,
                            return_type: Any) -> None:
        self.nesting_level += 1
        self.call_contexts.append(CallContext(function_name, return_type))
        self.current_scope = self.call_contexts[-1].scopes[-1]

    def exit_function_call(self) -> None:
        self.nesting_level -= 1
        self.call_contexts.pop()
        self.current_scope = self.call_contexts[-1].scopes[-1] if len(self.call_contexts) != 0 else self.global_scope

    def check_if_in_call_context(self) -> bool:
        return len(self.call_contexts) != 0

    def enter_block(self) -> None:
        self.call_contexts[-1].add_scope()

    def exit_block(self) -> None:
        self.call_contexts[-1].delete_scope()

    def get_variable(self, variable_name: str) -> Value:
        return self.current_scope.get_variable(variable_name) or self.global_scope.get_variable(variable_name)

    def add_variable(self, name: str, value: Value) -> None:
        self.current_scope.add_variable(name, value)

    def add_global_variable(self, name: str, value: Value) -> None:
        self.global_scope.add_variable(name, value)
    # def create_parameters_scope(self, input_parameters: list, provided_arguments: list) -> None:
    #     initial_scope = Scope(self.current_scope)
    #     # błąd jeśli nie jest taka sama liczba parametrow i argumentów
    #     for parameter, argument in zip(input_parameters, provided_arguments):
    #         initial_scope.variables[parameter.name] = argument

    #     return initial_scope

# class GlobalContext(Scope):
#     def __init__(self):
#         super().__init__()
#         self.variables = {}

#     def find_and_set_old_variable(self, name: str,  value: Value):
#         if name in self.variables.keys():
#             self.variables[name] = value
#             return True
#         return False