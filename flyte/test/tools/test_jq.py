from unittest import TestCase

from flyte.src.tools.jq import JQ


class TestJsonPath(TestCase):

    def test_jq_string(self):
        expression = "${.person.name}"
        data = {
            "person": {
                "name": "John"
            }
        }
        self.assertEqual("John", JQ(expression).executeString(data))


    def test_jq_dict(self):
        expression = {
                "name": "${ .person.name }"
              }
        data = {
            "person": {
                "name": "John"
            }
        }
        execute_dict = JQ(expression).executeDict(data)
        self.assertEqual({'name': 'John'}, execute_dict)
