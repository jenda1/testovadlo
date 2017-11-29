#!/bin/bash

set -e

for t in $(find /run.d/ -executable ! -type d | sort -n)
do
	$t
done

if [[ -f /run && -x /run ]]
then
	/run
fi
