
import numpy as np
from numpy.linalg import LinAlgError, norm

eps = 1.0e-12 # convenient small value for double comparison

def validate_intersect_in_segments(p0, p1, p2, p3, p4):
   """return True if p0 in bounding box of p1p2 AND p3p4, else return False."""
   in_line_1 = min(p1[0], p2[0]) < p0[0] < max(p1[0], p2[0]) and \
          min(p1[1], p2[1]) < p0[1] < max(p1[1], p2[1])
   in_line_2 = min(p3[0], p4[0]) < p0[0] < max(p3[0], p4[0]) and \
          min(p3[1], p4[1]) < p0[1] < max(p3[1], p4[1])
   
   return True if (in_line_1 and in_line_2) else False


def find_intersection_2D_vec(p1, p2, p3, p4):
   """from line segments p1p2 and p3p4, return the intersection if it exists.
   
   Each line segment may be represented by the vector eqns:

   x_1 = u_1 - v_1*t
   x_2 = u_2 - v_2*s

   where each underscored variable is a 3-vector, and t and s are real numbers
   lying in some closed interval of the real line such that for min(t) and min(s)
   x_1 = p1 and x_2 = p3 and likewise for the maxima. 

   The point of using this method is so that we return parameters for each
   intersection which gives us information about how far from the starting 
   point the intersection takes place. This information will be used in the 
   case when a single line segment has intersections with multiple other line
   segments. 

   arguments:
   p1 - numpy array of doubles with shape (2,1) - first point of line segment p1p2
   p2 - numpy array of doubles with shape (2,1) -second point of line segment p1p2
   p3 - numpy array of doubles with shape (2,1) - first point of line segment p3p4
   p4 - numpy array of doubles with shape (2,1) - second point of line segment p3p4

   return value(s):
   None - either the linear system is inconsistent or the intersection does not lie
   in both segments' bounding boxes
   np.array([intersect, x[0]]) - a numpy array whose first entry is the coordinates
   of the intersection and the second is the parameter associated with line segment
   p1p2, which serves as the "reference line segment"
   """
   # create 3-vector to solve linear system A*x = b
   b_1 = p1[0] - p3[0]
   b_2 = p1[1] - p3[1]
   b = np.array([b_1,b_2])

   # collect tangent vectors
   v_1 = np.subtract(p2,p1)
   v_2 = np.subtract(p4,p3)

   v_1_normalized = v_1 / norm(v_1)
   v_2_normalized = v_2 / norm(v_2)

   # if the tangent vectors are parallel, impossible for there to be an
   # intersection, given our projection is regular
   if np.array_equal(v_1_normalized, v_2_normalized):
      return None
   
   A = np.array([[-v_1[0], v_2[0]],[-v_1[1], v_2[1]]])
   x = np.empty((2,1))

   try:
      x = np.linalg.solve(A, b)
   except LinAlgError: # A is singular
      return None
   finally:
      intersect = find_intersection_2D(p1, p2, p3, p4)
      if intersect is None: return None # case when have intersect, but no in seg
      else:
         return np.array([intersect, x[0]]) # return both intersect and param values


# algorithm from: https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
def find_intersection_2D(p1, p2, p3, p4):
   """from line segments p1p2 and p3p4, return the intersection if it exists.
   
   The pair of lines is modeled as a linear system of the following form:

      a1*x + b1*y = c1
      a2*x + b2*y = c2

   and is solved via Cramer's Rule

   Here we also validate whether the intersection, if so found, exists within
   both line segments or not.
   
   arguments:
   p1 - numpy array of doubles with shape (2,1) - first point of line segment p1p2
   p2 - numpy array of doubles with shape (2,1) -second point of line segment p1p2
   p3 - numpy array of doubles with shape (2,1) - first point of line segment p3p4
   p4 - numpy array of doubles with shape (2,1) - second point of line segment p3p4
   
   return value(s):
   intersect - numpy array of doubles with shape (2,1) - x is the x-component 
   of the intersection and y is the y-component
   None - if the intersection does not exist or does not lie in segment p1p2
   """
   a1 = p2[1] - p1[1]
   b1 = p1[0] - p2[0]
   c1 = a1*p1[0] + b1*p1[1]

   a2 = p4[1] - p3[1]
   b2 = p3[0] - p4[0]
   c2 = a2*p3[0] + b2*p3[1]

   det = a1*b2 - a2*b1
   if det == 0: # lines are parallel, no intersection
      return None
   else: # Cramer's Rule
      x = (c1*b2 - c2*b1) / det
      y = (a1*c2 - a2*c1) / det

      intersect = np.array([x, y])

      if validate_intersect_in_segments(intersect, p1, p2, p3, p4):
         return intersect
      else: return None # not validating here... do in is_underpass


