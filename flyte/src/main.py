from __future__ import annotations

from flytekit import dynamic, workflow
from serverlessworkflow.sdk.action import Action
from serverlessworkflow.sdk.function import Function
from serverlessworkflow.sdk.inject_state import InjectState
from serverlessworkflow.sdk.foreach_state import ForEachState
from serverlessworkflow.sdk.operation_state import OperationState
from serverlessworkflow.sdk.state import State
from serverlessworkflow.sdk.workflow import Workflow

from flyte.src.context import Context
from flyte.src.custom_function import CustomFunction
from flyte.src.function_factory import FunctionFactory
from flyte.src.tools.jq import JQ


def operation_state(context: Context, state: OperationState, data: dict):
    result = {}

    action: Action
    for action in state.actions:
        ref_name = action.functionRef.refName
        function: CustomFunction = FunctionFactory(context.functions, ref_name).build()

        arguments = None
        if action.functionRef.arguments:
            arguments = JQ(action.functionRef.arguments).execute(data)

        function_invocation = function.invoke(arguments)

        if action.actionDataFilter:
            function_invocation = JQ(action.actionDataFilter.results).execute(function_invocation)

        result.update(function_invocation)

    return result


def inject_state(context: Context, state: InjectState, data: dict):
    inject_result = state.data
    return inject_result


def foreach_state(context: Context, state: ForEachState, data: dict):
    input_data = JQ(state.inputCollection).execute(data)

    # TODO iterate over actions
    action = state.actions[0]
    ref_name = action.functionRef.refName
    function: CustomFunction = FunctionFactory(context.functions, ref_name).build()

    result = [];
    for input_ in input_data:
        input_ = {
            state.iterationParam: input_
        }

        function_argument = JQ(action.functionRef.arguments).execute(input_)
        function_invocation = function.invoke(function_argument)
        # invocation_result = JQ(state.outputCollection).execute(function_invocation)
        result.append(function_invocation)

    state_output = {
        state.outputCollection: result
    }

    return state_output


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
                result.update(inject_state(context, state, data))
            elif state.type == 'operation':
                result.update(operation_state(context, state, data))
            elif state.type == 'foreach':
                result.update(foreach_state(context, state, data))
            else:
                raise Exception(f"state {state.type} not supported")

    return result


@workflow
def swf(wf: dict, data: dict = {}) -> dict:
    """
    Calls the dynamic workflow and returns the result"""
    return execute_swf(wf=wf, data=data)
