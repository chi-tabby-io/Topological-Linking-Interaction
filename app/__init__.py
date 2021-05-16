from flask import Flask

app = Flask(__name__)

from app import routes

# from .driver import driver
# from .generate_binary_list import generate_binary_list
# from .generate_chain import generate_chain