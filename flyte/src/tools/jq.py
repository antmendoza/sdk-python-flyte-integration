import jq


class JQ:

    def __init__(self, expression: str):
        self.expresion = expression
        self.jq_compiled = jq.compile(expression.replace("$", "").replace("{", "").replace("}", ""))

    def execute(self, data: dict):
        return self.jq_compiled.input(data).all();
