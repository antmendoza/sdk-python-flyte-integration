import unittest

from flyte.workflows.serverlessworflow import swf


class TestWorkflow(unittest.TestCase):

    def test_swf(self):
        result = swf(wf=
        {
            "id": "helloworld",
            "version": "1.0",
            "specVersion": "0.8",
            "name": "Hello World Workflow",
            "description": "Inject Hello World",
            "start": "Hello State",
            "states": [
                {
                    "name": "Hello State",
                    "type": "inject",
                    "data": {
                        "result": "Hello World!"
                    },
                    "end": True
                }
            ]
        })

        expected = {
            "result": "Hello World!"
        }
        self.assertEqual(expected, result)
