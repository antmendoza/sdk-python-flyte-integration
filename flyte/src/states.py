from __future__ import annotations

import copy

from flytekit import task
from serverlessworkflow.sdk.action import Action
from serverlessworkflow.sdk.foreach_state import ForEachState
from serverlessworkflow.sdk.inject_state import InjectState
from serverlessworkflow.sdk.operation_state import OperationState

from flyte.src.context import Context
from flyte.src.custom_function import CustomFunction
from flyte.src.function_factory import FunctionFactory
from flyte.src.tools.jq import JQ


@task()
def operation_state(context: Context, state: OperationState, input_data: dict) -> dict:
    state_data = copy.deepcopy(input_data)

    result = {}

    action: Action
    for action in state.actions:
        function: CustomFunction = FunctionFactory(context.functions, action.functionRef.refName).build()

        arguments = invocation_arguments(action, state_data)
        invocation_result = function.invoke(arguments)
        invocation_result_filtered = apply_action_data_filter(action, invocation_result)
        result.update(invocation_result_filtered)

    return result


@task()
def inject_state(context: Context, state: InjectState, input_data: dict) -> dict:
    inject_result = state.data
    return inject_result


@task()
def foreach_state(context: Context, state: ForEachState, input_data: dict) -> dict:
    state_data = copy.deepcopy(input_data)

    foreach_input_data = JQ(state.inputCollection).execute(state_data)

    # TODO iterate over actions
    action = state.actions[0]

    function: CustomFunction = FunctionFactory(context.functions, action.functionRef.refName).build()

    result = [];
    for foreach_input in foreach_input_data:
        foreach_input = {
            state.iterationParam: foreach_input
        }

        arguments = invocation_arguments(action, foreach_input)
        invocation_result = function.invoke(arguments)
        invocation_result_filtered = apply_action_data_filter(action, invocation_result)
        result.append(invocation_result_filtered)

    state_output = {
        state.outputCollection: result
    }

    return state_output


def apply_action_data_filter(action: Action, data: dict):
    if action.actionDataFilter:
        return JQ(action.actionDataFilter.results).execute(data)
    return data


def invocation_arguments(action, data):
    arguments = None
    if action.functionRef.arguments:
        arguments = JQ(action.functionRef.arguments).execute(data)
    return arguments
