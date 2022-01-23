#!/usr/bin/env sh

apk update && apk add make zip
make && echo "Package successfully created!"
