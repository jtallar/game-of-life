# Life Simulation
To generate executable and run the life simulation
1. Run `./prepare.sh` in root.
2. Go to output folder `cd target/tp2-simu-java-1.0-SNAPSHOT`.
3. Run `./tp2-simu.sh -Drc=1 -Dperiodic=false -Dm=10`, where:
    - rc is the radio of interaction to study
    - periodic is the edge periodic condition. If `true`, periodic is activated, otherwise it is deactivated.
    - m is an optional parameter to specify block side count. If not specified, optimal M value will be used.

