from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 

@app.route('/webhooks', methods=['GET'])
def webhooks():
    mode = request.args.get('hub.mode')
    challenge = request.args.get('hub.challenge')
    verify_token = request.args.get('hub.verify_token')

    return challenge

@app.route('/webhooks', methods=['POST'])
def webhooksPost():
    _json = request.json
    print(jsonify(_json))
    return "200"

