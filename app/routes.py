from .generate_chain import generate_closed_chain, chain_to_JSON
from .projection import find_reg_project_rotate
from flask import jsonify, request, render_template
from app import app


@app.route('/data_helper', methods=['GET', 'POST'])
def data_helper():
    #POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json()) #parse as JSON
        return 'OK', 200
    
    # GET request
    else:
        # current algorithm takes about 10-30s to generate closed,
        # non-intersecting chain of length 50 (05/16/2021)
        #NOTE: just don't put odd inputs O_O
        #FURTHER NOTE: a knot will NOT form if N <= 23
        N = 24
        saw = generate_closed_chain(N)[0]
        rot_saw = find_reg_project_rotate(saw)
        payload = chain_to_JSON(rot_saw)
        return jsonify(payload) # serialize and use JSON headers


@app.route('/')
@app.route('/index')
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template('index.html')