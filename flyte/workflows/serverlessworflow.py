from flytekit import dynamic, workflow
from serverlessworkflow.sdk.workflow import Workflow


@dynamic
def execute_swf(wf: dict) -> dict:
    """
    Calls the required tasks and returns the final result"""

    swf = Workflow.from_source(str(wf))

    result = {'id': swf.id}

    # looping through the string s1
    for i in range(len(str(wf))):
        pass
        #result['mynewkey' + str(i)] = i

    return result


@workflow
def swf(wf: dict) -> dict:
    """
    Calls the dynamic workflow and returns the result"""

    # sending two strings to the workflow
    return execute_swf(wf=wf)


if __name__ == "__main__":
    print(swf(wf=
    {
        "id": "helloworld",
        "version": "1.0",
        "specVersion": "0.8",
        "name": "Hello World Workflow",
        "description": "Inject Hello World",
        "start": "Hello State",
        "states": [
            {
                "name": "Hello State",
                "type": "inject",
                "data": {
                    "result": "Hello World!"
                },
                "end": True
            }
        ]
    }
    ))
