#!/bin/bash

set -e

for t in $(find /test.d/ -executable ! -type d | sort -n)
do
	$t || echo -e "\n** chyba: $?"
done

if [[ -f /test && -x /test ]]
then
	/test || echo -e "\nchyba: $?"
fi
