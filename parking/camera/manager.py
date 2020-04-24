import os
import cv2

from parking.camera.loaders.ufanet import UfanetCameraLoader
from parking.helpers import image_resize

need_cams = {
    '1515376745BBP372': 'Подъезд 4. Мусорка',
    '1515376745BBP388': 'Подъезд 4. Торец дома',
    '1515376745BBP399': 'Подъезд 3. Подъезд 4',
    '1515376745BBP409': 'Подъезд 3. Крыльцо',
    '1515376745BBP444': 'Подъезд 2. Крыльцо',
    '1515376745BBP460': 'Подъезд 2. Подъезд 1',
    '1515376745BBP493': 'Подъезд 1. Торец. Слева',
    '1515376745BBP510': 'Подъезд 1. Торец. Справа',
    '1520840341PMF876': 'Въезд во двор',
}


class CameraManager:

    def __init__(self, image_path, tmp_path):
        user_name = os.getenv('UFANET_USER_NAME')
        password = os.getenv('UFANET_USER_PASSWORD')

        self.image_path = image_path
        self.loader = UfanetCameraLoader(tmp_path, need_cams, user_name, password)
        os.makedirs(self.image_path, exist_ok=True)

    def get_image_file_name(self, cam_name):
        return os.path.join(self.image_path, cam_name + '.png')

    def load_cam_image(self, cam_name, width=None):
        image = self.loader.get_preview_cam_image(cam_name)
        if width is not None:
            image = image_resize(image, width=width)
        fname = self.get_image_file_name(cam_name)
        cv2.imwrite(fname, image)
        return fname

    def load_all_cam_images(self, width=None):
        imgs = []
        for cam_name in need_cams.keys():
            imgs.append({'cam_name': cam_name, 'title': need_cams[cam_name],
                         'fname': self.load_cam_image(cam_name, width=width)})
        return imgs

    def load_cam_screen(self, cam_name):
        fname = self.get_image_file_name(cam_name)
        self.loader.download_screen_cam_image(cam_name, fname)
        return fname

    def load_all_cam_screen(self):
        fnames = []
        for cam_name in need_cams.keys():
            fnames.append(self.load_cam_screen(cam_name))
        return fnames

    def get_all_cam_screen_url(self):
        fnames = []
        for cam_name in need_cams.keys():
            fnames.append({'url': self.loader.get_screen_cam_image_url(cam_name), 'title': need_cams[cam_name]})
        return fnames
