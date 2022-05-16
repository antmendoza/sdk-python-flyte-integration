from __future__ import annotations

import copy

from flytekit import task
from serverlessworkflow.sdk.action import Action
from serverlessworkflow.sdk.foreach_state import ForEachState
from serverlessworkflow.sdk.inject_state import InjectState
from serverlessworkflow.sdk.operation_state import OperationState
from serverlessworkflow.sdk.workflow import Workflow

from flyte.src.context import Context
from flyte.src.custom_function import CustomFunction
from flyte.src.function_factory import FunctionFactory
from flyte.src.tools.jq import JQ


@task
def operation_state(wf: dict, state: dict, input_data: dict) -> dict:
    context = build_context(wf)

    state_data = copy.deepcopy(input_data)

    result = {}

    op_state = OperationState(**state)

    action: Action
    for action in op_state.actions:
        function: CustomFunction = FunctionFactory(context.functions, action.functionRef.refName).build()

        arguments = invocation_arguments(action, state_data)
        invocation_result = function.invoke(arguments)
        invocation_result_filtered = apply_action_data_filter(action, invocation_result)
        result.update(invocation_result_filtered)

    return result


@task
def inject_state(wf: dict, state: dict, input_data: dict) -> dict:
    inject_result = InjectState(**state).data
    return inject_result


@task
def foreach_state(wf: dict, state: dict, input_data: dict) -> dict:
    context = build_context(wf)

    state_data = copy.deepcopy(input_data)

    f_state = ForEachState(**state)

    foreach_input_data = JQ(f_state.inputCollection).executeDict(state_data)

    # TODO iterate over actions
    action = f_state.actions[0]

    function: CustomFunction = FunctionFactory(context.functions, action.functionRef.refName).build()

    result = [];
    for foreach_input in foreach_input_data:
        foreach_input = {
            f_state.iterationParam: foreach_input
        }

        arguments = invocation_arguments(action, foreach_input)
        invocation_result = function.invoke(arguments)
        invocation_result_filtered = apply_action_data_filter(action, invocation_result)
        result.append(invocation_result_filtered)

    state_output = {
        f_state.outputCollection: result
    }

    return state_output


def apply_action_data_filter(action: Action, data: dict) -> dict:
    if action.actionDataFilter:
        return JQ(action.actionDataFilter.results).executeString(data)
    return data


def invocation_arguments(action, data) -> dict:
    arguments = None
    if action.functionRef.arguments:
        arguments = JQ(action.functionRef.arguments).executeDict(data)
    return arguments


def build_context(wf) -> Context:
    wf_object: Workflow = Workflow.from_source(str(wf))
    functions = wf_object.functions
    context = Context(functions=functions)
    return context
