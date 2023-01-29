from flask import Flask, render_template
from outfile_extractor import get_reaction
app = Flask(__name__)

reaction = get_reaction()
@app.route('/')
def hello_world():
    return render_template('hello.html', r=get_reaction())

