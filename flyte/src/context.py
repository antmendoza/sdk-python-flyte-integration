from __future__ import annotations

from serverlessworkflow.sdk.function import Function


class Context:
    functions: (str | [Function])

    def __init__(self, functions: (str | [Function])):
        self.functions = functions
