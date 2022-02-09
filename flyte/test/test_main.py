import unittest

from jsonpath_ng import parse

from flyte.src.main import swf


class TestWorkflow(unittest.TestCase):

    def test_helloworld(self):
        result = swf(wf={
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

    def test_load_tasks(self):
        wf = {
            "id": "greeting",
            "version": "1.0",
            "specVersion": "0.8",
            "name": "Greeting Workflow",
            "description": "Greet Someone",
            "start": "Greet",
            "functions": [
                {
                    "name": "greetingFunction",
                    "operation": "flyte.src.tasks.custom_taks#greeting",
                    "type": "custom"
                }
            ],
            "states": [
                {
                    "name": "Greet",
                    "type": "operation",
                    "actions": [
                        {
                            "functionRef": {
                                "refName": "greetingFunction",
                                "arguments": "${ {name: .person.name } }"
                            },
                            "actionDataFilter": {
                                "results": "${ {greeting: .greeting} }"
                            }
                        }
                    ],
                    "end": True
                }
            ]
        }

        data = {
            "person": {
                "name": "John"
            }
        }

        result = swf(wf=wf, data=data)

        expected = {
            "greeting": "Welcome to Serverless Workflow, John!"
        }

        self.assertEqual(expected, result)
