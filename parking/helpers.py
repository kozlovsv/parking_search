import os
from datetime import datetime
from flask import current_app as app

import cv2


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def make_hash_image_dir(sub_folder):
    cams_image_folder = app.config['CAMS_IMAGE_FOLDER']
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    path = os.path.join(app.static_folder, cams_image_folder, sub_folder, ts)
    os.makedirs(path)
    url = f"{app.static_url_path}/{cams_image_folder}/{sub_folder}/{ts}/"
    return path, url


def get_cam_imgs_url(url, imgs):
    imgs_url = []
    for img in imgs:
        imgs_url.append({'url': url + os.path.basename(img['fname']), 'title': img['title']})
    return imgs_url
