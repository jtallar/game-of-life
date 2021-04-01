import sys

def corners(f, dim, Ni, M):
    C = '1e-10'
    REF = -(int(Ni)-1)/2     # '-0.3'    
    RGB = '0 255 0'
    N = (int(Ni))/2 +0.3       #int(Ni) + 0.3
    if dim == 2:
        M_new = M+4
        corner = f'\n\n{REF} {REF} {C} {RGB}\n{REF} {N} {C} {RGB}\n{N} {REF} {C} {RGB}\n{N} {N} {C} {RGB}\n'
    elif dim == 3:
        M_new = M+8

        corner = f'\n\n{REF} {REF} {REF} {C} {RGB}\n{REF} {REF} {N} {C} {RGB}\n{REF} {N} {REF} {C} {RGB}\n{REF} {N} {N} {C} {RGB}\n{N} {REF} {REF} {C} {RGB}\n{N} {REF} {N} {C} {RGB}\n{N} {N} {REF} {C} {RGB}\n{N} {N} {N} {C} {RGB}\n'
    f.write(str(M_new))
    f.write(corner)

f = open("simu.xyz", "w")
L = ' 0.3 '
M = 0
restart = False
init = 0
for linenum, line in enumerate(sys.stdin):
    if linenum == 0:
        dim = int(line.rstrip())
        continue
    elif linenum == 1:
        N = int(line.rstrip())
        continue
    if restart:
        M = int(line.rstrip())
        corners(f, dim, str(N), M)
        restart = False
        init = linenum
        continue
    if "*" == line.rstrip():
        restart = True
        continue

    if (linenum-init) <= M:
        color = line.rstrip("\n").split(' ')
        if dim==3:
            num = abs(int(color[0])) + abs(int(color[1])) +abs(int(color[2]))
        elif dim==2:
            num = abs(int(color[0])) + abs(int(color[1]))
        RGB = ' ' + str(0.7+num/(N/5)) + ' ' + str(num/(N/2)) + ' ' + str(num/N)
        wline = line.rstrip("\n")+L+RGB+'\n'
        f.write(wline)