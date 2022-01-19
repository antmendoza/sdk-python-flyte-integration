#!/bin/bash

set -e

TAG=flyte:v1


while getopts t: flag
do
    case "${flag}" in
        t) TAG=${OPTARG};;
        h) echo "Usage: ${0} [-h|[-t <tag>]]"
           echo "  t = TAG of the build image"
           exit 1;;
    esac
done


flytectl sandbox exec -- docker build . --tag ${TAG}

echo "Docker image built with tag ${TAG}. You can use this image to run pyflyte package."
