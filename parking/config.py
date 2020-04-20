import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'parking-123-secret-key')
    CAMS_IMAGE_FOLDER = 'cam_img'
