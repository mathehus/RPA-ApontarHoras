from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 

app.run(host='0.0.0.0', port=4444)