import numpy as np
from generate_binary_list import gen_all_bin_list

# This file implements our closed chain alg
# The length of every polymer is the same
N = 100 
epsilon = 1.e-13
directions = gen_all_bin_list(3)

# generates a polymer of length N. May or may not be closed. The probability
# that the polymer is closed is given by the distribution function:
#               
#            P(n, r, delta) = Prod_k((n-delta_k*x_k)/(2n))
# 
# Where n represents...I am not sure. r is the position vector (of what???) and
# delta is a vector governing the direction of the next link
# 
# The polymer is generated on a "body-centered" lattice (something something
# solid state physics) and is, by construction, non-interacting (we do not
# allow the random walk to move to where it has come from)

def generate_chain(N):
    # initialize first node at the origin
    this_node = np.zeros(3)
    this_chain = np.empty(N)
    # initialize first element of our chain as the first node
    this_chain[0] = this_node
    
    # the loop which will generate and add each node to our chain
    for i in np.arange(1, N):
        # this is where we will weight our random choice with the pdf 
        # discussed above
        new_dir = np.random.choice(directions)
        # now we get a new node directed somewhere within our lattice
        this_node = np.add(this_node, new_dir)
        # add the new node to our chain
        this_chain[i] = this_node

    return this_chain

def is_closed(chain):
    
    if np.linalg.norm(chain[0] - chain[chain.size-1]) < 1.0 :
        return True
    else:
        return False

# essentially uses the functions above as helpers to generate a closed chain
def generate_closed_chain(N):
    
    this_chain = generate_polymer(N)

    # this step may take a while...but our pdf gives us a greater chance
    # that the randomly generated chain will be closed
    while not is_closed(this_chain):
        this_chain = generate_polymer(N)
    
    return this_chain




