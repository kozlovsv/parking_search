# -*- coding: utf-8 -*-
import os

from flask import render_template
from app import app
from app.camera.manager import CameraManager
from app.helpers import get_cam_imgs_url
import datetime
from flask import send_from_directory


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    manager = CameraManager(os.path.join(app.root_path, 'static', app.config['CAMS_IMAGE_FOLDER']),
                            os.path.join(app.instance_path, 'runtime'))
    manager.load_all_cam_images()
    imgs = get_cam_imgs_url(app.config['CAMS_IMAGE_FOLDER'])
    salt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    return render_template('index.html', imgs=imgs, salt=salt)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
