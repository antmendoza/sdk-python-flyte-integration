from unittest import TestCase

from jsonpath_ng import parse

from flyte.serverlessworkflow.src.json.json_path import JsonPath


class TestJsonPath(TestCase):

    def test_load_tasks(self):
        data = {
            "person": {
                "name": "John"
            }
        }
        json_data = data
        jsonpath_expression = parse('$.person.name')
        match = jsonpath_expression.find(json_data)

        self.assertEqual("John", match[0].value)

        result = JsonPath("${ .person.name }").execute(data)

        self.assertEqual("John", result)
