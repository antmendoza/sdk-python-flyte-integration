def solveMathExpression(data: dict) -> dict:
    return eval(data["expression"])


def retrieveExpressions(data: dict) -> dict:
    return {
        "expressions": [
            "2+2",
            "4-1",
            "10*3",
            "20/2"
        ]
    }
