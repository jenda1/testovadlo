#!/bin/bash

cd /data/arg0

java_files="$(find . -type f -name '*.java' -print)"

[[ -z "$java_files" ]] || { \
	echo "$ checkstyle $java_files"
	out=$(java -jar /lib/checkstyle-8.5-all.jar -c /lib/style.xml $java_files) || {
		grep -v '^\(Starting\|Audit done\|Checkstyle ends\)' <<<"$out"
		exit 1
	}
}
