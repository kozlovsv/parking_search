import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'parking-123-secret-key'
    CAMS_IMAGE_FOLDER = 'cam_img'
