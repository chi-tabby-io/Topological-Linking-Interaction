from .alexander import find_intersection_2D
import numpy as np


def intersect_unit_test():
    # define points: NOTE: this case is for parallel lines
    A = np.array([2.,0.])
    B = np.array([2., 2.])
    C = np.array([0., 2.])
    D = np.array([0., 0.])

    intersection = find_intersection_2D(A, B, C, D)

    if intersection is None:
        print("no intersection or intersection not in segment")
    else:
        print("intersection at ({x}, {y})".format(x=intersection[0], 
              y=intersection[1]))