def is_underpass(k, j, intersect, saw):
   # TODO: test again, ensure working after moving validation in segment
   # bit back to find intersection function
   """return True if segment pkpk_1 is an underpass of pjpj_1, else return False.
   
   This method uses the eqns for a line in 3D found
   here: https://byjus.com/maths/equation-line/ to calculate the z-value
   of the corresponding point in the SAW to determine whether pkpk_1 is
   an underpass or not.
   
   arguments:
   k - int - the index of node pk within the SAW
   j - int the index of node pj within the SAW
   intersect - numpy array with shape (2,1) - the intersection within the 
   projection, with format (x, y)
   saw - numpy array with shape (N, 3) - the SAW where underpasses will be 
   found from
   
   return value:
   boolean - True if pkpk_1 is an underpass, else False
   """
   pk = saw[k]
   pk_1 = saw[k+1]
   pj = saw[j]
   pj_1 = saw[j+1]

   zk = pk[2] + (pk_1[2] - pk[2])*(intersect[0] - pk[0]) / (pk_1[0] - pk[0])
   zj = pj[2] + (pj_1[2] - pj[2])*(intersect[0] - pj[0]) / (pj_1[0] - pj[0])
   return True if (zj - zk > eps) else False


def order_intersections(intersections):
   """returns a sorted list of intersections according to projection orientation.
   
   arguments:
   intersections - a list of lists, containing the intersection coords and indices, and 
   ordering parameter for each segment the first time it is encountered as an intersection
   
   return value:
   the sorted version of intersections
   """
   # dtype to be used for the structured array
   dtype = [('coords', np.float64, (2,)), ('indices', np.uintc, (4,)), ('order_param', np.float64)]
   intersections_as_array = np.array(intersections, dtype=dtype)
   # create temp array to be used as the sorting key
   temp = np.zeros(intersections_as_array.shape, dtype='int,float')
   # get first two columns of the indices
   temp['f0'] = intersections_as_array['indices'][:,:2]
   temp['f1'] = intersections_as_array['order_param']
   # this step is literally magic as far as I know
   return intersections_as_array[np.arsort(temp)]


def collect_all_intersections(proj):
   """return structured array of intersection coords and surrounding indices.
   
   I am going to define a separate function which runs in linear time which
   checks that the array is ordered according to the keys and the params (somewhat
   alphabet ordering, order first according to the keys, which are the first
   two indices of every intersection (these are well-ordered for every projection)
   and then if we have a tie, break it using the parameters, which will also
   be well-ordered.
   """

   intersections = []
   for k in np.arange(proj.shape[0]-1):
      for j in np.arange(proj.shape[0]-1):
         if j == k-1 or j == k or j == k+1:
            continue
         pk = proj[k][:2]
         pk_1 = proj[k+1][:2]
         pj = proj[j][:2]
         pj_1 = proj[j+1][:2]
         intersection = find_intersection_2D_vec(pk, pk_1, pj, pj_1)
         if intersection is not None:
            # may modify in the future, as we may not need to return numpy array
            # for find_intersection_2D_vec
            this_intersection = [intersection[0].tolist(),[k,k+1,j,j+1], intersection[1]]
            intersections.append(this_intersection)

   return_val = order_intersections(intersections)
   return return_val


