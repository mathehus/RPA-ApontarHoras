from asyncio.windows_events import NULL
from flask import Flask,jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 

#@app.route('/webhooks/<mode>', methods=['GET'])
#def webhooks(mode):

 #  return mode

# rodar a api
#app.run(debug=True, port=8080)