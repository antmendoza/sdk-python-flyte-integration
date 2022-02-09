from __future__ import annotations

import importlib

from flytekit import dynamic, workflow
from serverlessworkflow.sdk.function import Function
from serverlessworkflow.sdk.action import Action
from serverlessworkflow.sdk.inject_state import InjectState
from serverlessworkflow.sdk.operation_state import OperationState
from serverlessworkflow.sdk.state import State
from serverlessworkflow.sdk.workflow import Workflow

from flyte.src.context import Context


class ExecutableFunction:

    def __init__(self, function: Function):
        self.function = function

    def execute(self, data: dict):
        pass


class ResolveFunction:
    def __init__(self, functions: (str | [Function]), ref_name: str):
        self.functions = functions
        self.ref_name = ref_name

    @property
    def function(self) -> ExecutableFunction:
        function: Function = next(x for x in self.functions if x.name == self.ref_name)
        return ExecutableFunction(function)


def operation_state(context: Context, state: OperationState):
    action: Action
    for action in state.actions:
        print(action)
        ref_name = action.functionRef.refName
        function: ExecutableFunction = ResolveFunction(context.functions, ref_name).function
        print(function)

    module = importlib.import_module('flyte.src.tasks.custom_taks')
    my_class = getattr(module, 'Task')
    my_instance = my_class()
    return my_instance.task4()


def inject_state(context: Context, state: InjectState):
    inject_result = state.data
    return inject_result


@dynamic
def execute_swf(wf: dict, data: dict) -> dict:
    """
    Execute the required states and returns the final result"""

    wf_object: Workflow = Workflow.from_source(str(wf))

    result = {}

    functions: [Function] = wf_object.functions

    context = Context(functions=functions)
    state: State
    if wf_object.states:
        for state in wf_object.states:
            if state.type == 'inject':
                result.update(inject_state(context, state))
            if state.type == 'operation':
                result.update(operation_state(context, state))

    return result


@workflow
def swf(wf: dict, data: dict = {}) -> dict:
    """
    Calls the dynamic workflow and returns the result"""
    return execute_swf(wf=wf, data=data)
