#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters. Run with ./rule-analysis.sh rule_number fill"
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

./target/tp2-simu-1.0/life.sh -Drule="$RULE" -Dsize=101 -Dinit=41 -Ddim="$DIM" -Dpel=true -Dcenter=true -Dfill=$2
python3.8 analysis.py plot < data
