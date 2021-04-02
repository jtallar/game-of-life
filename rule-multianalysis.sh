#!/bin/bash
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters." 
    echo "Run with ./rule-multianalysis.sh rule_num fill repetitions"
    exit 1
fi

case $1 in
  1)
    RULE="=.2.|.=.3/=.3"; DIM=2;;
  2)
    RULE="=.2.|.=.3/=.3.|.=.6"; DIM=2;;
  3)
    RULE="<.3/=.3"; DIM=2;;
  4)
    RULE="=.2.|.=.3/=.3"; DIM=3;;
  5)
    RULE=">.4.&.<.8/=.6"; DIM=3;;
  6)
    RULE=">.3.&.<.6/=.5"; DIM=3;;
  *)
    echo "Invalid rule number, must be between 1 and 6."
    exit 1
    ;;
esac

ROOT_DIR=data_dir
if ! [ -d "$ROOT_DIR" ]; then
    mkdir "$ROOT_DIR"
fi
SIM_DIR="$ROOT_DIR"/"$2"
if [ -d "$SIM_DIR" ]; then
    printf '%s\n' "Removing Directory recursively ($SIM_DIR)"
    rm -rf "$SIM_DIR"
fi
mkdir "$SIM_DIR"

for i in $(seq 1 $3)
do
    ./target/tp2-simu-1.0/life.sh -Drule="$RULE" -Dsize=101 -Dinit=41 -Ddim="$DIM" -Dpel=true -Dcenter=true -Dfill=$2 -Dout="$SIM_DIR/data$i"
done
python3.8 multipleAnalysis.py "$SIM_DIR"