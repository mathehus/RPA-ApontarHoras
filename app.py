from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 