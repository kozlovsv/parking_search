import os
import requests
import m3u8
import datetime
import cv2


class UfanetCameraLoader:

    def __init__(self, tmp_path, need_cams, user_name, password):
        self.tmp_path = tmp_path
        self.need_cams = need_cams
        self.user_name = user_name
        self.password = password
        self._cams = None
        os.makedirs(self.tmp_path, exist_ok=True)

    @property
    def cams(self):
        if self._cams is None:
            r = requests.post('https://ucams.ufanet.ru/api/internal/login/',
                              json={'username': self.user_name, 'password': self.password}, allow_redirects=False)
            r = requests.post(
                'http://ucams.ufanet.ru/api/v0/cameras/my/',
                json={'order_by': 'addr_asc',
                      'fields': ['number', 'address', 'title', 'tariff', 'inactivity_period', 'permission',
                                 'is_embed', 'token_l', 'server', 'is_fav'], 'page': 1, 'page_size': 60},
                cookies=r.cookies
            )
            if r.status_code == 401:
                raise Exception("Неверный логин пароль!")
            elif r.status_code != 200:
                raise Exception(r.text)
            json_cams = r.json()
            cams = dict()
            for cam in json_cams['results']:
                if cam['number'] not in self.need_cams:
                    continue
                cams[cam['number']] = {
                    'domain': cam['server']['domain'],
                    'number': cam['number'],
                    'token': cam['token_l'],
                    'title': cam['title'],
                }
            self._cams = cams
        return self._cams

    def download_cam_video(self, cam_name):
        cam = self.cams[cam_name]
        host = f"http://{cam['domain']}/{cam_name}/tracks-v1/"
        r = requests.get(f"{host}mono.m3u8?token={cam['token']}")
        m3u8_text = r.text
        m3u8_obj = m3u8.loads(m3u8_text)
        ts_url = host + m3u8_obj.segments[-1].uri
        r = requests.get(ts_url, allow_redirects=True)
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        ts_fname = os.path.join(self.tmp_path, cam_name + '_' + ts + '.ts')
        open(ts_fname, 'wb').write(r.content)
        return ts_fname

    def download_preview_cam_video(self, cam_name):
        cam = self.cams[cam_name]
        preview_url = f"http://{cam['domain']}/{cam_name}/preview.mp4?token={cam['token']}"
        r = requests.get(preview_url, allow_redirects=True)
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        ts_fname = os.path.join(self.tmp_path, cam_name + '_' + ts + '.mp4')
        open(ts_fname, 'wb').write(r.content)
        del r
        return ts_fname

    def get_preview_cam_image(self, cam_name):
        preview_fname = self.download_preview_cam_video(cam_name)
        try:
            vidcap = cv2.VideoCapture(preview_fname)
            success, image = vidcap.read()
            vidcap.release()
            if not success:
                raise Exception("Ошибка при получении картинки с камеры. Невозможно прочитать видео поток.")
        finally:
            os.remove(preview_fname)
        return image

    def get_cam_image(self, cam_name):
        ts_fname = self.download_cam_video(cam_name)
        try:
            vidcap = cv2.VideoCapture(ts_fname)
            success, image = vidcap.read()
            vidcap.release()
            if not success:
                raise Exception("Ошибка при получении картинки с камеры. Невозможно прочитать видео поток.")
        finally:
            os.remove(ts_fname)
        return image
