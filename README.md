# Life Simulation
To generate executable and run the life simulation
1. Run `./prepare.sh` in root.
2. Run `./target/tp2-simu-1.0/life.sh -Dsize=100 -Dinit=40 -Dfill=60 -Dseed=10 -Dsteps=Long.MAX_VALUE -Dout=data -Dpel=false -Drule="=.2.|.=.3/=.3" -Ddim=2 -Dmoore=1 -Dcenter=false`, where:
    - `size` square matrix side size
    - `init`: initial square matrix side size 
    - `fill`: initial square matrix occupation percentage
    - `steps`: maximum amount of steps performed
    - `out`: output file filepath
    - `pel`: sets parallel processing
    - `rule`: Survival/Birth rule
    - `dim`: matrix amount of dimensions
    - `moore`: moore neighbour cells depth
    - `center`: true for centered to origin (0, 0, 0) output and input
    - the example above equals to run `./life.sh`
3. [OPTIONAL] Run  `./life.sh -Din=dataIn`, where
    - `in`: initializer file and also output file (must finish in new line)
    - `steps`, `moore`, `pal` and `rule` can be added
    - this method replaces `size`, `init`, `fill`, `seed`, `dim` and `out`


# Animation Tool
Generates `simu.xyz` given a simulation file as input. If simulation file is named `data`, then:
`python3 preprocessing.py < data`

To view the animation, you must open `simu.xyz` with Ovito:
`./bin/ovito simu.xyz`

After configuring column mapping, to render particles as cubes, go to Visual elements -> Particles 
and in Particle display, select `Cube/Box` as Standard shape.

## 2D Column Mapping 
If your simulation is a 2D file, configure the file column mapping as follows:
   - Column 1 - Position - X
   - Column 2 - Position - Y
   - Column 3 - Radius
   - Column 4 - Color - R
   - Column 5 - Color - G
   - Column 6 - Color - B

## 3D Column Mapping
If your simulation is a 3D file, configure the file column mapping as follows:
   - Column 1 - Position - X
   - Column 2 - Position - Y
   - Column 3 - Position - Z
   - Column 4 - Radius
   - Column 5 - Color - R
   - Column 6 - Color - G
   - Column 7 - Color - B