import numpy as np
from numpy.linalg import norm

"""rotates about the x-axis in a counterclockwise fashion by angle alpha
   (also rotates the axes clockwise by angle alpha"""
def rot_matrix_x(alpha):
    return np.array([[1., 0., 0.],
                      [0., np.cos(alpha), -np.sin(alpha)],
                      [0., np.sin(alpha), np.cos(alpha)]])

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
def find_reg_project_com(saw):
    L = saw.shape[0]
    projection = None
    for i in np.range(L):
        if i == L-1:
            projection = com_projection(saw, i, 0) 
        projection = com_projection(saw, i, i+1)
    if not is_regular_projection(projection):
        projection = None
    return projection


"""prepares a saw so that it may be projected into the xy plane via art setting 
   z-comp of every vertex to zero. We don't actually do that here, but instead,
   rotate the saw so that such a projection will be regular """
def pre_reg_project(saw):
    # using negative pi / 3 rad so that we rotate axes counterclockwise
    alpha = -np.pi / 3.
    x_rot = rot_matrix_x(alpha)

    rot_saw = []
    for vertex in saw:
        rot_vertex = np.matmul(x_rot, vertex)
        #project to xy plane :)
        rot_vertex[2] = 0.
        rot_saw.append(rot_vertex)
    
    rot_saw = np.array(rot_saw)

    return rot_saw
    
        