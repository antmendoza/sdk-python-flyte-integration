from __future__ import annotations

import copy

from flytekit import dynamic, workflow
from serverlessworkflow.sdk.function import Function
from serverlessworkflow.sdk.state import State
from serverlessworkflow.sdk.workflow import Workflow

from flyte.src.context import Context
from flyte.src.states import inject_state, operation_state, foreach_state


@dynamic
def execute_swf(wf: dict, data: dict) -> dict:
    """
    Iterate over the states"""

    wf_object: Workflow = Workflow.from_source(str(wf))

    state_data = copy.copy(data)

    functions: [Function] = wf_object.functions

    context = Context(functions=functions)
    state: State
    if wf_object.states:
        for state in wf_object.states:
            input_state_data = copy.deepcopy(state_data)
            if state.is_inject_state():
                state_data = inject_state(context=context, state=state, input_data=input_state_data)
            elif state.is_operation_state():
                state_data = operation_state(context=context, state=state, input_data=input_state_data)
            elif state.is_foreach_state():
                state_data = foreach_state(context=context, state=state, input_data=input_state_data)
            else:
                raise Exception(f"state {state.type} not supported")

    return state_data


@workflow
def swf(wf: dict, data: dict = {}) -> dict:
    """
    Calls the dynamic workflow and returns the result
    Params:
    - wf: the workflow, based on the serverlessworkflow specification, to be executed
    - data: the initial workflow data
    """
    return execute_swf(wf=wf, data=copy.deepcopy(data))
