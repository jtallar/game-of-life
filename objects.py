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
                float(array[0]), float(array[1])
            )
        # 3D Point
        return cls(
            float(array[0]), float(array[1]), float(array[2])
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

class Ending(enum.Enum):

    Border = 'Got to edge 🏁'
    Dead = 'All cells died 💀️'
    Repeated = 'Repetition 🔁'
    Multiple = 'Multiple death causes'

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return self.value

class Observables(object):
    def __init__(self, ending, step_count, live_count_slope, max_distance_slope):
        self.ending = ending
        self.step_count = step_count
        self.live_count_slope = live_count_slope
        self.max_distance_slope = max_distance_slope
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return """Ended by: %s\nTotal number of generations (including initial one): %s
            \nFinal live_count slope: %s\nFinal futhest_distance slope: %s\n""" % (self.ending, self.step_count, self.live_count_slope, self.max_distance_slope)

class FullValue(object):
    def __init__(self, media, std):
        std_dec = math.ceil(abs(math.log10(std)))
        self.media = round(media, std_dec)
        self.std = round(std, std_dec)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "%s±%s" % (self.media, self.std)

class Summary(object):
    def __init__(self, observable_list):
        step_list = []
        live_count_slope_list = []
        max_distance_slope_list = []
        self.ending = observable_list[0].ending

        for obs in observable_list:
            step_list.append(obs.step_count)
            live_count_slope_list.append(obs.live_count_slope)
            max_distance_slope_list.append(obs.max_distance_slope)
            if self.ending != obs.ending:
                self.ending = Ending.Multiple

        self.step = FullValue(sts.mean(step_list), sts.stdev(step_list))
        self.live_count_slope = FullValue(sts.mean(live_count_slope_list), sts.stdev(live_count_slope_list))
        self.max_distance_slope = FullValue(sts.mean(max_distance_slope_list), sts.stdev(max_distance_slope_list))
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "Step(%s)\nLive count m(%s)\nMax distance m(%s)\nEnding(%s)" % (self.step, self.live_count_slope, self.max_distance_slope, self.ending)