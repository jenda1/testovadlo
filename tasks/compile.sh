#!/bin/bash

mkdir -p /data/build
cd /data/arg0

java_files="$(find . -type f -name '*.java' -print)"

[[ -z "$java_files" ]] || { \
	echo "$ javac " $java_files
	javac  -encoding utf-8 -d /data/build $java_files || exit 1
}
