#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters." 
    echo "Run with ./rule-multianalysis.sh fill repetitions"
    exit 1
fi

ROOT_DIR=data_dir
if ! [ -d "$ROOT_DIR" ]; then
    mkdir "$ROOT_DIR"
fi
SIM_DIR="$ROOT_DIR"/"$1"
if [ -d "$SIM_DIR" ]; then
    printf '%s\n' "Removing Directory recursively ($SIM_DIR)"
    rm -rf "$SIM_DIR"
fi
mkdir "$SIM_DIR"

for i in $(seq 1 $2)
do
    ./target/tp2-simu-1.0/life.sh -Drule="=.2.|.=.3/=.3" -Dsize=101 -Dinit=41 -Ddim=2 -Dpel=true -Dcenter=true -Dfill=$1 -Dout="$SIM_DIR/data$i"
done
python3.8 multipleAnalysis.py "$SIM_DIR"