
import numpy as np

from .private.utilities import pre_alexander_compile


def populate_alexander_matrix(saw, proj, t):
   """return alexander matrix of the given saw.
   
   We are using the logic from the guiding paper for this project (soon to 
   be in the README!) in order to return the alexander matrix of the given
   saw.
   
   arguments:
   saw - numpy array with shape (N, 3) - the SAW whose alexander matrix we wish
   to calculate
   proj - numpy array with shape (N, 2) - the regular projection of saw
   t - float - the polynomial parameter
   
   return value:
   alex_mat - numpy array with shape (I, I) where I is the number of underpasses.
   """
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
