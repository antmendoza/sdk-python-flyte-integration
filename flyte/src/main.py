from __future__ import annotations

from flytekit import dynamic, workflow
from serverlessworkflow.sdk.function import Function
from serverlessworkflow.sdk.state import State
from serverlessworkflow.sdk.workflow import Workflow

from flyte.src.context import Context
from flyte.src.states import inject_state, operation_state, foreach_state


@dynamic
def execute_swf(wf: dict, data: dict) -> dict:
    """
    Execute the required states and returns the final result"""

    wf_object: Workflow = Workflow.from_source(str(wf))

    result = data

    functions: [Function] = wf_object.functions

    context = Context(functions=functions)
    state: State
    if wf_object.states:
        for state in wf_object.states:
            if state.type == 'inject':
                result = (inject_state(context, state, result))
            elif state.type == 'operation':
                result = (operation_state(context, state, result))
            elif state.type == 'foreach':
                result = (foreach_state(context, state, result))
            else:
                raise Exception(f"state {state.type} not supported")

    return result


@workflow
def swf(wf: dict, data: dict = {}) -> dict:
    """
    Calls the dynamic workflow and returns the result"""
    return execute_swf(wf=wf, data=data)
