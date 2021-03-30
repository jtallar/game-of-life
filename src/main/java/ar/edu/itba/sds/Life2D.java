package ar.edu.itba.sds;

import java.awt.*;
import java.io.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.BiPredicate;
import java.util.function.Consumer;
import java.util.function.IntConsumer;
import java.util.stream.IntStream;

public class Life2D {
    private static final int ERROR_STATUS = 1;

    private static int matrixSide;
    private static HashSet<Point> aliveCells;
    private static long steps;
    private static String outFileName;
    private static BiPredicate<Boolean, Integer> predicate;
    private static boolean parallel;

    public static void main(String[] args) {

        long startTime = System.currentTimeMillis();

        // initializes matrixSide and aliveCells
        initializeMatrixValues();

        // initialize the steps, out file name and parallel
        initializeVarious();

        // initialize the filter condition for a cell to live or die
        initializeFilterCondition();

        long endTime = System.currentTimeMillis();
        System.out.printf("Life Game Processing time \t\t ⏱  %g seconds\n", (endTime - startTime) / 1000.0);
        startTime = endTime;




        // set with the hashes of the alive cells hash set
        final HashSet<Integer> setHashes = new HashSet<>();

        // flag for stop criteria, true if a live cell reaches the edges
        final AtomicBoolean gotToEdge = new AtomicBoolean(false);

        // as an auxiliary list, to save the next step living cells
        final List<Point> newList = Collections.synchronizedList(new ArrayList<>());




        // the consumer applied on each cell
        final IntConsumer consumer = cell -> {
            // get values
            Point me = new Point(cell % matrixSide, (cell - cell % matrixSide) / matrixSide);
            int aliveNeighbours = getAliveNeighbours(aliveCells, me);
            boolean imAlive = aliveCells.contains(me);

            // if the predicate is met, the new cell is going to live for the next iterations
            if (predicate.test(imAlive, aliveNeighbours)) {
                newList.add(me);
                gotToEdge.set(me.x == 0 || me.y == 0 || me.x == matrixSide - 1 || me.y == matrixSide - 1);
            }
        };

        // check if the stream is parallel or not
        final Runnable runnable;
        if (parallel) runnable = () -> IntStream.range(0, matrixSide * matrixSide).parallel().forEach(consumer);
        else runnable = () -> IntStream.range(0, matrixSide * matrixSide).forEach(consumer);




        // life game iteration until steps are over or stop criteria is met
        long i = 0;
        while (i < steps) {

            // print to the output the living cells
            printAliveCells(aliveCells, matrixSide, outFileName);

            // stop criteria
            if (aliveCells.size() == 0) break; // all cells dead
            if (!setHashes.add(aliveCells.hashCode())) break; // repeated state
            if (gotToEdge.get()) break; // a cell or more got to an edge

            // iterate over all possible cells
            runnable.run();

            // save the new cells to the set
            aliveCells.clear();
            aliveCells.addAll(newList);
            newList.clear();
            i++;
        }
        // end of steps




        endTime = System.currentTimeMillis();
        System.out.printf("Life Game Execution time \t\t ⏱  %g seconds\n", (endTime - startTime) / 1000.0);
        System.out.printf("\nLife Game Finished in %d steps\n", i);
        System.out.print("\nLife Game Finished due to ");
        if (aliveCells.size() == 0) System.out.print("all dead cells 💀️");
        else if (gotToEdge.get()) System.out.print("a reach on the edge \uD83C\uDFC1");
        else if (steps == i) System.out.print("reach of top steps 🪜");
        else System.out.print("a repeated stat️e \uD83D\uDD01");
    }


    /**
     * Initializes the matrix side value and the set of alive cells
     */
    protected static void initializeMatrixValues() {

        final Properties properties = System.getProperties();

        // if an existing file is provided for the initialization, the rest is not taken into account
        final String existingInit = properties.getProperty("initFile");

        if (existingInit != null) {
            // initial matrix size and alive cells
            matrixSide = initializeMatrixSideFromFile(existingInit);
            aliveCells = initializeMatrixFromFile(existingInit);

        } else {

            try {
                // initial matrix size
                matrixSide = Integer.parseInt(properties.getProperty("size", "100"));

                // region size to be set out as initial zone has to be par or not according to initial matrix size
                final int initialMatrixSide = Integer.parseInt(properties.getProperty("initSize", "60"));

                // occupation percentage level of initial zone
                final int initialOccupationPercentage = Integer.parseInt(properties.getProperty("occupation", "60"));

                // seed for random generated positions
                final long randomSeed = Long.parseLong(properties.getProperty("seed", String.valueOf(System.nanoTime())));

                // initialize with a random value the matrix
                aliveCells = initializeMatrixRandom(matrixSide, initialMatrixSide, initialOccupationPercentage, randomSeed);

            } catch (NumberFormatException e) { printAndExit(e.getMessage()); }
        }
    }


    /**
     * Initializes the stop criteria and out filename for the algorithm
     */
    protected static void initializeVarious() {
        final Properties properties = System.getProperties();

        try {
            // steps stop criteria
            steps = Long.parseLong(properties.getProperty("steps", String.valueOf(Long.MAX_VALUE)));
        } catch (NumberFormatException e) { printAndExit(e.getMessage()); }

        // if runs parallel or not
        parallel = Boolean.parseBoolean(properties.getProperty("parallel"));

        // if there is already a file append there
        if (properties.getProperty("initFile") != null) {
            outFileName = properties.getProperty("initFile");
            return;
        }

        // filename output prefix with the cells
        outFileName = properties.getProperty("out", "data");

        // create the file
        try(BufferedWriter writer = new BufferedWriter(new FileWriter(outFileName))) {
            writer.write("2\n" + matrixSide + "\n");
        } catch (IOException e) { printAndExit(e.getMessage()); }



    }


