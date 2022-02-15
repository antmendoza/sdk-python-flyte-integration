import json
import os
import unittest
from os import listdir

from flyte.src.main import swf


class Spec:
    def __init__(self, directory: str, file: str):
        wf_file = os.path.join(os.path.dirname(__file__), directory, file)

        with open(wf_file, "r") as swf_file:
            test = json.loads(swf_file.read())
            self.workflow = test["wf"]
            self.input_data = test["data"]
            self.expected_result = test["expected_result"]


class TestWorkflow(unittest.TestCase):

    def test_data_set(self):
        specs_location = './specs/'
        specs_dir = os.path.join(os.path.dirname(__file__), specs_location)
        specs_files = listdir(specs_dir)
        self.assertEqual(len(specs_files), 4)

        for file_name in specs_files:
            with self.subTest(f"test_{file_name}"):
                spec: Spec = Spec(specs_location, file_name)
                result = swf(wf=spec.workflow, data=spec.input_data)

                self.assertEqual(spec.expected_result, result, f"Error testing: {file_name}")