def get_underpass_nodes(proj, saw):
   """return a list of underpasses, in order of occurence."""
   intersection_nodes = collect_all_intersections_by_indices(proj)
   intersection_coords = collect_all_intersections_by_coord(proj)
   underpass_nodes = np.empty((1,4), dtype=np.uintc)
   for i in np.arange(np.shape(intersection_nodes)[0]):
      if is_underpass(intersection_nodes[i,0], intersection_nodes[i,2],
                      intersection_coords[i], saw):
         underpass_nodes = np.append(underpass_nodes, np.array([intersection_nodes[i]],dtype=np.uintc), axis=0)
   return underpass_nodes[1:]


def assign_underpass_types(underpasses, proj, underpass_info):
   """return None, only modify elements of underpass_info by assigning underpass type."""
   for l in np.arange(np.shape(underpasses)[0]):
      # collect underpass type
      pk = proj[underpasses[l][1]][:2]
      pk_1 = proj[underpasses[l][2]][:2]
      pj = proj[underpasses[l][3]][:2]
      v1 = np.subtract(pk, pj)
      v2 = np.subtract(pk, pk_1)
      if np.cross(v1, v2) == 1: # Type I
         underpass_info[l,0] = 0
      else: # Type II
         underpass_info[l,0] = 1


def assign_generator_to_underpasses(underpass_nodes, intersection_nodes,
                                    intersection_coords, underpass_info, saw):
   """return None, modify elements of underpass_info by assigning overpass generators"""
   #using indexes is just..easier
   for i in np.arange(np.shape(underpass_nodes)[0]):
      # below finds the index of the current underpass within intersections, then decrements
      j = np.nonzero(np.all((intersection_nodes-underpass_nodes[i])==0,axis=1))[0][0] - 1
      while True:
         if j < 0:
            j = np.shape(intersection_nodes)[0] - 1
         if not is_underpass(intersection_nodes[j,0], intersection_nodes[j,2],
                             intersection_coords[j], saw):

            underpass_k = np.roll(intersection_nodes[j], 2)
            k = np.nonzero(np.all((underpass_nodes-underpass_k)==0,axis=1))[0][0]
            underpass_info[k, 1] = i
            j -= 1
         else:
            break


#FURTHER NOTE 10/10/2021: this function kind of acts like our new alexander_pre_compile
def pre_alexander_compile(saw, proj):
   """return a list of underpass info, including underpass type and generator."""
   #intersection_nodes = collect_all_intersections_by_indices(proj)
   #intersection_coords = collect_all_intersections_by_coord(proj)
   intersections = collect_all_intersections(proj)
   underpass_nodes = get_underpass_nodes(proj, saw)

   # initialize unerpass_info
   underpass_info = np.zeros((np.shape(underpass_nodes)[0],2),dtype=np.intc) 

   assign_underpass_types(underpass_nodes, proj, underpass_info)
   assign_generator_to_underpasses(underpass_nodes, intersections["indices"],
                                   intersections["coords"], underpass_info, saw)

   return underpass_info


def populate_alexander_matrix(saw, proj, t):
   """return alexander matrix of the given saw."""
   # will have to change name of pre_alexander_compile
   underpass_info = pre_alexander_compile(saw, proj)
   I = np.shape(underpass_info)[0]
   alex_mat = np.zeros((I, I))
   
   for k in np.arange(I):
      if underpass_info[k, 1] == k or underpass_info[k, 1] == k+1:
         alex_mat[k, k] = -1
         if k == I-1:
            continue
         else: alex_mat[k, k+1] = 1
      else:
         alex_mat[k, underpass_info[k, 1]] = t - 1
         if underpass_info[k, 0] == 0: # Type I
            alex_mat[k, k] = 1
            if k == I-1:
               continue
            else: alex_mat[k, k+1] = -t
         else: # Type II
            alex_mat[k, k] = -t
            if k == I-1:
               continue
            else: alex_mat[k, k+1] = 1

   return alex_mat
