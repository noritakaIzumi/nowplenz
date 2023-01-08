#!/usr/bin/env ash

apk update
apk add zip
pip install --upgrade pip

cd /tmp

pip install --no-cache-dir boto3 -t python && zip -r boto3.zip python && rm -rf python
pip install --no-cache-dir mypy-boto3-iam -t python && zip -r mypy-boto3-iam.zip python && rm -rf python
pip install --no-cache-dir beautifulsoup4 -t python && zip -r beautifulsoup4.zip python && rm -rf python

cd -
mkdir -p build/layers

cp /tmp/boto3.zip build/layers
cp /tmp/mypy-boto3-iam.zip build/layers
cp /tmp/beautifulsoup4.zip build/layers
