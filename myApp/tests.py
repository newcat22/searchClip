from django.test import TestCase

# Create your tests here.


import requests
import json
import os
from django.core.files.storage import default_storage


def upload(path):
    headers = {'Authorization': '6kUT2VoDAqiLnUu6gSuN7VdnfuwwOUvY'}
    files = {'smfile': open(path, 'rb')}
    url = 'https://sm.ms/api/v2/upload'
    res = requests.post(url, files=files, headers=headers).json()
    print(json.dumps(res))


# /home/long/anaconda3/envs/clipSearch/bin/python3 /home/long/code/searchClip/myApp/tests.py
# {"success": true, "code": "success", "message": "Upload success.", "data": {"file_id": 0, "width": 968, "height": 472, "filename": "snake.png", "storename": "yqbonYitKsGFQjd.png", "size": 527014, "path": "/2023/11/04/yqbonYitKsGFQjd.png", "hash": "3rgCZyGl8PANVMbYLf4aw9EKFB", "url": "https://s2.loli.net/2023/11/04/yqbonYitKsGFQjd.png", "delete": "https://sm.ms/delete/3rgCZyGl8PANVMbYLf4aw9EKFB", "page": "https://sm.ms/image/yqbonYitKsGFQjd"}, "RequestId": "DF42004A-0D7C-40F8-A782-EEE3505E2DFC"}
# 没有图的时候数据上传格式
# Process finished with exit code 0
if __name__ == "__main__":
    file_path = os.path.join('images', "code.jpg")
    file_path = "/home/long/code/searchClip/images/monu.png"

    upload(file_path)


