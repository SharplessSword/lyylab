import json

from flask import Flask, render_template, request, redirect, url_for
from outfile_extractor import get_reaction
from curve_fit import get_curve_value
from txt_extractor import txt_extractor
app = Flask(__name__)
# app.config['DEBUG'] = True
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename.endswith('.out'):
        content = uploaded_file.stream.read().decode('utf-8')
        return render_template('show_file.html', reaction_list=get_reaction(content))
    elif uploaded_file.filename.endswith('.txt'):
        # content = uploaded_file.stream.read().decode('utf-8')
        content = uploaded_file.stream.read().decode('utf-8')
        xdata, ydata = txt_extractor(content)
        return render_template('show_txt_file.html', xdata=xdata, ydata=ydata)

@app.route('/update', methods=['POST'])
def update_curve_fit():
    data = json.loads(request.form.get('data'))
    print(data)
    xdata, ydata, select_index = data['xdata'], data['ydata'], data['selected_temperature']
    fit_ydata, a, n, e = get_curve_value(xdata, ydata, select_index)

    return {'ydata': ydata, 'fit_ydata': fit_ydata, 'a': a, 'n': n, 'e': e}


