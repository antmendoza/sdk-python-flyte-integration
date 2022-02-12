# Serverless Workflow integration with flyte

This is a PCO to demonstrate how to execute [Serverless Workflow Specification DLSs](https://github.com/serverlessworkflow/specification) 
into the [Flyte workflow engine](https://flyte.org/).

Full support to the Serverless Workflow Specification is not provided.

## Execution

The [`@workflow` function](./flyte/src/main.py) accepts two parameters:
- `wf` the workflow we want to execute
- `data` (optional) the initial workflow data


## Examples
Examples of the tested workflows can be found here: [specs](./flyte/test/specs) 

The [test_specs.py](./flyte/test/test_specs.py) test execute every spec file under the [specs](./flyte/test/specs) folder. 
Each spec has three sections: 
- `data`: the initial workflow data
- `wf`: the workflow to be executed
- `expected_output`: the expected output after running the `wf` with the provided `data`

You can run any of the examples into flyte by providing the `wf` and `data` parameters.

[swf_spec.yaml](./swf_spec.yaml)

```
inputs:
  wf: {
    "id": "solvemathproblems",
    "version": "1.0",
    "specVersion": "0.8",
    "name": "Solve Math Problems Workflow",
    "description": "Solve math problems",
    "start": "Solve",
    "functions": [
      {
        "name": "solveMathExpressionFunction",
        "operation": "flyte.src.tasks.math#solveMathExpression",
        "type": "custom"
      }
    ],
    "states": [
      {
        "name": "Solve",
        "type": "foreach",
        "inputCollection": "${ .expressions }",
        "iterationParam": "singleexpression",
        "outputCollection": "results",
        "actions": [
          {
            "functionRef": {
              "refName": "solveMathExpressionFunction",
              "arguments": "${ {expression: .singleexpression} }"
            }
          }
        ],
        "end": true
      }
    ]
  }
  data: {
    "expressions": [
      "2+2",
      "4-1",
      "10*3",
      "20/2"
    ]
  }

```


## Supported states

| State     | Supported |
| --------- |-----------|
| Event     | No        |
| Operation | WIP       |
| Switch    | No        |
| Sleep     | No        |
| Parallel  | No        |
| Inject    | WIP       |
| ForEach   | WIP       |
| Callback  | No        |



