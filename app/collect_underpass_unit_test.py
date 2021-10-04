from numpy import e

from .alexander import collect_underpass_info
from .generate_chain import generate_closed_chain
from .projection import find_reg_project_rot


def collect_underpass_unit_test():
    try:
        N = 10
        # TODO: create several test cases, and then run each and check for errors
        info = collect_underpass_info()
    except: 
        print("test failed.")
    else:
        print("test passed")