    /**
     * Initializes the filter criteria for kill or live cells
     */
    protected static void initializeFilterCondition() {

        // TODO maybe make dynamic?
        final Properties properties = System.getProperties();

        final String rule = properties.getProperty("rule", "B3/S23");

        // filtering condition
        switch (rule) {
            case "B36/S23":
                predicate = (alive, count) -> {
                    if (alive) return count == 2 || count == 3;
                    else return count == 3 || count == 6;
                };
                break;

            case "B2/S3":
                predicate = (alive, count) -> {
                    if (alive) return count == 2;
                    else return count == 3;
                };
                break;

            default:
                predicate = (alive, count) -> {
                    if (alive) return count == 2 || count == 3;
                    else return count == 3;
                };
        }

    }


    /**
     * Initializes de matrix given the params taken
     * @param matrixSide The whole matrix side value
     * @param initialMatrixSide The initial matrix side value. Should be less than @param matrixSide
     * @param initialOccupationPercentage The initial occupation percentage for the initial matrix
     * @param randomSeed Random seed for shuffling
     * @return The HashSet with the values
     */
    protected static HashSet<Point> initializeMatrixRandom(final int matrixSide, final int initialMatrixSide, final int initialOccupationPercentage, final long randomSeed) {

        // check for invalid relation values
        if ((matrixSide - initialMatrixSide) % 2 != 0 || matrixSide < initialMatrixSide) printAndExit("Invalid initial matrix size");
        if (initialOccupationPercentage <= 0 || initialOccupationPercentage >= 100) printAndExit("Invalid initial occupation percentage");

        // auxiliary variables for posterior use
        final List<Point> init = new ArrayList<>((int) Math.pow(initialMatrixSide, 2));
        final int offsetStart = (matrixSide - initialMatrixSide) / 2;
        final int offsetEnd = offsetStart + initialMatrixSide;

        // create all possible valid cells points for initialization
        for (int y = offsetStart; y < offsetEnd; y++)
            for (int x = offsetStart; x < offsetEnd; x++)
                init.add(new Point(x, y));

        // shuffle the list of all possible cells for initialization
        Collections.shuffle(init, new Random(randomSeed));
        // create hash set with the first given percentage of the possible cells for initialization
        return new HashSet<>(init.subList(0, (initialOccupationPercentage * initialMatrixSide * initialMatrixSide) / 100));
    }


    /**
     * Read from the file only the general size of the matrix
     * @param filename The filename to read
     * @return The size of the matrix
     */
    protected static int initializeMatrixSideFromFile(final String filename) {

        try(BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            if (Integer.parseInt(reader.readLine()) != 2) printAndExit("Should be 2 Dimension file data");
            return Integer.parseInt(reader.readLine());
        } catch (IOException e) { printAndExit(e.getMessage()); }

        return -1;
    }


    /**
     * Initializes the alive cells from a given file
     * @param filename The filename to read from
     * @return The new HashSet of alive cells
     */
    protected static HashSet<Point> initializeMatrixFromFile(final String filename) {

        try(BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            reader.readLine(); // skip first line - 2 or 3D
            reader.readLine(); // skip second line - matrix size
            reader.readLine(); // skip third line - *

            int size = Integer.parseInt(reader.readLine()); // amount of living cells
            final List<Point> init = new ArrayList<>(size); // auxiliary array

            for (int i = 0; i < size; i++) {
                String line = reader.readLine();
                if (line == null) throw new IOException();
                String[] aux = line.split(" ");
                init.add(new Point(Integer.parseInt(aux[0]), Integer.parseInt(aux[1])));
            }

            // check if its the final line
            if (reader.readLine() != null) printAndExit("Bad formatted input file");

            return new HashSet<>(init);

        } catch (IOException e) { printAndExit(e.getMessage()); }

        return null;
    }


    /**
     * Prints the cells alive
     * @param set The set with the alive cells
     * @param matrixSide The matrix side size for decomposing the value
     * @param outFileName The filename prefix
     */
    protected static void printAliveCells(final HashSet<Point> set, final int matrixSide, final String outFileName) {
        try(BufferedWriter writer = new BufferedWriter(new FileWriter(outFileName, true))) {
            writer.write("*\n" + set.size() + "\n");

            // write each point
            for (Point p : set) writer.write((int) p.getX() + " " + (int) p.getY() + " " + 0 + "\n");
        } catch (IOException e) { printAndExit(e.getMessage()); }
    }


    /**
     * Counts the amount of neighbour alive cells
     * @param aliveCells The set of alive cells
     * @param me The position of me
     * @return The amount of alive neighbour cells
     */
    protected static int getAliveNeighbours(final Set<Point> aliveCells, final Point me) {
        int count = 0;
        if (aliveCells.contains(new Point(me.x + 1, me.y - 1))) count++;
        if (aliveCells.contains(new Point(me.x + 1, me.y))) count++;
        if (aliveCells.contains(new Point(me.x + 1, me.y + 1))) count++;

        if (aliveCells.contains(new Point(me.x - 1, me.y - 1))) count++;
        if (aliveCells.contains(new Point(me.x - 1, me.y))) count++;
        if (aliveCells.contains(new Point(me.x - 1, me.y + 1))) count++;

        if (aliveCells.contains(new Point(me.x, me.y - 1))) count++;
        if (aliveCells.contains(new Point(me.x, me.y + 1))) count++;

        return count;
    }

    protected static void printAndExit(String message) {
        System.err.println(message);
        System.exit(ERROR_STATUS);
    }
}
