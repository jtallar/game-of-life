import math

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
