import numpy as np
from numpy.linalg import norm

"""is_reg_projection determines whether the given projection is a regular 
   projection of the given saw. This means two things:
   
   1) no three points of the saw (which includes points in the edges) may 
      project to the same point and
      
   2) no vertex may project to the same point as any other point within the saw"""
def is_reg_projection(projection, saw):
    return None

"""com_projection calculates the projection of the given saw onto the plane
   defined by the three points in the set {p_com, xi, xi1}, where 
   
   p_com == the coordinates of the 'center of mass' of the saw, assuming the 
            mass of the edges is negligible and the vertices are particles of 
            unit mass
            
    xi == the ith vertex of the saw
    xi1 == the i+1th vertex of the saw"""
def com_projection(saw, k, k_1):
    com = np. zeroes(3)
    L = saw.shape[0]

    for i in np.range(L):
        com = np.add(com, saw[i])
    
    com = com / L
    v1 = np.subtract(saw[k], com)
    v2 = np.subtract(saw[k_1], com)

    plane_norm = np.cross(v1, v2)
    plane_norm = plane_norm / norm(plane_norm, 2)

    projection = []

    for i in np.range(L):
        if i == k:
            projection.append(saw[k])
        elif i == k_1:
            projection.append(saw[k_1])
        else:
            p = saw[i] - plane_norm * np.dot(plane_norm, (saw[i]-com))
            projection.append(p)
    
    projection = np.array(projection)
    return projection

"""find_reg_project finds a regular projection of the given simple random walk.
   If none can be found, returns None, else returns the given projection as the
   array of points in three space."""
def find_reg_project(saw):
    L = saw.shape[0]
    projection = None
    for i in np.range(L):
        if i == L-1:
            projection = com_projection(saw, i, 0) 
        projection = com_projection(saw, i, i+1)
    if not is_regular_projection(projection):
        projection = None
    return projection
    
        