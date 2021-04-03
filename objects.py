import math
import enum
import statistics as sts

class Cell(object):

    def __init__(self, x, y, z=None):
        """Returns a Cell object with the given coordinates

        Parameters
        ----------
        x : float
            Horizontal coordinate
        y : float
            Vertical coordinate
        z : float
            Depth coordinate
        """

        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def new_from_array(cls, array):
        """Constructs a Cell object from a list (array)

        Parameters
        ----------
        array : list
            List of coordinates. Expected order is [x, y] or [x, y, z]
        """

        if len(array) == 2:
            # 2D Point
            return cls(
                int(array[0]), int(array[1])
            )
        # 3D Point
        return cls(
            int(array[0]), int(array[1]), int(array[2])
        )

    def coordinate_list(self):
        if self.z is not None:
            return [self.x, self.y, self.z]
        return [self.x, self.y]

    # L1 distance from cell to origin
    def distance_to_origin_l1(self):
        z = self.z if self.z is not None else 0
        return abs(self.x) + abs(self.y) + abs(z)
    
    # L2 distance from cell to origin
    def distance_to_origin_l2(self):
        z = self.z if self.z is not None else 0
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(z, 2))
    
    def is_border_cell(self, side):
        offset = int((side - 1) / 2)
        if any(v == -offset or v == side - 1 - offset for v in self.coordinate_list()):
            return True
        return False
    
    # Define hash and eq methods to allow comparation in cell hash and eq
    def __hash__(self):
        z = self.z if self.z is not None else 0
        hash = 1
        hash = 1009 * hash + self.x
        hash = 1009 * hash + self.y
        return 1009 * hash + z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not (self == other)


class Ending(enum.Enum):

    Border = 'Got to edge 🏁'
    Dead = 'All cells died 💀️'
    Repeated = 'Repetition 🔁'
    Multiple = 'Multiple death causes'

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return self.value

# TODO: Add min_distance_slope, generation_changes_slope
class Observables(object):
    def __init__(self, ending, step_count, live_count_slope, max_distance_slope, min_distance_slope, gen_changes_slope):
        self.ending = ending
        self.step_count = step_count
        self.live_count_slope = live_count_slope
        self.max_distance_slope = max_distance_slope
        self.min_distance_slope = min_distance_slope
        self.gen_changes_slope = gen_changes_slope
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return """Ended by: %s\nTotal number of generations (including initial one): %s
            \nFinal live_count slope: %s\nFinal furthest_distance slope: %s
            \nFinal minimum_distance slope: %s\nFinal gen_changes slope: %s\n""" % (self.ending, self.step_count, self.live_count_slope, self.max_distance_slope, self.min_distance_slope, self.gen_changes_slope)

class FullValue(object):
    def __init__(self, media, std):
        if std == 0:
            self.dec_count = 3
        else:
            self.dec_count = math.ceil(abs(math.log10(std)))
        self.media = round(media, self.dec_count)
        self.std = round(std, self.dec_count)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "%s±%s" % (self.media, self.std)

class Summary(object):
    def __init__(self, observable_list, init_percentage):
        self.init_percentage = init_percentage
        step_list = []
        live_count_slope_list = []
        max_distance_slope_list = []
        min_distance_slope_list = []
        gen_changes_slope_list = []
        self.ending = {}

        for obs in observable_list:
            step_list.append(obs.step_count)
            live_count_slope_list.append(obs.live_count_slope)
            max_distance_slope_list.append(obs.max_distance_slope)
            min_distance_slope_list.append(obs.min_distance_slope)
            gen_changes_slope_list.append(obs.gen_changes_slope)
            if obs.ending not in self.ending:
                self.ending[obs.ending] = 0
            self.ending[obs.ending] += 1

        self.step = FullValue(sts.mean(step_list), sts.stdev(step_list))
        self.live_count_slope = FullValue(sts.mean(live_count_slope_list), sts.stdev(live_count_slope_list))
        self.max_distance_slope = FullValue(sts.mean(max_distance_slope_list), sts.stdev(max_distance_slope_list))
        self.min_distance_slope = FullValue(sts.mean(min_distance_slope_list), sts.stdev(min_distance_slope_list))
        self.gen_changes_slope = FullValue(sts.mean(gen_changes_slope_list), sts.stdev(gen_changes_slope_list))
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "Init Percentage(%s)\nStep(%s)\nLive count m(%s)\nMax distance m(%s)\nMin distance m(%s)\nGen changes m(%s)\nEnding(%s)\n" % (self.init_percentage, self.step, self.live_count_slope, self.max_distance_slope, self.min_distance_slope, self.gen_changes_slope, self.ending)