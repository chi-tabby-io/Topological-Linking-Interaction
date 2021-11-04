import numpy as np

from .alexander import evaluate_alexander_polynomial, populate_alexander_matrix
from .generate_chain import generate_closed_chain
from .private.utilities import rot_saw_xy
from .projection import find_reg_project


def basic_monte_carlo_sim(num_nodes, num_chains, table=True):

    total_knots = 0
    if table:
        print("+-----------------+---  MONTE CARLO SIMULATION ---+----------------+")
        print("|    CHAIN ID     | ALEXANDER POLYNOMIAL (t = -1) |   IS A KNOT?   |")
        print("+-----------------+-------------------------------+----------------+")
    for i in np.arange(num_chains):
        chain = generate_closed_chain(num_nodes)[0]
        alex_mat = populate_alexander_matrix(rot_saw_xy(chain), find_reg_project(chain), -1)
        alex_poly = evaluate_alexander_polynomial(alex_mat)
        is_knotted = not (alex_poly == 1)
        if table:
            print("|{:^17}|{:^31}|{:^16}|".format(i+1, alex_poly, is_knotted))
            print("+-----------------+-------------------------------+----------------+")

        if is_knotted: total_knots += 1
    print()
    print("final results: total number of knots was {}".format(total_knots))
