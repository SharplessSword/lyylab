from flask import Flask, render_template, request, redirect, url_for
from outfile_extractor import get_reaction
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    content = uploaded_file.stream.read().decode('utf-8')
    return render_template('show_file.html', reaction_list=get_reaction(content))