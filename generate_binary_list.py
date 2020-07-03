import numpy as np

# for ease of use, the exported function
def gen_all_bin_list(N):
    all_poss = []
    poss = np.empty(N)
    gen_bin_list_helper(N, all_poss, poss, 0)
    return np.array(all_poss)

# helper function which recursively generates all possible binary lists
# of a given length N
def gen_bin_list_helper(N, all_poss, poss, i):
    if i == N:
        # make the necessary transformation (0, 1) -> (-1, 1) because
        # we are working with unit random walks
        poss = 2*poss - 1
        # once we've reached the end of this possibility, at it to all
        # possible list
        all_poss.append(poss)
        return
    
    # compute all permutations with a 0 in the ith position
    poss[i] = 0
    gen_bin_list_helper(N, all_poss, poss, i+1)

    # compute all permutations with a 1 in the ith postion
    poss[i] = 1
    gen_bin_list_helper(N, all_poss, poss, i+1)

