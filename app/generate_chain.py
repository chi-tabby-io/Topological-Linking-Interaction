import numpy as np
from math import isclose
from numpy.linalg import norm
from scipy.spatial.distance import cdist
from .private.generate_binary_list import gen_all_bin_list
from .private.utilities import pivot_rotations

dirs = gen_all_bin_list(3) # all possible directions in cubic lattice

np.random.seed(0)


# NOTE: generates a chain according to the probability dist. Does not test if
# is closed nor whether is self-intersecting.
def generate_chain_helper_worm(N, shift=False):
    """return a random walk 'chain' with N nodes.
    
    The method uses the 'worm in an apple' approach to generate the chain,
    forbidding moving in the reverse direction along which it arrived to the
    current node. The method also uses a special probability distribution to
    increase the chance of ring closure. The resulting set of all produced
    random walks is not normally distributed, so care must be taken when 
    statistics are run on chains produced from this algorithm.
    
    arguments:
    N - int - the length of the desired chain
    
    return value:
    chain - numpy array of nodes with shape (N, 3) - the generated random walk
    """
    chain = np.zeros((N, 3))
    node = chain[0]
    dir = np.zeros(3) 

    for i in np.arange(1, N):
        probs = special_prob_dist(N - i, node, dirs)
        dir = dirs[np.random.choice(dirs.shape[0], p=probs)]
        new_node = np.add(node, dir)

        j = 0
        while any(np.equal(chain[:i], new_node).all(1)):
            # before doing anything, check whether we are locked out (think snake)
            surrounding = dirs + node
            chain_as_set = {tuple(node) for node in chain[:i]}
            surrounding_as_set = {tuple(node) for node in surrounding}
            if chain_as_set.intersection(surrounding_as_set) is surrounding_as_set:
                return None # No remaining dirs to choose from: give up this attempt
            remaining_surrounding = np.array(list(surrounding_as_set.difference(chain_as_set)))
            new_node = remaining_surrounding[np.random.choice(remaining_surrounding.shape[0])]

            j += 1
            if j == 10000:
                print("probs: {} and node {}\nchain: {}".format(probs, i, chain))

        chain[i] = new_node
        node = new_node
    
    return chain


def v_dot(a): return lambda b: np.dot(a,b)


#alg from: https://biophyenvpol.wordpress.com/2014/11/13/pivot-algorithm-of-self-avoiding-chain-using-python-and-cython/
def generate_chain_helper_pivot(N, num_it):
    rotate_matrices = np.array([[[1,0,0],[0,0,-1],[0,1,0]],[[1,0,0],[0,-1,0],[0,0,-1]]
        ,[[1,0,0],[0,0,1],[0,-1,0]],[[0,0,1],[0,1,0],[-1,0,0]]
        ,[[-1,0,0],[0,1,0],[0,0,-1]],[[0,0,-1],[0,1,0],[-1,0,0]]
        ,[[0,-1,0],[1,0,0],[0,0,1]],[[-1,0,0],[0,-1,0],[0,0,1]]
        ,[[0,1,0],[-1,0,0],[0,0,1]]])

    chain = np.dstack((np.arange(N), np.zeros(N), np.zeros(N)))[0]

    for i in np.arange(num_it):
        pivot = np.random.randint(1, N-1)
        side = np.random.choice([-1,1])

        if side == 1:
            old_chain = chain[0:pivot+1]
            temp_chain = chain[pivot+1:]
        else:
            old_chain = chain[pivot:]
            temp_chain = chain[0:pivot]
        
        sym_op = rotate_matrices[np.random.randint(len(rotate_matrices))] # TODO: change all other examples of this to len
        new_chain = np.apply_along_axis(v_dot(sym_op), 1, temp_chain - chain[pivot]) + chain[pivot]

        overlap = cdist(new_chain, old_chain)
        overlap = overlap.flatten()

        if len(np.nonzero(overlap)[0]) != len(overlap):
            continue
        else:
            if side == 1:
                chain = np.concatenate((old_chain, new_chain), axis=0)
            elif side == -1:
                chain = np.concatenate((new_chain, old_chain), axis=0)

    chain -= chain[0]
    # May not want to use this method, very low prob of closing...
    return chain


def special_prob_dist(n, node, dirs):
    """return array of probs for all possible directions at a given step.
    
    This function is used in the context of generate_chain only. It computes
    the probabilities associated with each possible direction in the
    body-centered lattice, dependent on where we are along the total length
    of the generated chain. This is to make it more likely that the chain
    so-generated returns to the starting point.
    
    Some difficulties to overcome were the edge-cases where when we are only a 
    few steps away from the origin, the only way to close the chain is to move
    backward. We brute-force through this issue by returning None and rejecting 
    that return value
    
    arguments:
    n - int - the length of the chain that will be generated
    node - numpy array with shape (3, 1) - the current node
    dirs - numpy array with shape (8, 3) - set of all directions in 
    body-centered lattice
    
    return value:
    probs - numpy array with shape (8, 1) - probabilities associated with
    dirs, which will be used to choose the direction for the chain to travel
    in the next step.
    """
    probs = []

    for i in np.arange(dirs.shape[0]):
        p = 1.0
        for j in np.arange(dirs[i].shape[0]):
            p *= (n - dirs[i][j] * node[j]) / (2 * n)
            if p < 0:
                p = 0
        probs.append(p)

    probs = np.array(probs)
    # if had to make any probs 0, must renormalize
    if np.any(probs[:] == 0):
        probs = probs / sum(probs)

    return probs


def generate_closed_chain(N, shift=True, num_it=1000, pivot=False):
    chain = None
    attempts = 0

    while True:
        
        if pivot:
            chain = generate_chain_helper_pivot(N, num_it)
        else:
            chain = generate_chain_helper_worm(N, shift)
        
        attempts += 1
        if is_closed(chain):
            break
    
    # chain length is N + 1, just so we get that last link in within visualization
    # TODO: change all functions internal to python so that we have len(chain) == 20
    # only within our javascript code will we add the extra origin node (because why
    # else do we need this node?) 
    chain = np.append(chain, np.array([chain[0]]), axis=0)
    dtype = [('chain', np.float64, (N+1,3)), ('attempts', np.uintc)]
    return np.array((chain.tolist(), attempts), dtype=dtype)


SQRT_3 = 1.7320508075688772  # the distance between each link

def is_closed(chain):
    if chain is None: return False
    else: return True if isclose(norm(chain[0] - chain[-1]), SQRT_3) else False


def is_self_intersecting(chain):
    unique = np.unique(chain, axis=0)
    return True if (chain.shape[0] != unique.shape[0]) else False 
