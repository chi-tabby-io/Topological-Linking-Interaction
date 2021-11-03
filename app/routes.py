import os

import numpy as np
from flask import jsonify, render_template, request

from app import app
from app.alexander import populate_alexander_matrix
from app.private.utilities import construct_json_validation_from_file

from .generate_chain import generate_closed_chain
from .private.utilities import chain_to_JSON
from .projection import find_reg_project, rot_saw_xy
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
        populate_alexander_matrix_unit_test()
        N  = 24
        chain = generate_closed_chain(N)[0]
        payload = chain_to_JSON(chain)
        return jsonify(payload)


@app.route("/")
@app.route("/index")
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template("index.html")
