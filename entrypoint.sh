#!/bin/bash

set -e

for t in $(find /test.d/ -executable ! -type d | sort -n)
do
        $t && ret=0 || ret=$?

        echo $ret > $t.exitcode
        [[ $ret -le 10 ]] || exit $((ret-10))
done
