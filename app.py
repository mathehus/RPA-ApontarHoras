from asyncio.windows_events import NULL
from flask import Flask,jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 

@app.route('/webhooks/<mode>/<challenge>/<verify_token>', methods=['GET'])
def webhooks(mode,challenge,verify_token):

    if(verify_token == "meatyhamhock"): 
        return challenge
    else:    
       return NULL

# rodar a api
app.run(debug=True, port=8080)