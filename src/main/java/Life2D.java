import java.awt.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.BiPredicate;
import java.util.stream.IntStream;

public class Life2D {

    public static void main(String[] args) {
        // read properties
        Properties properties = System.getProperties();

        // initial matrix size
        int matrixSide = Integer.parseInt(properties.getProperty("size", "5"));

        // region size to be set out as initial zone has to be par or not according to initial matrix size
        int initialMatrixSide = Integer.parseInt(properties.getProperty("initSize", "3"));

        // occupation percentage level of initial zone
        int initialOccupationPercentage = Integer.parseInt(properties.getProperty("occupation", "60"));

        // seed for random generated positions
        long randomSeed = Long.parseLong(properties.getProperty("seed", String.valueOf(System.nanoTime())));

        // steps stop criteria
        long steps = Long.parseLong(properties.getProperty("steps", String.valueOf(Long.MAX_VALUE)));

        final HashSet<Integer> setHashes = new HashSet<>();

        // initialize set
        final HashSet<Point> set = initializeMatrix(matrixSide, initialMatrixSide, initialOccupationPercentage, randomSeed);
//        final List<Point> newList = Collections.synchronizedList(new ArrayList<>());
        final List<Point> newList = new ArrayList<>();

        // flag for stop criteria, true if a live cell reaches the edges
        final AtomicBoolean gotToEdge = new AtomicBoolean(false);

        // filtering condition
        final BiPredicate<Boolean, Integer> predicate = (alive, count) -> {
            if (alive) return count >= 2;
            else return count == 3;
        };

        for (long i = 0; i < 10; i++) {
            System.out.println();
            System.out.println("TIME " + i);
            printAliveCells(set, matrixSide);

            if (set.size() == 0) return; // all cells dead
            if (!setHashes.add(set.hashCode())) return; // repeated state
            if (gotToEdge.get()) return;

            IntStream.range(0, matrixSide * matrixSide).forEach(cell -> {
                Point me = new Point(cell % matrixSide, (cell - cell % matrixSide) / matrixSide);
                int aliveNeighbours = getAliveNeighbours(set, me);
                boolean imAlive = set.contains(me);
                if (predicate.test(imAlive, aliveNeighbours)) {
                    newList.add(me);
                    gotToEdge.set(me.x == 0 || me.y == 0 || me.x == matrixSide - 1 || me.y == matrixSide - 1);
                }
            });

            set.clear();
            set.addAll(newList);
            newList.clear();
        }
        // end of steps
    }

    /**
     * Initializes de matrix given the params taken
     * @param matrixSide The whole matrix side value
     * @param initialMatrixSide The initial matrix side value. Should be less than @param matrixSide
     * @param initialOccupationPercentage The initial occupation percentage for the initial matrix
     * @param randomSeed Random seed for shuffling
     * @return The HashSet with the values
     */
    protected static HashSet<Point> initializeMatrix(final int matrixSide, final int initialMatrixSide, final int initialOccupationPercentage, final long randomSeed) {

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
        return new HashSet<>(init.subList(0, (initialOccupationPercentage * matrixSide) / 100 ));
    }

    /**
     * Prints the cells alive
     * @param set The set with the alive cells
     * @param matrixSide The matrix side size for decomposing the value
     */
    protected static void printAliveCells(final HashSet<Point> set, final int matrixSide) {
        System.out.println(matrixSide);
        System.out.println(set.size());
        set.forEach(p -> System.out.println(p.getX() + ", " + p.getY() + ", " + 0));
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
}
