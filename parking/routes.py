# -*- coding: utf-8 -*-
import os
import time

from flask import render_template, g
from flask import current_app as app
from parking.camera.manager import CameraManager
from flask import send_from_directory
from parking.helpers import make_hash_image_dir, get_cam_imgs_url


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    print(app.static_folder)
    print(app.static_url_path)
    manager = CameraManager(os.path.join(app.root_path, 'static', 'img', app.config['CAMS_IMAGE_FOLDER']),
                            os.path.join(app.instance_path, 'runtime'))
    imgs = manager.get_all_cam_screen_url()
    return render_template('index.html', imgs=imgs)


@app.route('/detail', methods=['GET'])
def detail():
    image_path, image_url = make_hash_image_dir('detail')
    manager = CameraManager(image_path, os.path.join(app.instance_path, 'runtime'))
    imgs = manager.load_all_cam_images(600)
    images_url = get_cam_imgs_url(image_url, imgs)
    return render_template('index.html', imgs=images_url)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
