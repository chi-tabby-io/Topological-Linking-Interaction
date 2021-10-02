import numpy as np

eps = 1.0e-12 # convenient small value for double comparison

def validate_intersect_in_segment(p0, p1, p2):
   """return True if p0 in bounding box of p1 and p2, else return False."""
   return True if min(p1[0], p2[0]) <= p0[0] <= max(p1[0], p2[0]) and \
          min(p1[1], p2[1]) <= p0[1] <= max(p1[1], p2[1]) else False


# algorithm from: https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
def find_intersection_2D(p1, p2, p3, p4):
   """from line segments p1p2 and p3p4, return the intersection if it exists.
   
   Also determines whether the intersection lies on the line segment p1p2 (this
   is sufficient for determining whether the intersection lies within both
   line segments.

   The pair of lines is modeled as a linear system of the following form:

      a1*x + b1*y = c1
      a2*x + b2*y = c2

   and is solved via Cramer's Rule
   
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

      if validate_intersect_in_segment(intersect, p1, p2):
         return intersect
      else: return None


def is_underpass(k, j, intersect, saw):
   """return True if segment pkpk_1 is an underpass of pjpj_1, else return False.
   
   This method assumes that intersect is a valid intersection for the line 
   segments pkpk_1 and pjpj_1. It then uses the eqns for a line in 3D found
   here: https://byjus.com/maths/equation-line/ to calculate the z-value
   of the corresponding point in the SAW to determine whether pkpk+1 is
   an underpass or not.
   
   arguments:
   k - int - the index of node pk within the SAW
   j - int the index of node pj within the SAW
   intersect - numpy array with shape (2,1) - the intersection within the projection,
   with format (x, y)
   saw - numpy array with shape (N, 3) - the SAW where underpasses will be found from
   
   return value:
   boolean - True if pkpk_1 is an underpass, else False
   """
   pk = saw[k]
   pk_1 = saw[k+1]
   pj = saw[j]
   pj_1 = saw[j+1]
   zk = pk[3] + (pk_1[3] - pk[3])*(intersect[0] - pk[0]) / (pk_1[0] - pk[0])
   zj = pj[3] + (pj_1[3] - pj[3])*(intersect[0] - pj[0]) / (pj_1[0] - pj[0])
   return True if (zj - zk > eps) else False
   

def collect_underpass_info(saw, proj):
   """return numpy array with underpass type and index of generator.
   
   This function collects the necessary topological information about the
   SAW in order to populate its Alexander Matrix. The two pieces of 
   information are the corresponding overpass generator index (same as the
   index of the underpass) and the underpasse's type (type I or type II), 
   codified as either 0 or 1.
   
   arguments:
   saw - numpy array with shape (N, 3) - the SAW where underpasses will be found from
   proj - numpy array with shape (N, 2) - the regular projection used to find intersections
   
   return value:
   underpass_info - numpy array of shape (I, 2) - the array of information for each underpass.
   I is the number of underpasses (not known a priori) The format for each subarray is
   [{0|1}, {k}] where k runs from zero to I - 1.
   """
   # FIXME: assigning overpass number to k is WRONG!!! 
   underpass_info = []
   underpass_hash = []
   overpass_hash = []
   under_index = 0
   over_index = 0
   for k in np.arange(proj.shape[0]-1):
      # collecting pre and post j, j+1 information so we loop through every node except those
      # with index j and j+1
      temp_index_array = np.arange(proj.shape[0])
      pre_j = temp_index_array[:k]
      post_j_1 = temp_index_array[k+2:]
      temp_index_array = np.concatenate((pre_j,post_j_1), axis=None)
      for j in temp_index_array:
         pk = proj[k][:2]
         pk_1 = proj[k+1][:2]
         pj = proj[j][:2]
         pj_1 = proj[j+1][:2]
         intersect = find_intersection_2D(pk, pk_1, pj, pj_1)
         if intersect is not None:
            if is_underpass(k, j, intersect, saw):
               info = []
               v1 = np.subtract(pk, pj)
               v2 = np.subtract(pk, pk_1)
               if np.cross(v1, v2) == 1: # Type I
                  info.append[0]
               else: # Type II
                  info.append[1]
               # info.append[k]
               underpass_hash.append([under_index, intersect])
               under_index += 1
               # check overpass hash for same intersect, if exists, put overpass
               # index into underpass_info
               underpass_info.append(info)
            else:
               overpass_hash.append([over_index, intersect])
               over_index += 1
               # check underpass hash for the same intersect, if exists, put
               # that overpass index into underpass_info
   
   # let's re-do the overpass assignment:
   # run through 
   return np.array(underpass_info)


def populate_alexander_matrix(saw, proj, t):

   underpass_info = collect_underpass_info(saw, proj)
   I = np.shape(underpass_info)[0]
   alex_mat = np.zeroes((I, I))

   for k in np.arange(I):
      if underpass_info[k, 1] == k:
         alex_mat[k, k] = -1
      elif underpass_info[k, 1] == k+1:
         alex_mat[k, k+1] = 1
      else:
         if underpass_info[k, 0] == 0: # Type I
            alex_mat[k, k] = 1
            alex_mat[k, k+1] = -t
         else: # Type II
            alex_mat[k, k] = -t
            alex_mat[k, k+1] = 1
         alex_mat[k, underpass_info[k, 1]] = t - 1

   return alex_mat
