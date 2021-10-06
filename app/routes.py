import numpy as np
from flask import jsonify, render_template, request

from app import app

from .collect_underpass_unit_test import collect_underpass_unit_test
from .generate_chain import chain_to_JSON, generate_closed_chain
from .intersect_unit_test import intersect_unit_test
from .projection import find_reg_project_rot, rot_saw_xy


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
        # current algorithm takes about 10-30s to generate closed,
        # non-intersecting chain of length 50 (05/16/2021)
        # NOTE: just don't put odd inputs O_O
        # FURTHER NOTE: a knot will NOT form if N <= 23
        #N = 140 # the length of the SAW - definitely not the best place to put this
        #saw = generate_closed_chain(N)[0]
        saw = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, -1.0], [0.0, 2.0, -2.0], [-1.0, 3.0, -1.0], [0.0, 4.0, 0.0], [1.0, 5.0, -1.0], [0.0, 6.0, -2.0], [1.0, 7.0, -3.0], [0.0, 8.0, -4.0], [1.0, 9.0, -5.0], [2.0, 8.0, -6.0], [1.0, 9.0, -7.0], [2.0, 10.0, -8.0], [3.0, 9.0, -7.0], [4.0, 10.0, -8.0], [3.0, 11.0, -9.0], [2.0, 10.0, -10.0], [3.0, 9.0, -9.0], [4.0, 8.0, -10.0], [5.0, 7.0, -9.0], [4.0, 6.0, -8.0], [3.0, 5.0, -7.0], [2.0, 6.0, -8.0], [1.0, 7.0, -9.0], [0.0, 6.0, -10.0], [-1.0, 5.0, -9.0], [-2.0, 4.0, -10.0], [-1.0, 5.0, -11.0], [0.0, 4.0, -10.0], [1.0, 5.0, -11.0], [2.0, 4.0, -10.0], [3.0, 5.0, -9.0], [4.0, 4.0, -10.0], [3.0, 3.0, -11.0], [4.0, 2.0, -12.0], [3.0, 1.0, -13.0], [4.0, 0.0, -12.0], [3.0, -1.0, -11.0], [4.0, -2.0, -12.0], [5.0, -1.0, -11.0], [6.0, 0.0, -12.0], [7.0, 1.0, -13.0], [8.0, 2.0, -12.0], [9.0, 3.0, -11.0], [10.0, 4.0, -12.0], [11.0, 3.0, -11.0], [10.0, 2.0, -10.0], [11.0, 1.0, -11.0], [12.0, 0.0, -10.0], [11.0, 1.0, -9.0], [12.0, 2.0, -10.0], [13.0, 3.0, -9.0], [14.0, 2.0, -10.0], [15.0, 1.0, -9.0], [16.0, 0.0, -8.0], [17.0, -1.0, -9.0], [18.0, 0.0, -8.0], [19.0, -1.0, -7.0], [20.0, -2.0, -6.0], [19.0, -1.0, -5.0], [18.0, -2.0, -4.0], [17.0, -3.0, -5.0], [16.0, -4.0, -6.0], [15.0, -5.0, -5.0], [14.0, -4.0, -6.0], [13.0, -5.0, -5.0], [12.0, -6.0, -6.0], [13.0, -7.0, -7.0], [12.0, -8.0, -6.0], [11.0, -7.0, -5.0], [10.0, -6.0, -6.0], [9.0, -7.0, -5.0], [10.0, -8.0, -4.0], [9.0, -9.0, -5.0], [10.0, -10.0, -6.0], [9.0, -11.0, -5.0], [10.0, -12.0, -4.0], [9.0, -13.0, -3.0], [10.0, -14.0, -2.0], [9.0, -13.0, -1.0], [8.0, -12.0, -2.0], [7.0, -13.0, -3.0], [6.0, -12.0, -2.0], [7.0, -13.0, -1.0], [8.0, -14.0, -2.0], [7.0, -15.0, -1.0], [8.0, -14.0, 0.0], [9.0, -13.0, 1.0], [10.0, -12.0, 0.0], [9.0, -11.0, -1.0], [8.0, -10.0, 0.0], [7.0, -9.0, -1.0], [6.0, -10.0, -2.0], [7.0, -11.0, -1.0], [8.0, -12.0, 0.0], [7.0, -13.0, 1.0], [8.0, -14.0, 2.0], [9.0, -15.0, 1.0], [8.0, -16.0, 2.0], [7.0, -15.0, 3.0], [6.0, -14.0, 4.0], [5.0, -15.0, 3.0], [4.0, -14.0, 4.0], [3.0, -13.0, 3.0], [4.0, -12.0, 4.0], [3.0, -11.0, 3.0], [2.0, -10.0, 4.0], [3.0, -9.0, 3.0], [2.0, -8.0, 4.0], [3.0, -7.0, 3.0], [2.0, -8.0, 2.0], [3.0, -9.0, 1.0], [4.0, -10.0, 0.0], [3.0, -11.0, 1.0], [2.0, -12.0, 2.0], [1.0, -13.0, 1.0], [0.0, -12.0, 2.0], [1.0, -11.0, 1.0], [0.0, -10.0, 0.0], [-1.0, -9.0, -1.0], [0.0, -8.0, -2.0], [-1.0, -7.0, -3.0], [0.0, -6.0, -2.0], [-1.0, -5.0, -3.0], [0.0, -4.0, -2.0], [1.0, -3.0, -1.0], [2.0, -4.0, -2.0], [1.0, -5.0, -1.0], [0.0, -4.0, 0.0], [-1.0, -5.0, 1.0], [0.0, -4.0, 2.0], [1.0, -3.0, 3.0], [0.0, -2.0, 2.0], [-1.0, -3.0, 3.0], [-2.0, -4.0, 2.0], [-3.0, -3.0, 3.0], [-2.0, -2.0, 2.0], [-1.0, -1.0, 1.0], [0.0, -2.0, 0.0], [1.0, -1.0, 1.0], [0.0, 0.0, 0.0]])
        #saw = rot_saw_xy(saw)
        xy_project = find_reg_project_rot(saw)
        collect_underpass_unit_test()
        payload = chain_to_JSON(xy_project)
        #payload = chain_to_JSON(saw)
        return jsonify(payload)  # serialize and use JSON headers


@app.route("/")
@app.route("/index")
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template("index.html")
