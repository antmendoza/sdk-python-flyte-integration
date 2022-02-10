def greeting(data: dict):
    return {
        "greeting": f"Welcome to Serverless Workflow, {data['name']}!"
    }


def solveMathExpression(data: dict):
    return {"results": eval(data["expression"])}
