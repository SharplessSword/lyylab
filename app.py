import json

from flask import Flask, render_template, request, redirect, url_for
from outfile_extractor import get_reaction
from curve_fit import get_curve_value
from datetime import timedelta
app = Flask(__name__)
# app.config['DEBUG'] = True
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    content = uploaded_file.stream.read().decode('utf-8')
    return render_template('show_file.html', reaction_list=get_reaction(content))


@app.route('/update', methods=['POST'])
def update_curve_fit():
    data = json.loads(request.form.get('data'))
    xdata, ydata = data['xdata'], data['ydata']
    xdata, fit_ydata, a, n, e = get_curve_value(xdata, ydata)

    return {'fit_ydata': fit_ydata, 'a': a, 'n': n, 'e':e}

