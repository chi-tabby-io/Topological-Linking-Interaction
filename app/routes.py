import matplotlib.pyplot as plt
import numpy as np
from flask import jsonify, render_template, request

from app import app

from .generate_chain import generate_closed_chain
from .monte_carlo import basic_monte_carlo_sim
from .private.utilities import chain_to_JSON

N  = 18
NUM_CHAINS = 30

#from .projection import find_reg_project, rot_saw_xy
# from .tests.intersect_unit_test import intersect_unit_test
# from .tests.populate_alexander_matrix_unit_test import \
#     populate_alexander_matrix_unit_test


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
        chain = generate_closed_chain(N)[0]
         
        payload = chain_to_JSON(chain)
        return jsonify(payload)


@app.route("/plot.png", methods=["GET"])
def plot():
    raw_data = basic_monte_carlo_sim(N, NUM_CHAINS, table=False)
    # analyze the results
    total_knots = len(np.where(raw_data[:,0]))
    #attempt_stats = np.array([np.mean(raw_data[:,1]), np.std(raw_data[:,1])])

    # plot attempt stats as hist
    hist, bin_edges = np.histogram(raw_data[:,1], 50, density=True)
    #axis = plt.add_subplot(1,1,1)
    # plt.set_title("Distribution of Number of Attempts")
    # plt.set_xlabel("Number of Attempts")
    # plt.set_ylabel("Probability of Number of Number Attempts")

    plt.plot(hist)
    PLOT_NAME = "images/plot.png"
    plt.savefig(PLOT_NAME)
    plot.close()
    print()
    print("final results: total number of knots was {}".format(total_knots))
    return render_template("index.html", plot=PLOT_NAME)


@app.route("/")
@app.route("/index")
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template("index.html")

# @app.after_request
# def add_header(response):
#     response.cache_control.max_age = 300
#     return response
