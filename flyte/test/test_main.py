import json
import os
import unittest

from flyte.src.main import swf


class TestWorkflow(unittest.TestCase):

    def test_helloworld(self):
        wf = self.read_file_as_json('helloworld.json')
        expected = {
            "result": "Hello World!"
        }
        self.assertEqual(expected, swf(wf=wf))

    def test_load_tasks(self):
        wf = self.read_file_as_json('greeting.json')
        data_input = {
            "person": {
                "name": "John"
            }
        }
        result = swf(wf=wf, data=data_input)
        expected = {
            "greeting": "Welcome to Serverless Workflow, John!"
        }
        self.assertEqual(expected, result)

    def read_file_as_json(self, file):
        wf_file = os.path.join(os.path.dirname(__file__), './', file)

        with open(wf_file, "r") as swf_file:
            wf = swf_file.read()
        return json.loads(wf)
