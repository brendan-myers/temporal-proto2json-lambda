#!/bin/bash

rm proto2json.zip

# install dependencies in ./package
mkdir package
pip install --target ./package boto3
pip install --target ./package protobuf
pip install --target ./package --platform manylinux2014_aarch64 --only-binary=:all: temporalio

# create zip of all dependencies
cd package
zip -r ../proto2json.zip . 

# add lambda function/handler to zip
cd ..
zip proto2json.zip lambda_function.py