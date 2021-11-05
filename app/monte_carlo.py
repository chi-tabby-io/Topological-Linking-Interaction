import os

import matplotlib.pyplot as plt
import numpy as np

from .alexander import evaluate_alexander_polynomial, populate_alexander_matrix
from .generate_chain import generate_closed_chain
from .private.utilities import rot_saw_xy
from .projection import find_reg_project


def basic_monte_carlo_sim(num_nodes, num_chains, table=True):
    """return None. Print table and final statistics for monte carlo sim.
    
    We are concerned with the distributions of knot formation as well as
    number of attempts."""
    raw_data = np.zeros((num_chains,2)) # first element is result of is_knotted, second is num attempts
    if table:
        print("+-----------------+---  MONTE CARLO SIMULATION ---+----------------+")
        print("|    CHAIN ID     | ALEXANDER POLYNOMIAL (t = -1) |   IS A KNOT?   |")
        print("+-----------------+-------------------------------+----------------+")
    
    # run the simulation
    for i in np.arange(num_chains):
        chain, num_attempts = generate_closed_chain(num_nodes)
        alex_mat = populate_alexander_matrix(rot_saw_xy(chain), find_reg_project(chain), -1)
        alex_poly = evaluate_alexander_polynomial(alex_mat)
        is_knotted = not (alex_poly == 1)
        if table:
            print("|{:^17}|{:^31}|{:^16}|".format(i+1, alex_poly, is_knotted))
            print("+-----------------+-------------------------------+----------------+")

        raw_data[i][0] = is_knotted
        raw_data[i][1] = num_attempts

    return raw_data
