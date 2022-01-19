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

TAG=flyte:${version}
echo "Using tag=${TAG}"

rm ./flyte-package.tgz

pyflyte --pkgs flyte.workflows package --image ${TAG}
