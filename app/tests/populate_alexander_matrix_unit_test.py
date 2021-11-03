import json

import numpy as np

from ..alexander import (evaluate_alexander_polynomial,
                         populate_alexander_matrix)
from ..private.utilities import pre_alexander_compile, rot_saw_xy
from ..projection import find_reg_project

# TODO: change from absolute path (rel to project root) to variable
TEST_CASE_N_18 = "app/tests/test_knots_N_18.json"

#TODO: create test cases where you know what the matrix should look like
def populate_alexander_matrix_unit_test():
    with open(TEST_CASE_N_18) as ifile:
        print("Loading test data from file {}...".format(TEST_CASE_N_18))
        in_data = json.load(ifile)
        test_chains = in_data["tests"]
        # validation_list = in_data["validation_list"]
        print("Finished loading test data.")
        for chain in test_chains:
            alexander_mat = populate_alexander_matrix(chain,
                                                      find_reg_project(chain),
                                                      -1)
            alexander_poly = evaluate_alexander_polynomial(chain, -1)

            # print(alexander_mat, end='\n\n')
            print(alexander_poly, end='\n\n')
