#!/bin/bash


echo "deploying..."
flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml


echo "to check the status \n"
echo "flytectl get execution --project flytesnacks --domain development <execname>"
