#!/bin/bash
echo "deploying..."
flytectl create execution --project flytesnacks --domain development --execFile swf_spec.yaml

echo "to check the status \n"
echo "flytectl get execution --project flytesnacks --domain development <execname>"
