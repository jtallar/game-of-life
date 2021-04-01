#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters. Run with ./rule1.sh fill repetitions"
    exit 1
fi
for i in {1..$(seq 1 $2)}
do
    ./target/tp2-simu-1.0/life.sh -Drule="<.3/=.3" -Dsize=101 -Dinit=41 -Ddim=2 -Dpel=true -Dcenter=true -Dfill=$1 > /dev/null
    python3.8 analysis.py < data
    echo '--------------------------------------------------------------'
done