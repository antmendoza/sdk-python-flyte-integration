from unittest import TestCase

from flyte.src.tools.jq import JQ


class TestJsonPath(TestCase):

    def test_jq(self):
        expression = "${.person.name}"
        data = {
            "person": {
                "name": "John"
            }
        }
        self.assertEqual("John", JQ(expression).executeDict(data))
