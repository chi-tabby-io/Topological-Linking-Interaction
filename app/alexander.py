import numpy as np

eps = 1.0e-12 # convenient small value for double comparison

def validate_intersect_in_segments(p0, p1, p2, p3, p4):
   """return True if p0 in bounding box of p1p2 AND p3p4, else return False."""
   in_line_1 = min(p1[0], p2[0]) < p0[0] < max(p1[0], p2[0]) and \
          min(p1[1], p2[1]) < p0[1] < max(p1[1], p2[1])
   in_line_2 = min(p3[0], p4[0]) < p0[0] < max(p3[0], p4[0]) and \
          min(p3[1], p4[1]) < p0[1] < max(p3[1], p4[1])
   
   return True if (in_line_1 and in_line_2) else False


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
   
   

def pre_alexander_compile(saw, proj):
   """return underpass type and overpassing generators as an array.
   
   This function uses the common intersection for each underpass and overpass
   as a sort of common key to collect the important info in underpass_info (i.e.
   the underpass type) and the important info in overpasses (i.e. the overpass
   index) into one array.
   
   arguments:
   saw - numpy array with shape (N, 3) - the SAW where underpasses will be 
   found from
   proj - numpy array with shape (N, 2) - the regular projection of the SAW
   
   return value:
   out - numpy array with shape (I, 2), where I is the number of intersections.
   Is the array of relevant information we need to populate Alexander Matrix.
   """
   underpass_info = collect_underpass_info(saw, proj)
   overpasses = collect_overpass_intersects(saw, proj)
   out = []
   for k in np.arange(np.shape(underpass_info)[0]):
      for i in np.arange(np.shape(overpasses)[0]):
         # may have to set a tolerance on this, even though, theoretically,
         # the intersection should be the same
         if np.array_equal(underpass_info[k, 1], overpasses[i]):
            out.append([underpass_info[k, 0], i])
   return np.array(out)


def collect_underpass_info(saw, proj):
   """return array of underpass type and intersection.
   
   This function loops through the projection twice, such that for each line
   segment, we test whether it is intersected by any other line segment. We
   then check whether at the current line segment, whether such an intersection
   is an underpass. We then determine the type of underpass (either type I or
   type II, with type I being "left-handed" and type II being ""right-handed"
   from the persective of the underpass) and collect the results in 
   underpass_info.

   NOTE: saw is not the original SAW, but should be the already rotated one, in 
   order to be in correct alignment with the projection

   arguments:
   saw - numpy array with shape (N, 3) - the SAW where underpasses will be 
   found from
   proj - numpy array with shape (N, 2) - the regular projection of the SAW

   return value:
   underpass_info - a ragged numpy array. Each element along axis 0 is a pair, 
   with the first element being the type of underpass, and the second being
   the coordinates of the underpass.
   """
   
   underpass_info = []

   for k in np.arange(proj.shape[0]-1):
      for j in np.arange(proj.shape[0]-1):
         if j == k-1 or j == k or j == k+1:
            continue
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
                  info.append(0)
               else: # Type II
                  info.append(1)
               info.append(intersect)
               underpass_info.append(info)

   return np.array(underpass_info,dtype=object)


def collect_overpass_intersects(saw, proj):
   """return intersections that are overpasses as an array.
   
   This method is similar to collect_underpass_info, except that it only
   collects the intersections in the order that they are found to be overpasses.
   This is the only information that we need about the overpasses.
   
   NOTE: saw is not the original SAW, but should be the already rotated one, in 
   order to be in correct alignment with the projection
   
   arguments:
   saw - numpy array with shape (N, 3) - the SAW where underpasses will be 
   found from
   proj - numpy array with shape (N, 2) - the regular projection of the SAW

   return value:
   overpass_info - a numpy array with shape (I, 2), where I is the number of
   intersections. Each entry along axis 0 is a (2,1) array encoding the 
   coordinates of the ith overpass.
   """
   overpass_info = []
   
   for i in np.arange(proj.shape[0]-1):
      for j in np.arange(proj.shape[0]-1):
         if j == i-1 or j == i or j == i+1:
            continue
         pi = proj[i][:2]
         pi_1 = proj[i+1][:2]
         pj = proj[j][:2]
         pj_1 = proj[j+1][:2]
         intersect = find_intersection_2D(pi, pi_1, pj, pj_1)
         if intersect is not None:
            if not is_underpass(i, j, intersect, saw):
               overpass_info.append(intersect)

   return np.array(overpass_info)


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
