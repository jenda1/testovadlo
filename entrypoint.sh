#!/bin/bash

set -e

for t in $(find /test.d/ -executable ! -type d | sort -n)
do
	$t || { ret=$?; echo -e "\n** chyba: $ret"; [[ $ret -lt 100 ]] || exit 1; }
done

if [[ -f /test && -x /test ]]
then
	/test || { ret=$?; echo -e "\n** chyba: $ret"; [[ $ret -lt 100 ]] || exit 1; }
fi
