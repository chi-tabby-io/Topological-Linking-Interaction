import json
import numpy as np
from .generate_binary_list import gen_all_bin_list

# This file implements our closed chain alg
sqrt_3 = 1.7320508075688772 # the distance between each link
epsilon = 1.e-12
dirs = gen_all_bin_list(3)

def normalize_elems(array):
    for i in np.arange(array.shape[0]):
        array[i] = array[i] / np.linalg.norm(array[i])
    return array

# only need this functionality if implementing face-centered vertices
# dirs = normalize_elems(dirs)

# assume shape of arr is (n, m)
def index_of(seq, arr):
    for i in np.arange(arr.shape[0]):
        if np.array_equal(seq, arr[i]):
            return i
    return -1

# generates a polymer of length N. May or may not be closed. The probability
# that the polymer is closed is given by the distribution function:
#               
#            P(n, r, delta) = Prod_k((n-delta_k*x_k)/(2n))
# 
# Where n represents...I want to say the number of links left until we get to 
# the end of the chain. r is the position vector of the current node (I think) 
# and delta is a vector governing the direction to the next link
# 
# The polymer is generated on a "body-centered" lattice (easier to see once
# we visualize in three.js)
# 
# TODO: look-up how to construct a non-self-intersecting chain. I have taken
# care of the case when we move back to the previous node, but I take that as
# a trivial case for ensuring non-self-intersection

def generate_chain(N):
    # initialize first node at the origin
    node = np.zeros(3)
    chain = []
    # add the initial node and second node to our chain
    chain.append(node)
    dir_id = np.random.randint(dirs.shape[0])
    dir = dirs[dir_id]
    node = np.add(node, dir)
    chain.append(node)

    poss_dirs = []
    # the loop which will generate and add each node to our chain
    for i in np.arange(2, N):

        # TODO: test prob dist!!!

        new_dir = dirs[np.random.choice(dirs.shape[0], 
                       p=special_prob_dist(N-i, node, dirs))]     
                                                                                                                                           
        # exclude directions which are inverse of previous direction
        # (this would guarantee a self-intersection)
        while np.array_equal(dir + new_dir, np.zeros(3)):
            new_dir = dirs[np.random.randint(dirs.shape[0])]

        # re-assign the index of this direction so that we don't accidentally
        # choose it in the next pass
        dir_id = index_of(dir, dirs)
        # something is wrong
        if dir_id == -1:
            raise IndexError("The direction could not be found.")
        
        # vector addition of node and the chosen dir makes a new node
        node = np.add(node, dir)
        # add the new node to our chain
        chain.append(node)
        dir = new_dir

    return np.array(chain)


# return weights for chosen directions given a prob dist (see ref paper)
def special_prob_dist(n, node, dirs):
    probs = []
    # for each direction, assign a unique probability of being chosen
    for i in np.arange(dirs.shape[0]):
        p = 1.
        for j in np.arange(dirs[i].shape[0]):
            p *= (n - dirs[j]*node[j]) / 2*n
        probs.append(p)

    return np.array(probs)


def is_closed(chain):
    if abs(np.linalg.norm(chain[0] - chain[chain.shape[0]-1]) - sqrt_3) < epsilon:
        return True
    else:
        return False


# essentially uses the functions above as helpers to generate a closed chain
def generate_closed_chain(N):
    
    chain = generate_chain(N)

    # this step may take a while...but our pdf, once implemented, gives us a
    # greater chance that the randomly generated chain will be closed
    # Note that attempts is for testing the efficiency of our alg
    attempts = 0
    while not is_closed(chain):
        chain = generate_chain(N)
        while is_self_intersecting(chain):
            chain = generate_chain(N)
            attempts +=1
        attempts += 1

    print(" took " + str(attempts) + " attempts to generate closed chain")
    
    return np.array([chain, attempts], dtype=object)


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self.obj)


# expected input: numpy ndarray
def chain_to_JSON(chain, file_dumps=False):
    data = {"vertices": chain}

    if file_dumps:
        filename = "vertex_array.json"
        print("Serializing NumPy array into {}...".format(filename))
        # write to file 'chain.json'
        with open(filename, "w") as ofile:
            json.dump(data, ofile, cls=NumpyArrayEncoder)
        print("Done writing serialized NumPy array into {}.".format(filename))
        return ""

    else:
        print("Dumping NumPy Array into JSON string...")
        return json.dumps(data, cls=NumpyArrayEncoder)


# detects whether is self-intersecting iff there exist two of the same vertex
def is_self_intersecting(chain):
    unique = np.unique(chain, axis=0)
    if chain.shape[0] != unique.shape[0]:
        return True
    else:
        return False
