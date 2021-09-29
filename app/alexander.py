import numpy as np

"""validates whether the intersection of the line segments p1p2 and p3p4 is 
   within the bounding box of the line segments themselves"""

def validate_intersect_in_segment(p0, p1, p2, p3, p4):
   return True if min(p1[0], p2[0]) <= p0[0] <= max(p1[0], p2[0]) and \
          min(p1[1], p2[1]) <= p0[1] <= max(p1[1], p2[1]) else False

"""Determines whether the lines made from segments p1p2 and p3p4 are parallel 
   or not by attempting to find their intersection. Assume all points are 
   in R2"""

def find_intersection_2D(p1, p2, p3, p4):
   a1 = p2[1] - p1[1]
   b1 = p1[0] - p2[0]
   c1 = a1*p1[0] + b1*p1[1]

   a2 = p4[1] - p3[1]
   b2 = p3[0] - p4[0]
   c2 = a2*p3[0] + b2*p3[1]

   det = a1*b2 - a2*b1
   if det == 0: # lines are parallel, no intersection
      print("det zero wha wha")
      return None
   else:
      x = (c1*b2 - c2*b1) / det
      y = (a1*c2 - a2*c1) / det

      intersect = np.array([x, y])

      if validate_intersect_in_segment(intersect, p1, p2, p3, p4):
         return intersect
      else: return None


"""Traverses a saw *prepared for projection into the xy plane,* assigning double 
   points to be either 'overcrossings' or 'undercrossings'"""

"""collect_underpass_info collects the following information, and returns it
   as an ordered array: (underpass_type(int {0,1}, generator_num(int,{k})) where 
   'k' is the number of intersections, and is also the length of said array """


def collect_underpass_info(saw, projection):
    # TODO: 1.)use this to find intersections
    # https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
    #       2.) determine how, from the found intersections, we can find overpass
    #       versus underpass.
    return None
