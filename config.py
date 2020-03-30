import os
# noinspection PyUnresolvedReferences
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'parking-123-secret-key')
    CAMS_IMAGE_FOLDER = 'cam_img'
