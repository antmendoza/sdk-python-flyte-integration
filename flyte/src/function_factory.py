from __future__ import annotations

from serverlessworkflow.sdk.function import Function

from flyte.src.custom_function import CustomFunction


class FunctionFactory:
    def __init__(self, functions: (str | [Function]), ref_name: str):
        self.functions = functions
        self.ref_name = ref_name
        self.function: Function = next(x for x in self.functions if x.name == self.ref_name)

    def build(self):
        if self.function.type == "custom":
            return CustomFunction(self.function.operation)

        raise RuntimeError(f'Type ${self.function.type} not supported')