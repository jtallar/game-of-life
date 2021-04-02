#!/bin/bash
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters." 
    echo "Run with ./rule-multianalysis.sh rule_num fill_start fill_step repetitions"
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
if [ -d "$ROOT_DIR" ]; then
    printf '%s\n' "Removing Directory recursively ($ROOT_DIR)"
    rm -rf "$ROOT_DIR"
fi
mkdir "$ROOT_DIR"

FILL="$2"
while [ "$FILL" -le 100 ]
do
    SIM_DIR="$ROOT_DIR"/"$FILL"
    if [ -d "$SIM_DIR" ]; then
        printf '%s\n' "Removing Directory recursively ($SIM_DIR)"
        rm -rf "$SIM_DIR"
    fi
    mkdir "$SIM_DIR"
    echo "Running $4 times with fill $FILL..."
    for i in $(seq 1 $4)
    do
        ./target/tp2-simu-1.0/life.sh -Drule="$RULE" -Dsize=101 -Dinit=41 -Ddim="$DIM" -Dpel=true -Dcenter=true -Dfill="$FILL" -Dout="$SIM_DIR/data$i"
    done
    echo "-----------------------------------"
    ((FILL = FILL + "$3"))
done

python3.8 multipleAnalysis.py "$ROOT_DIR"