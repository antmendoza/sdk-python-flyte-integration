#!/bin/bash


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


echo "Using tag=${TAG}"


pyflyte --pkgs flyte.workflows package --image ${TAG}  --force #--fast
