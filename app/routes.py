from flask import jsonify, render_template, request

from app import app

from .collect_underpass_unit_test import collect_underpass_unit_test
from .generate_chain import chain_to_JSON, generate_closed_chain
from .intersect_unit_test import intersect_unit_test
from .projection import find_reg_project_rot


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
        N = 24 # the length of the SAW - definitely not the best place to put this
        saw = generate_closed_chain(N)[0]
        xy_project = find_reg_project_rot(saw)
        collect_underpass_unit_test()
        payload = chain_to_JSON(xy_project)
        return jsonify(payload)  # serialize and use JSON headers


@app.route("/")
@app.route("/index")
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template("index.html")
