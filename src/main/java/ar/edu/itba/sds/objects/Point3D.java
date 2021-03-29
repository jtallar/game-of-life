package ar.edu.itba.sds.objects;

import java.util.Objects;

public class Point3D {

    private int x;
    private int y;
    private int z;

    public Point3D(final int x, final int y, final int z) {
        this.x = x;
        this.y = y;
        this.z = z;


    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getZ() {
        return z;

    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point3D point3D = (Point3D) o;
        return x == point3D.x && y == point3D.y && z == point3D.z;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 71 * hash + getX();
        hash = 71 * hash + getY();
        return 71 * hash + getZ();
    }
}
