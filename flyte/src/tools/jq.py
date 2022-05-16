import jq


def f(v, data):
    replace = v.replace("$", "", 1).replace("{", "", 1).replace("}", "", 1)
    first = jq.compile(replace).input(data).first()
    return first


class JQ:

    def __init__(self, expression: dict):
        self.expression = expression

    def executeDict(self, data: dict):
        items = self.expression.items()
        items_ = {k: f(v, data) for k, v in items}
        return items_

    def executeString(self, data):
        return f(self.expression, data)
