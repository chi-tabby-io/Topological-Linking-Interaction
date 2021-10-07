import json

import numpy as np

from .alexander import collect_underpass_info
from .projection import find_reg_project_rot, rot_saw_xy

TEST_CASE_N_8 = "test_chains_N8.json"
TEST_CASE_N_30 = "test_chains_N30.json"
TEST_CASE_N_90 = "test_chains_N90.json"
TEST_CASE_N_140 = "test_chains_N140.json"


def export_test_chains_to_JSON(test_chain_list, file):
    tests_list = []
    for i in np.arange(np.shape(test_chain_list)[0]):
        test_list = test_chain_list[i].tolist()
        tests_list.append(test_list)
    #TODO: check whether file exists or not: create if not, append if it does
    print("placing test arrays into file {}...".format(file))
    with open (file, "w") as ofile:
        json.dump(tests_list, ofile)
        print("Finished placing all test chains into file {}".format(file))


def collect_underpass_unit_test():
    with open(TEST_CASE_N_30) as ifile:
        print("Loading test data from file {}...".format(TEST_CASE_N_8))
        in_data = json.load(ifile)
        tests = in_data["tests"]
        validation_list = in_data["validation_list"]
        print("Finished loading test data.")
        for i in np.arange(np.shape(tests)[0]):  
            try:
                project = find_reg_project_rot(tests[i])
                test_info = collect_underpass_info(rot_saw_xy(tests[i]), project)
                print(test_info)
                assert np.shape(test_info)[0] == validation_list[i]
            except AssertionError: 
                print("test {} failed.".format(i+1))
            else:
                print("test {} passed.".format(i+1))
