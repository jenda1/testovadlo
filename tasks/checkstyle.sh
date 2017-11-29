#!/bin/bash

java_files=( $(find /data/arg0/ -type f -name '*.java' -print) )

[[ -z "${java_files[@]}" ]] || { \
	echo "$ checkstyle ${java_files[@]#/data/arg0/}"
	out=$(java -jar /lib/checkstyle-8.5-all.jar -c /lib/style.xml "${java_files[@]}") || {
		grep -v '^\(Starting\|Audit done\|Checkstyle ends\)' <<<"$out"
		exit 1
	}
}
