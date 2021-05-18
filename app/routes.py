from .generate_chain import generate_closed_chain, chain_to_JSON
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
        N = 10
        payload = chain_to_JSON(generate_closed_chain(N)[0])
        return jsonify(payload) # serialize and use JSON headers


@app.route('/')
@app.route('/index')
def index():
    # look inside 'templates' and serve 'index.html'
    return render_template('index.html')