from unittest import TestCase

from flyte.src.custom_function import CustomFunction


def task1():
    return "Task 1 invoked"


class TestCustomFunction(TestCase):
    def test_custom_function(self):
        operation = "flyte.test.test_custom_function#task1"
        result = CustomFunction(operation=operation).invoke()

        self.assertEqual("Task 1 invoked", result)
