import json

import numpy as np

from .alexander import collect_overpass_intersects
from .projection import find_reg_project_rot, rot_saw_xy

TEST_CASE_N_8 = "test_chains_N8.json"
TEST_CASE_N_30 = "test_chains_N30.json"
TEST_CASE_N_90 = "test_chains_N90.json"
TEST_CASE_N_140 = "test_chains_N140.json"

def collect_overpass_intersects_unit_test():
    with open(TEST_CASE_N_90) as ifile:
        print("Loading test data from file {}...".format(TEST_CASE_N_8))
        in_data = json.load(ifile)
        tests = in_data["tests"]   
        validation_list = in_data["validation_list"]
        for i in np.arange(np.shape(tests)[0]):
            try:
                project = find_reg_project_rot(tests[i])
                test_info = collect_overpass_intersects(rot_saw_xy(tests[i]),project)
                print(np.shape(test_info)[0])
                assert np.shape(test_info)[0] == validation_list[i]
            except AssertionError:
                print("test {} failed.".format(i+1))
            else:
                print("test {} passed.".format(i+1))
