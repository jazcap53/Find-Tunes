from flask import Flask, render_template
from markupsafe import escape


app = Flask(__name__)

@app.route('/')
def find_a_tune(tune=None):
    return render_template('find_a_tune.html')
