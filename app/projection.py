import numpy as np
from numpy.linalg import norm

"""rotates about the x-axis in a counterclockwise fashion by angle alpha
   (also rotates the axes clockwise by angle alpha"""


def rot_matrix_x(alpha):
    """return rotation matrix about x-axis by angle alpha"""
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, np.cos(alpha), -np.sin(alpha)],
            [0.0, np.sin(alpha), np.cos(alpha)],
        ]
    )


def rot_matrix_y(alpha):
    """return rotation matrix about Y-axis by angle alpha"""
    return np.array(
        [
            [np.cos(alpha), 0.0, np.sin(alpha)],
            [0.0, 1.0, 0.0],
            [-np.sin(alpha), 0.0, np.cos(alpha)],
        ]
    )

"""is_reg_projection determines whether the given projection is a regular 
   projection of the given saw. This means two things:
   
   1) no three points of the saw (which includes points in the edges) may 
      project to the same point and
      
   2) no vertex may project to the same point as any other point within the saw"""


def is_reg_projection(projection, saw):
    """return True if projection is a regular projection of saw, else False.
    
    A projection of a SAW is regular if it satisfies the following two conditions:
    1) no three points of the saw (which includes points in the edges) may 
        project to the same point and
    2) no vertex may project to the same point as any other point within the saw
    
    arguments:
    projection - numpy array of shape (N, 2) - the projection of the SAW
    saw - numpy array of shape (N, 3) - the SAW we are doing analysis on
    
    return value:
    so far None (unimplemented)
    """
    #TODO: implement, to test functionality of com_projection
    return None


def com_projection(saw, k, k_1):
    """return numpy array of projection using com, pk, and pk_1 as ref points.
    
    The method computes the center of mass of the saw, assuming all nodes
    have unit mass. It then projects each point of the SAW to the plane
    defined by points com, pk, and pk_1 along the normal to the plane.
    This function may be redundant given the rotational method below.
    
    arguments:
    saw - numpy array of shape (N, 3) - the saw we are finding projection of
    k - int - index of point pk in saw
    k_1 - int - index of point pk_1 in the saw (I include it here so that we wrap
    back to the original node of the saw in the outer function find_reg_project_com,
    not here)
    
    return value:
    projection - numpy array of shape (N, 2) - the com projection sought after
    """
    com = np.zeroes(3)
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
            p = saw[i] - plane_norm * np.dot(plane_norm, (saw[i] - com))
            projection.append(p)

    projection = np.array(projection)
    return projection


"""find_reg_project finds a regular projection of the given simple random walk.
   If none can be found, returns None, else returns the given projection as the
   array of points in three space."""


def find_reg_project_com(saw):
    """return regular projection of saw.
    
    uses the com_projection method to search for a regular projection within
    the set of planes defined by the com, and all adjacent points (pk, pk_1) in
    the saw, including the last and first points. Just in-case this isn't always
    possible, returns None
    
    argument:
    saw - numpy array of shape (N, 3) - the SAW which we wish to find a com 
    projection from
    
    return values:
    projection - numpy array of shape (N, 2) - the regular projection of the SAW,
    if it exists
    None - if the regular projection via the com method does not exist
    """
    L = saw.shape[0]
    projection = None
    for i in np.range(L):
        if i == L - 1:
            projection = com_projection(saw, i, 0)
        projection = com_projection(saw, i, i + 1)
    if not is_regular_projection(projection):
        projection = None
    return projection


"""prepares a saw so that it may be projected into the xy plane via art setting 
   z-comp of every vertex to zero. We don't actually do that here, but instead,
   rotate the saw so that such a projection will be regular """



def rot_saw_xy(saw):
    alpha = -np.pi / 3.0
    beta = np.pi / 6.0
    gamma = np.pi
    x_rot = rot_matrix_x(alpha)
    y_rot = rot_matrix_y(beta + gamma) # gamma rotation is for debugging
    rotated_saw = []
    for vertex in saw:
        rot_vertex = np.matmul(x_rot, vertex)
        rot_vertex = np.matmul(y_rot, vertex)
        rotated_saw.append(rot_vertex)
    return rotated_saw

def find_reg_project_rot(saw):
    """return regular projection of SAW via rotation by irrational angle.
    
    I like this one. Finds a regular projection of the SAW by rotating 
    the axes CCW (or conversely, by rotating the SAW CW) by an irrational
    angle, thus guaranteeing that no multiple points are triple, and that
    no two vertices are projected to the same point (vertices are at most
    single points).

    (Note that the angle is completely arbitrary, so I chose PI/3)
    (CHANGELOG: added second y-rotation by pi / 6 on 10/04/2021)
    
    argument:
    saw - numpy array of shape (N, 3) - the SAW which we wish to find a com
    
    return value:
    projection - numpy array of shape (N, 2) - the projection of the saw
    """
    rotated_saw = rot_saw_xy(saw)
    projection = []
    for vertex in rotated_saw:
        project_vertex = vertex
        project_vertex[2] = 0.0 # project to xy plane :)
        projection.append(project_vertex)

    projection = np.array(projection)

    return projection
