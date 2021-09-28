import numpy as np

"""Traverses a saw *prepared for projection into the xy plane,* assigning double 
   points to be either 'overcrossings' or 'undercrossings'"""

"""collect_underpass_info collects the following information, and returns it
   as an ordered array: (underpass_type(int {0,1}, generator_num(int,{k})) where 
   'k' is the number of intersections, and is also the length of said array """
def collect_underpass_info(saw, projection):
    # TODO: 1.)use this to find intersections https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
    #       2.) determine how, from the found intersections, we can find overpass
    #       versus underpass.
    return None