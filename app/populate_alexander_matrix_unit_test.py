import json

import numpy as np

from.alexander import populate_alexander_matrix, pre_alexander_compile
from .projection import find_reg_project_rot, rot_saw_xy

# TEST_CASE_N_8 = "test_chains_N8.json"
# TEST_CASE_N_30 = "test_chains_N30.json"
# TEST_CASE_N_90 = "test_chains_N90.json"
# TEST_CASE_N_140 = "test_chains_N140.json"
TEST_CASE_N_18 = "populate_alexander_matrix_test_chains_N18.json"

#TODO: create test cases where you know what the matrix should look like
def populate_alexander_matrix_unit_test():
    with open(TEST_CASE_N_18) as ifile:
        print("Loading test data from file {}...".format(TEST_CASE_N_18))
        in_data = json.load(ifile)
        tests = in_data["tests"]
        # validation_list = in_data["validation_list"]
        print("Finished loading test data.")
        for i in np.arange(np.shape(tests)[0]):  
            project = find_reg_project_rot(tests[i])
            pre_results = pre_alexander_compile(rot_saw_xy(tests[i]), project)
            print(pre_results)
            results = populate_alexander_matrix(rot_saw_xy(tests[i]), project, -1)
            #print(results)
            # try:
            #     assert np.shape(test_info)[0] == validation_list[i]
            # except AssertionError: 
            #     print("test {} failed.".format(i+1))
            # else:
            #     print("test {} passed.".format(i+1))
