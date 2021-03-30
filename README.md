# Life Simulation
To generate executable and run the life simulation
1. Run `./prepare.sh` in root.
2. Go to output folder `cd target/tp2-simu-1.0`.
3. Run `./life.sh -Dsize=100 -Dinit=40 -Dfill=60 -Dseed=10 -Dsteps=Long.MAX_VALUE -Dout=data -Dpel=false -Drule="=.2.|.=.3/=.3" -Ddim=2 -Dmoore=1`, where:
    - `size` square matrix side size
    - `init`: initial square matrix side size 
    - `fill`: initial square matrix occupation percentage
    - `steps`: maximum amount of steps performed
    - `out`: output file filepath
    - `pel`: sets parallel processing
    - `rule`: Survival/Birth rule
    - `dim`: matrix amount of dimensions
    - `moore`: moore neighbour cells depth
    - the example above equals to run `./life.sh`
4. Run  `./life.sh -in=dataIn`, where
    - `in`: initializer file and also output file (must finish in new line)
    - `steps`, `moore`, `parallel` and `rule` can be added
    - this method replaces `size`, `initSize`, `occupation`, `seed`, `dimension` and `out`

