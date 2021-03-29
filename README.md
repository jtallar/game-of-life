# Life Simulation
To generate executable and run the life simulation
1. Run `./prepare.sh` in root.
2. Go to output folder `cd target/tp2-simu-1.0`.
3. Run `./life.sh -Dsize=100 -DinitSize=40 -Doccupation=60 -Dseed=10 -Dsteps=Long.MAX_VALUE -Dout=out/test`, where:
    - size is the size of one side of the square matrix
    - initSize is the size of one side of the initial square matrix
    - occupation is the percentage of occupation in the initial square matrix
    - steps are the maximum amount of steps performed
    - our is the filepath prefix for the output files
    - the above are the provided default values, same as running `./life.sh`
4. Run  `./life.sh -Dinit=out/test-2.txt`, where
    - init is the initializer file, sets the amount of living cells and matrix size
    - steps and out can be also added. init replaces size, initSize, occupation and seed
