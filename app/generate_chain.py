import json

import numpy as np
from numpy.linalg import norm

from .private.generate_binary_list import gen_all_bin_list

sqrt_3 = 1.7320508075688772  # the distance between each link
epsilon = 1.0e-12 # convenient small value for double comparison
dirs = gen_all_bin_list(3) # all possible directions in cubic lattice


# assume shape of arr is (n, m)
def index_of(seq, arr):
    """return index of a subarray within given array, if it exists."""
    for i in np.arange(arr.shape[0]):
        if np.array_equal(seq, arr[i]):
            return i
    return -1


# NOTE: generates a chain according to the probability dist. Does not test if
# is closed nor whether is self-intersecting.
def generate_chain(N, pivot):
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
    node = np.zeros(3) # initialize first node at the origin
    chain = np.zeros((N, 3))
    dir = np.zeros(3) # initialize dir array before loop
    for i in np.arange(1, N):
        probs = special_prob_dist(N - i, node, dirs)
        new_dir = dirs[np.random.choice(dirs.shape[0], p=probs)]
        # backwards movements are prohibited
        while np.array_equal(dir + new_dir, np.zeros(3)):
            # silly case in which only possible new direction is neg of previous
            if abs(probs[index_of(new_dir, dirs)] - 1.0) < epsilon: 
                return None
            new_dir = dirs[np.random.choice(dirs.shape[0], p=probs)]
        # vector addition of node and the chosen dir makes a new node
        node = np.add(node, new_dir)

        # we have an intersection
        if node.tolist() in chain.tolist(): 
            # if we are using model 2, then pivot the chain in a given direction
            if pivot:
                delta = 0.1 # this is the amount by which we pivot interesting to play with
                phi = np.random.uniform(0, 2*np.pi)
                theta = np.random.uniform(0, np.pi)
                pivot_dir = np.zeros(3)
                pivot_dir[0] = np.cos(phi) * np.sin(theta)
                pivot_dir[1] = np.sin(phi) * np.sin(theta)
                pivot_dir[2] = np.cos(theta)
                node = np.add(node, delta * pivot_dir)
            else: return None
        chain[i] = node
        dir = new_dir

    return chain


# return weights for chosen directions given a prob dist (see ref paper)
def special_prob_dist(n, node, dirs):
    """return array of probs for all possible directions at a given step.
    
    This function is used in the context of generate_chain only. It computes
    the probabilities associated with each possible direction in the
    body-centered lattice, dependent on where we are along the total length
    of the generated chain. This is to make it more likely that the chain
    so-generated returns to the starting point.
    
    Some difficulties to overcome were the edge-cases where when we are only a 
    few steps away from the origin, the only way to close the chain is to move
    backward. We brute-force through this issue by letting the chain be
    generated anyway, letting the chain be rejected in the generate_closed_chain
    function.
    
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
    # for each direction, assign a unique probability of being chosen
    for i in np.arange(dirs.shape[0]):
        p = 1.0
        # loop over all coordinates
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


def is_closed(chain):
    if abs(np.linalg.norm(chain[0] - chain[chain.shape[0] - 1]) - sqrt_3) < epsilon:
        return True
    else:
        return False


# essentially uses the functions above as helpers to generate a closed chain
def generate_closed_chain(N, pivot=False):

    chain = generate_chain(N, pivot)

    # this step may take a while...but our pdf, once implemented, gives us a
    # greater chance that the randomly generated chain will be closed
    # Note that attempts is for testing the efficiency of our alg
    attempts = 0

    while chain is None: # None means is self-intersecting...
        chain = generate_chain(N, pivot)
        attempts += 1
        # if attempts % 50 == 0:
        #     print("Current number of attempts:" + str(attempts))

    chain = np.append(chain, np.array([chain[0]]), axis=0)
    return np.array([chain, attempts], dtype=object) # turn into structured array


# detects whether is self-intersecting iff there exist two of the same vertex
def is_self_intersecting(chain):
    unique = np.unique(chain, axis=0)
    if chain.shape[0] != unique.shape[0]:
        return True
    else:
        return False
