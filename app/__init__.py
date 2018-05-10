import json

import flask
from flask import Flask, json, request, redirect, url_for, render_template
import os
import numpy as np
from werkzeug.utils import secure_filename
from flask_cors import CORS
import domain.Workout

app = Flask('app', static_url_path='', static_folder='../site', template_folder='../templates')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = '../site/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['fit', 'csv'])


class NumpyEncoder(json.JSONEncoder):                       
    def default(self, obj):                                 
        if isinstance(obj, np.int64):                       
            return int(obj)                                 
        return json.JSONEncoder.default(self, obj)          


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def root():
    return app.send_static_file('index-nvd3.html')


@app.route('/upload')
def upload_file():
    return app.send_static_file('html/file.html')


@app.route('/view/<file_name>')
def view(file_name):
    return render_template('index-nvd3.html', json_url='files/{}.json'.format(file_name))


@app.route('/uploader', methods=['POST'])
def do_upload():
    if flask.request.method == 'POST':
        my_files = request.files.getlist("file")
        description = request.form['test_desc']

        print(my_files)
        print(description)
        
        # check if the post request has the file part
        if len(my_files) == 0:
            return redirect(request.url)

        file_names = []
        file_labels = []
        # if user does not select file, browser also
        # submit a empty part without filename
        for file in my_files:
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_names.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_labels.append(filename)

        files = domain.Workout.DateTimeSession(description)
        i = 0
        for file_path in file_names:
            files.add_file(file_path, file_labels[i])
            i+=1
            
        with open(UPLOAD_FOLDER+'/{}.json'.format(secure_filename(description)), 'w') as ofile:
            ofile.write(json.dumps(files.get_output(), cls=NumpyEncoder))
            return render_template('index-nvd3.html', json_url='files/{}.json'.format(secure_filename(description)))

    return root()






