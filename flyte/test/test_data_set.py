import json
import os
import unittest
from os import listdir

from flyte.src.main import swf


class DataSet:
    def __init__(self, directory: str, file: str):
        wf_file = os.path.join(os.path.dirname(__file__), directory, file)

        with open(wf_file, "r") as swf_file:
            test = json.loads(swf_file.read())
            self.workflow = test["workflow"]
            self.input_data = test["input_data"]
            self.expected_result = test["expected_result"]


class TestWorkflow(unittest.TestCase):

    def test_data_set(self):
        data_set_location = './data_set/'
        data_set_dir = os.path.join(os.path.dirname(__file__), data_set_location)
        data_set_files = listdir(data_set_dir)
        self.assertEqual(len(data_set_files), 4)

        for file_name in data_set_files:
            with self.subTest(f"test_{file_name}"):
                test: DataSet = DataSet(data_set_location, file_name)
                result = swf(wf=test.workflow, data=test.input_data)

                self.assertEqual(test.expected_result, result, f"Error testing: {file_name}")