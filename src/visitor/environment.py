from src.ast_tree.ast_type import AstType
from src.visitor.interpreter_errors import TypeAssignmentError
from src.visitor.interpreter_errors import VariableNameConflictError
from src.visitor.interpreter_errors import ReadOnlyAttributeError
from src.visitor.interpreter_errors import NotInitializedError
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.visitor.interpreter import Interpreter


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


class ReadOnlyDescriptor:
    def __init__(self, attribute_name):
        self._attribute_name = attribute_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__.get(self._attribute_name)
        if value is None:
            raise NotInitializedError(self._attribute_name)
        return value

    def __set__(self, instance, value):
        if not instance.__dict__.get(f'_{self._attribute_name}_initialized', False) or instance._is_updating():
            instance.__dict__[self._attribute_name] = value
            instance.__dict__[f'_{self._attribute_name}_initialized'] = True
        else:
            raise ReadOnlyAttributeError(self._attribute_name)


class AspectValue:
    def __init__(self, function_name, function_target) -> None:
        # self.name = name
        self.type = AstType.TYPE_ASPECT
        self.targets = {function_name: function_target}
        self.enable = True

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, value: bool):
        if isinstance(value, bool):
            self._enable = value
        else:
            raise ValueError("Enable must be a boolean value")

    @property
    def disable(self):
        self._enable = False


class FunctionValue:

    name = ReadOnlyDescriptor('name')
    args = ReadOnlyDescriptor('args')
    returnValue = ReadOnlyDescriptor('return_value')
    returnType = ReadOnlyDescriptor('return_type')
    callCount = ReadOnlyDescriptor('call_count')
    type = ReadOnlyDescriptor('type')

    def __init__(self, name, args, return_value=None, return_type=AstType.NULL):
        self._set_updating(True)  # Start updating
        self.name = name
        self.args = args
        self.returnValue = return_value
        self.returnType = return_type
        self.callCount = Value(1, AstType.INT)
        self.type = AstType.TYPE_FUNCTION
        self._set_updating(False)  # Stop updating

    def _is_updating(self):
        return self.__updating

    def _set_updating(self, value):
        self.__updating = value

    def accept_updater(self, updater: "Interpreter", **kwargs):
        updater.update_targeted_function(self, **kwargs)

    def increment_call_count(self) -> None:
        new_call_count = self.callCount.get_value() + 1
        self.callCount = Value(new_call_count, AstType.INT)


class Args:

    def __init__(self,
                 value: list['Param']) -> None:

        self.value = value

    @property
    def count(self) -> int:
        return Value(len(self.value), AstType.INT)


class Param:
    def __init__(self,
                 name: str,
                 value: Any,
                 type: AstType) -> None:

        self.name = name
        self.value = value
        self.type = type


class Scope:
    def __init__(self) -> None:

        self.variables = {}

    def find_and_set_old_variable(self, name: str,  value: Value):
        if name in self.variables.keys():  # two
            if self.variables[name].type == value.type:
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
                     value: Value | FunctionValue) -> None:
        if not self.find_and_set_old_variable(name, value):
            self.variables[name] = value

    def add_function_variable(self, name: str, value: FunctionValue) -> None:
        self.variables.update({name: value})

    def get_variable(self,
                     variable_name: str) -> Value | FunctionValue:
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
        self.current_scope = self.call_contexts[-1].scopes[-1] \
            if len(self.call_contexts) != 0 else self.global_scope

    def check_if_in_call_context(self) -> bool:
        return len(self.call_contexts) != 0

    def enter_block(self) -> None:
        self.call_contexts[-1].add_scope()

    def exit_block(self) -> None:
        self.call_contexts[-1].delete_scope()

    def get_variable(self, variable_name: str) -> Value:
        return self.current_scope.get_variable(variable_name) or\
              self.global_scope.get_variable(variable_name)

    def add_variable(self, name: str, value: Value) -> None:
        self.current_scope.add_variable(name, value)

    def check_for_global_aspect(self, name: str) -> bool:
        if name in self.global_scope.variables.keys()\
         and self.global_scope.variables[name].type == AstType.TYPE_ASPECT:
            return self.global_scope.variables.get(name)
        else:
            return None

    def add_global_variable(self, name: str, value: Any) -> None:
        self.global_scope.add_variable(name, value)

    def add_function_variable(self, name: str, value: FunctionValue) -> None:
        self.current_scope.add_function_variable(name, value)

    def enter_aspect_block(self, targeted_function: FunctionValue) -> None:
        self.call_contexts[-1].add_scope()
        self.add_function_variable("function", targeted_function)