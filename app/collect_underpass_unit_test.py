import numpy as np

from .alexander import collect_underpass_info
from .generate_chain import generate_closed_chain
from .projection import find_reg_project_rot, rot_saw_xy


def collect_underpass_unit_test():
    # first, define our test cases (i.e. the saws to test)
    # then, run through each test scenario, asserting is true, and
    # excepting the AssertionError otherwise
    # for now, make simple with N = 8

    # square spanning octants 1 and 3 : projects to xy plane as the unknot
    test_chain_1 = np.array([[0.,0.,0.],[1.,1.,1.],[2.,2.,2.],[1.,1.,3.],
                            [0.,0.,4.],[-1.,-1.,3.],[-2.,-2.,2],[-1.,-1.,1.],
                            [0.,0.,0.]])

    # single crossing (edge case: intersection at location of endpoints)
    test_chain_2 =  np.array([[0.0,0.0,0.0],[1.0,-1.0,1.0],[0.0,-2.0,2.0],
                             [-1.0,-1.0,1.0],[0.0, 0.0,2.0],[-1.0,1.0,3.0], 
                             [-2.0,2.0,2.0], [-1.0,1.0,1.0],[0.0,0.0,0.0]])
    
    # double crossing
    test_chain_3 = np.array([[0.0, 0.0, 0.0],[1.3660254037844386, -1.0, 0.0],
                            [0.9999999999999999, 0.0, 0.0],[0.6339745962155612, -1.0, 0.0],
                            [0.26794919243112236, 0.0, 0.0],[0.6339745962155612, 1.0, 0.0],
                            [-0.7320508075688775, 0.0, 0.0],[-0.36602540378443876, 1.0, 0.0],
                            [0.0, 0.0, 0.0]])
    # simple loop in xz plane
    test_chain_4 = np.array([[0.,0.,0.],[0.,1.,0.],[0.,2.,0.],[0.,2.,1.],
                             [0.,2.,2.],[0.,1.,2.],[0.,0.,2.],[0.,0.,1.],
                             [0.,0.,0.]])

    tests = np.array([test_chain_1, test_chain_2, test_chain_3, test_chain_4])
    test_compare_to = np.array([0,1,3,0]) # number of intersections of each test
    for i in np.arange(np.shape(tests)[0]):  
        try:
            # TODO: debug why case 3 failed
            # TODO: debug is_underpass by throwing out intersections that include
            #       two endpoints...will definitely not be underpass
            project = find_reg_project_rot(tests[i])
            test_info = collect_underpass_info(rot_saw_xy(tests[i]), project)
            assert np.shape(test_info)[0] == test_compare_to[i]
        except AssertionError: 
            print("test {} failed.".format(i+1))
        else:
            print("test {} passed.".format(i+1))
