package ar.itba.edu.sds;

import java.util.*;
import java.util.function.Consumer;
import java.util.stream.IntStream;

public class Life {

    public static void main(String[] args) {

        // read properties
        Properties properties = System.getProperties();

        // initial matrix size
        int matrixSide = Integer.parseInt(properties.getProperty("size", "100"));

        // region size to be set out as initial zone has to be par or not according to initial matrix size
        int initialMatrixSide = Integer.parseInt(properties.getProperty("initSize", "40"));

        // occupation percentage level of initial zone
        int initialOccupationPercentage = Integer.parseInt(properties.getProperty("occupation", "60"));

        // seed for random generated positions
        long randomSeed = Long.parseLong(properties.getProperty("seed", String.valueOf(System.nanoTime())));

        // self explanatory
        boolean isThreeD = Boolean.parseBoolean(properties.getProperty("3D", "false"));


        // initialize set
        final HashSet<Integer> set = initializeMatrix(matrixSide, initialMatrixSide, initialOccupationPercentage, randomSeed, isThreeD);

        printAliveCells(set, matrixSide);


    }

    /**
     * Initializes de matrix given the params taken
     * @param matrixSide The whole matrix side value
     * @param initialMatrixSide The initial matrix side value. Should be less than @param matrixSide
     * @param initialOccupationPercentage The initial occupation percentage for the initial matrix
     * @param randomSeed Random seed for shuffling
     * @param isThreeD True in case is a 3-Dimensional matrix, false if it is 2-Dimensional
     * @return The HashSet with the values
     */
    protected static HashSet<Integer> initializeMatrix(final int matrixSide, final int initialMatrixSide, final int initialOccupationPercentage, final long randomSeed, final boolean isThreeD) {

        // auxiliary variables for posterior use
        final List<Integer> init = new ArrayList<>((int) Math.pow(initialMatrixSide, ((isThreeD) ? 3 : 2)));
        final int offsetStart = (matrixSide - initialMatrixSide) / 2;
        final int offsetEnd = offsetStart + initialMatrixSide;

        // TODO this could be prettier
        if (isThreeD) {
            for (int z = offsetStart; z < offsetEnd; z++)
                for (int y = offsetStart; y < offsetEnd; y++)
                    for (int x = offsetStart; x < offsetEnd; x++)
                        init.add(matrixSide * matrixSide * z + matrixSide * y + x);
        } else {
            for (int y = offsetStart; y < offsetEnd; y++)
                for (int x = offsetStart; x < offsetEnd; x++)
                    init.add(matrixSide * y + x);
        }


        // shuffle the list of all possible cells for initialization
        Collections.shuffle(init, new Random(randomSeed));
        // create hash set with the first given percentage of the possible cells for initialization
        return new HashSet<>(init.subList(0, (initialOccupationPercentage * matrixSide) / 100 ));
    }


    /**
     * Prints the cells alive
     * @param set The set with the alive cells
     * @param matrixSide The matrix side size for decomposing the value
     */
    protected static void printAliveCells(final HashSet<Integer> set, final int matrixSide) {

        final Consumer<Integer> decoder = i -> {
            final int x = i % matrixSide;
            final int y = ((i - x) / matrixSide) % matrixSide;
            final int z = ((i - matrixSide * y - x) / (matrixSide * matrixSide)) % matrixSide;
            System.out.println(x + ", " + y + ", " + z);
        };

        System.out.println(matrixSide);
        System.out.println(set.size());
        set.forEach(decoder);
    }


    protected static ArrayList<Integer> mooreCells(final int matrixSide, final int radius, final boolean isThreeD) {
        // TODO this
        if (radius <= 0) return null;

        final HashSet<Integer> neighbourCells = new HashSet<>((int) Math.pow(2 * radius + 1, (isThreeD) ? 3 : 2));

        // TODO make prettier
        if (isThreeD) {
            for (int z = 0; z <= radius; z++)
                for (int y = 0; y <= radius; y++)
                    for (int x = 0; x <= radius; x++) {
                        neighbourCells.add(x - y * matrixSide - z * matrixSide * matrixSide);
                        neighbourCells.add(-x - y * matrixSide - z * matrixSide * matrixSide);
                        neighbourCells.add(x + y * matrixSide - z * matrixSide * matrixSide);
                        neighbourCells.add(-x + y * matrixSide - z * matrixSide * matrixSide);

                        neighbourCells.add(x - y * matrixSide + z * matrixSide * matrixSide);
                        neighbourCells.add(-x - y * matrixSide + z * matrixSide * matrixSide);
                        neighbourCells.add(x + y * matrixSide + z * matrixSide * matrixSide);
                        neighbourCells.add(-x + y * matrixSide + z * matrixSide * matrixSide);
                    }
        } else {
            for (int y = 0; y <= radius; y++)
                for (int x = 0; x <= radius; x++) {
                    neighbourCells.add(x - y * matrixSide);
                    neighbourCells.add(-x - y * matrixSide);

                    neighbourCells.add(x + y * matrixSide);
                    neighbourCells.add(-x + y * matrixSide);
                }
        }

        return new ArrayList<>(neighbourCells);

    }
}
