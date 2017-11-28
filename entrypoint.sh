#!/bin/bash

set -e

if [[ -f /run && -x /run ]]
then
	/run
fi

for t in $(find /run.d/ -executable ! -type d)
do
	$t
done
