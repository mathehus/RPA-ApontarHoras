from flask import Flask,request,jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 


@app.route('/webhooks', methods=['POST'])
def webhooksPost():
    _json = request.json

    print(_json)
    return "200"




   

