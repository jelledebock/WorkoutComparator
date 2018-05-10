import urllib.parse
import json

import flask
from flask import Flask, json, request, redirect, url_for, render_template, jsonify
import os
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
from flask_cors import CORS
import domain.Workout
import domain.File

app = Flask(__name__, static_url_path='', static_folder='site', template_folder='templates')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = './site/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['fit', 'csv'])


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
    return render_template('index-nvd3.html', json_url='files/json/{}.json'.format(file_name))


@app.route('/values')
def values():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    metric = urllib.parse.unquote(request.args.get('metric'))
    json_url = urllib.parse.unquote(request.args.get('json_url'))
    df_folder = os.path.join(SITE_ROOT, 'site/files', 'dfs', json_url.split('.')[0].split('/')[-1])
    json_path = os.path.join(SITE_ROOT, 'site', json_url)

    file_name = urllib.parse.unquote(request.args.get('file_label'))
    csv_df_file = os.path.join(df_folder, file_name)
    csv_df_file += '.csv'

    with open(json_path) as ifile:
        json_obj = json.loads(ifile.read())
        sort_by = json_obj["sort_by"]
        print("Getting {} values of {} in {}".format(metric, json_url, file_name))

    return flask.jsonify(domain.File.get_x_y_values(pd.read_csv(csv_df_file), sort_by, metric))


@app.route('/edit')
def edit():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    file_name = urllib.parse.unquote(request.args.get('file_name'))
    file_subcomponent = urllib.parse.unquote(request.args.get('file_subcomponent'))+'.csv'
    offset = urllib.parse.unquote(request.args.get('offset'))
    folder = file_name.split('/')[-1].split('.')[-2]

    df_file = os.path.join(SITE_ROOT, 'site', 'files', 'dfs', folder, file_subcomponent)
    domain.File.modify_with_offset(df_file, offset)

    return json.dumps({'success':True})


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

        dir_to_upload_dfs = os.path.join(UPLOAD_FOLDER, 'dfs', secure_filename(description))
        summary_upload = os.path.join(UPLOAD_FOLDER, 'json', secure_filename(description)+'.json')

        files.get_output(summary_upload, dir_to_upload_dfs)

        return render_template('index-nvd3.html', json_url='files/json/{}.json'.format(secure_filename(description)))

    return root()


if __name__ == '__main__':
    app.run(debug=True, port=5002)






