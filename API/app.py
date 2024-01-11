from flask import Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello world"

@app.route("/home")
def home():
    return "This is Home page"

# import controller.user_controller as user_controller
# import controller.product_controller as product_controller

from controller import *