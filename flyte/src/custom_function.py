from __future__ import annotations

import importlib


class CustomFunction:
    def __init__(self, operation: str):
        self.operation = operation

    def invoke(self):
        operation_parts = self.operation.split("#")
        module_ = operation_parts[0]
        function = operation_parts[1]
        module_instance = importlib.import_module(module_)
        function_instance = getattr(module_instance, function)
        return function_instance()