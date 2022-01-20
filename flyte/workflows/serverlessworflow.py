from flytekit import dynamic, workflow


@dynamic
def execute_swf(wf: dict) -> dict:
    """
    Calls the required tasks and returns the final result"""

    result = {}

    # looping through the string s1
    for i in range(len(str(wf))):
        result['mynewkey' + str(i)] = i

    return result


@workflow
def swf(wf: dict) -> dict:
    """
    Calls the dynamic workflow and returns the result"""

    # sending two strings to the workflow
    return execute_swf(wf=wf)


if __name__ == "__main__":
    print(swf(wf={}))
