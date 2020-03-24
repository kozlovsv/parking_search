import os
import cv2
from app.camera.loaders.ufanet import UfanetCameraLoader

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

    def load_cam_image(self, cam_name):
        image = self.loader.get_cam_image(cam_name)
        fname = self.get_image_file_name(cam_name)
        cv2.imwrite(fname, image)
        return fname

    def load_all_cam_images(self):
        for cam_name in need_cams.keys():
            self.load_cam_image(cam_name)
