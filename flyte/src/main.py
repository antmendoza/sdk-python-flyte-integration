import importlib

from flytekit import dynamic, workflow
from serverlessworkflow.sdk.function import Function
from serverlessworkflow.sdk.inject_state import InjectState
from serverlessworkflow.sdk.operation_state import OperationState
from serverlessworkflow.sdk.state import State
from serverlessworkflow.sdk.workflow import Workflow


def operation_state(state: OperationState):
    module = importlib.import_module('flyte.src.tasks.custom_taks')
    my_class = getattr(module, 'Task')
    my_instance = my_class()
    return my_instance.task4()


def inject_state(state: InjectState):
    inject_result = state.data
    return inject_result


@dynamic
def execute_swf(wf: dict, data: dict) -> dict:
    """
    Execute the required states and returns the final result"""

    wf_object: Workflow = Workflow.from_source(str(wf))

    result = {}

    functions: [Function] = wf_object.functions

    state: State
    if wf_object.states:
        for state in wf_object.states:
            if state.type == 'inject':
                result.update(inject_state(state))
            if state.type == 'operation':
                result.update(operation_state(state))

    return result


@workflow
def swf(wf: dict, data: dict = {}) -> dict:
    """
    Calls the dynamic workflow and returns the result"""
    return execute_swf(wf=wf, data=data)


