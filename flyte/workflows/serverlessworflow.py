from flytekit import dynamic, workflow
from serverlessworkflow.sdk.inject_state import InjectState
from serverlessworkflow.sdk.workflow import Workflow


@dynamic
def execute_swf(wf: dict) -> dict:
    """
    Execute the required states and returns the final result"""

    wf_object: Workflow = Workflow.from_source(str(wf))

    result = {}

    state: State
    for state in wf_object.states:
        if state.type == 'inject':
            result.update(inject_state(state))

    return result


def inject_state(state: InjectState):
    inject_result = state.data
    return inject_result


@workflow
def swf(wf: dict) -> dict:
    """
    Calls the dynamic workflow and returns the result"""

    return execute_swf(wf=wf)

