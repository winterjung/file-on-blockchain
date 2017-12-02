import os
import hashlib
import contract
from flask import (Flask, request, redirect, url_for, send_from_directory,
                   render_template)
from werkzeug import secure_filename
from datetime import datetime

UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
INS = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            owner = request.form["owner"]
            filehash = sha256_checksum(path)
            filesize = os.path.getsize(path)
            upload_on_blockchain(filehash=filehash,
                                 filename=filename,
                                 filesize=filesize,
                                 owner=owner)

            return redirect(url_for('uploaded_file',
                                    filename=filename,
                                    filehash=filehash))
    return render_template("upload.html")


@app.route('/uploader')
def uploaded_file():
    filename = request.args['filename']
    filehash = request.args['filehash']
    return render_template("uploaded.html",
                           filename=filename,
                           filehash=filehash)


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/info/<filehash>')
def get_file_info(filehash):
    file_info = contract.get_file_info(INS, filehash)
    info = {
        "file_name": file_info[0],
        "upload_date": datetime.fromtimestamp(file_info[1]),
        "file_size": file_info[2],
    }
    return render_template("info.html",
                           filehash=filehash,
                           info=info)


@app.route('/check', methods=['POST'])
def check_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        filehash = sha256_checksum(path)
        is_exist = contract.check_file_exist(INS, filehash)
        return render_template('check.html',
                               is_exist=is_exist,
                               filehash=filehash,
                               filename=filename)


# TODO: Use celery
def upload_on_blockchain(**kwargs):
    contract.upload(INS, **kwargs)


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


if __name__ == "__main__":
    INS = contract.deploy("storage.sol", "FileHashStorage")
    app.run(debug=False)
