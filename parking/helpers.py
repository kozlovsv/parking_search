from flask import url_for
from glob import glob
import os
from flask import current_app as app
from parking.camera.manager import need_cams


def get_cam_imgs_url(path, ext='png'):
    fname_all = glob(os.path.join(app.root_path, 'static', path, '*.' + ext))
    fname_all.sort()
    imgs = []
    for fname in fname_all:
        url = url_for('static', filename=path + '/' + os.path.basename(fname))
        cam_name = get_cam_name_from_file_name(fname)
        title = need_cams.get(cam_name, cam_name)
        imgs.append({'url': url, 'title': title})
    return imgs


def get_cam_name_from_file_name(fname):
    return os.path.splitext(os.path.basename(fname))[0]
