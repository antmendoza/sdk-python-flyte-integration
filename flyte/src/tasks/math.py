def solveMathExpression(data: dict):
    return eval(data["expression"])


def retrieveExpressions(data: dict):
    return {
        "expressions": [
            "2+2",
            "4-1",
            "10*3",
            "20/2"
        ]
    }
