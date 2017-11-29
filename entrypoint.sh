#!/bin/bash

set -e

for t in $(find /test.d/ -executable ! -type d | sort -n)
do
	$t
done

if [[ -f /test && -x /test ]]
then
	/test
fi
