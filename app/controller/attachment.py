# coding:utf-8
from . import bp
import uuid
import os
from flask import request, jsonify, current_app


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/attachments/upload', methods=['POST'])
def upload():
    names = []
    for file in request.files.values():
        if file and allowed_file(file.filename):
            filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            names.append(filename)
    return jsonify(names), 200
