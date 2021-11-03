import os

import numpy as np
from flask import jsonify, render_template, request

from app import app
from app.private.utilities import construct_json_validation_from_file

# from .collect_overpass_intersects_test import \
#     collect_overpass_intersects_unit_test
#from .collect_underpass_unit_test import collect_underpass_unit_test
from .generate_chain import generate_closed_chain
from .private.utilities import chain_to_JSON
from .projection import find_reg_project_rot, rot_saw_xy
from .tests.intersect_unit_test import intersect_unit_test
from .tests.populate_alexander_matrix_unit_test import \
    populate_alexander_matrix_unit_test


@app.route("/data_helper", methods=["GET", "POST"])
def data_helper():
    """return json representation of SAW for GET request, return OK, 200 else.
    
    This function handles GET and POST requests from our web app. So far the 
    POST requests are quite simple, but in the future, we may handle more
    complex tasks here. The GET request is likewise very simply, only handing
    over the serialized SAW information to the web app."""
    if request.method == "POST": # POST request
        print("Incoming..")
        print(request.get_json())  # parse as JSON
        return "OK", 200

    else: # GET request
        #have to make a check for posix or windows
        test_code_file = os.getcwd() + "\\app\\tests\\test_knots_N_18.txt"
        construct_json_validation_from_file(test_code_file)

        # payload = code_to_json_chain()
        return jsonify(payload)
        # # current algorithm takes about 10-30s to generate closed,
        # # non-intersecting chain of length 50 (05/16/2021)
        # # NOTE: just don't put odd inputs O_O
        # # FURTHER NOTE: a knot will NOT form if N <= 23
        # N = 8 # the length of the SAW - definitely not the best place to put this
        # saw = generate_closed_chain(N)[0]
        # # rotate to match what our program uses behind the scenes (for debugging)
        # saw = rot_saw_xy(saw)
        # xy_project = find_reg_project_rot(saw)
        # #collect_underpass_unit_test()
        # #collect_overpass_intersects_unit_test()
        # #pre_alexander_compile_unit_test()
        # populate_alexander_matrix_unit_test()
        # payload = chain_to_JSON(xy_project)
        # #payload = chain_to_JSON(saw)
        # return jsonify(payload)  # serialize and use JSON headers


@app.route("/")
@app.route("/index")
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template("index.html")
