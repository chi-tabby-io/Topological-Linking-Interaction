import numpy as np

# This file implements our closed chain alg
# The length of every polymer is the same
N = 100 
epsilon = 1.e-13
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
    pass

def is_closed(chain):
    
    if np.linalg.norm(chain[0] - chain[chain.size-1]) < 1.0 :
        return True
    else:
        return False

# essentially, calls 
def generate_closed_chain(N):
    
    this_chain = generate_polymer(N)

    while not is_closed(this_chain):
        this_chain = generate_polymer(N)
    
    return this_chain




