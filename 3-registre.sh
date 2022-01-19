#!/bin/bash


while getopts v: flag
do
    case "${flag}" in
        v) version=${OPTARG};;
    esac
done

if [ -z "${version}" ]; then
  echo "No version set, run the script with -v <version>"
  exit 0
fi



flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version ${version}

