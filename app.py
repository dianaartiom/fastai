from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os, random
import scipy.misc
import numpy as np

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config["UPLOAD_FOLDER"] = "static/upload/"

updir = app.config["UPLOAD_FOLDER"]

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/')
def index():
    return render_template('index.html')

def generate_random_name():
    int_name = str(random.randint(1, 10000))
    print(int_name)
    filename = int_name + ".png"
    dummy_array = np.ones([50, 50])
    scipy.misc.toimage(dummy_array).save('static/upload/' + filename)
    return filename

def delete_file(filename):
    os.remove(filename)

@app.route('/uploadajax', methods=['POST', 'GET'])
def load_image():
    filename = generate_random_name()
    file_path = '/'.join(['upload', filename])
    file_size = os.path.getsize(os.path.join(updir, filename))
    
    return jsonify(name=filename, path=file_path, size=file_size)


# @app.route('/uploadajax', methods=['POST', 'GET'])
# def upldfile():
#     if request.method == 'POST':
#         files = request.files['file']
#         print(files)
#         if files and allowed_file(files.filename):
#             filename = secure_filename(files.filename)
#             app.logger.info('FileName: ' + filename)
#             print('FileName: ' + filename)
#             updir = os.path.join(basedir, 'upload/')
#             files.save(os.path.join(updir, filename))
#             file_size = os.path.getsize(os.path.join(updir, filename))
#             file_path = '/'.join(['upload', filename])
#             return jsonify(name=filename, path=file_path, size=file_size)

if __name__ == '__main__':
    app.run(debug=True)
