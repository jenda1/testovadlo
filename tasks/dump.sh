#!/bin/bash

echo "/data"
for f in $(find /data -type f); do
	echo $f:
	perl -ple '$_="  ".$_' $f
	echo
done
