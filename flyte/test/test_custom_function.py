from unittest import TestCase

from flyte.src.custom_function import CustomFunction

def task1(data: dict):
    return "Hello " + data["name"];


class TestCustomFunction(TestCase):
    def test_custom_function(self):
        operation = "flyte.test.test_custom_function#task1"
        result = CustomFunction(operation=operation).invoke({"name": "Antonio"})

        self.assertEqual("Hello Antonio", result)
