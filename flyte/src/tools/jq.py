import jq


class JQ:

    def __init__(self, expression: str):
        self.expression = expression
        self.jq_compiled = jq.compile(expression
                                      .replace("$", "", 1)
                                      .replace("{", "", 1)
                                      .replace("}", "", 1))

    def execute(self, data: dict):
        return self.jq_compiled.input(data).first();
