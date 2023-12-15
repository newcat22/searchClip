from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# 查询图片
from image_retriever.engine import Engine
import torch
from PIL import Image
from django.views.decorators.http import require_GET
from urllib.parse import unquote

# %%
engine = Engine()
engine.load_model("/home/long/model/clip-vit-large-patch14", device="cuda", dtype=torch.float32)
# engine.add_images_by_directory_path("images")  预加载图片
# len(engine)
# 
# simimarity, paths = engine.search_image_by_text("a china girl", 1)
# print(simimarity)
# print(paths)

import requests
import json
import os

# 全局字典来存储图片的URL和删除链接
uploaded_images = {}
headers = {'Authorization': '6kUT2VoDAqiLnUu6gSuN7VdnfuwwOUvY'}


# 首页
def index(request):
    return render(request, 'myApp/index.html')


class Student:
    def __init__(self, name, url):
        self.name = name
        self.url = url  # 图片的URL


class Pic:
    def __init__(self, name, url):
        self.name = name
        self.url = url  # 图片的URL

    def to_dict(self):
        return {'name': self.name, 'url': self.url}


# 测试案例
def students(request):
    # 创建一些学生实例
    student1 = Student(name='学生一', url='https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg')
    student2 = Student(name='学生二', url='https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg')

    # 将学生实例放入一个列表中
    studentsList = [student1, student2]
    return render(request, 'myApp/test.html', {'students': studentsList})


import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


def upload(path):
    """
    上传图片到图床
    :param path:
    :return:
    """
    # 替换为你的API密钥
    files = {'smfile': open(path, 'rb')}
    url = 'https://sm.ms/api/v2/upload'
    response = requests.post(url, files=files, headers=headers).json()
    print(json.dumps(response))

    # 检查上传是否成功并保存URL和删除链接
    if response.get("success"):
        image_url = response['data']['url']
        delete_url = response['data']['delete']
        uploaded_images[os.path.basename(path)] = {'url': image_url, 'delete': delete_url}
        print("Uploaded and URL saved:", image_url)
    else:
        print("Upload failed")


def delete_image(image_name):
    """
    删除图床图片
    :param image_name:
    :return:
    """
    image_info = uploaded_images.get(image_name)
    if not image_info:
        print("Image not found")
        return

    # 发送删除请求
    response = requests.get(image_info['delete'])
    if response.status_code == 200:
        del uploaded_images[image_name]
        print("Image deleted successfully")
    else:
        print("Failed to delete image")


def get_uploaded_images():
    """
    获取图库图像（待做持久化）
    :return:
    """
    return uploaded_images


# 上传图片
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        #file_path = os.path.join(settings.BASE_DIR, 'images', image.name)
        file_path = os.path.join('images', image.name)
        print(file_path)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        engine.add_image(image_path=file_path)
        upload(file_path) #上传图片到图床
        return JsonResponse({'message': 'Image uploaded successfully'})
    return JsonResponse({'message': 'Invalid request'}, status=400)


# 展示图库
def image_database(request):
    # image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    # if not os.path.exists(image_dir):
    #     return JsonResponse({'images': []})
    images = []
    # 遍历uploaded_images字典
    for filename, info in uploaded_images.items():
        if 'url' in info:  # 确保每个项都有URL
            pic = Pic(name=filename, url=info['url'])  # 创建Pic对象
            images.append(pic.to_dict())  # 将Pic对象添加到列表中


    # for image_name in os.listdir(image_dir):
    #     image_url = os.path.join(settings.MEDIA_URL, 'images', image_name)
    #     pic = Pic(name=image_name, url=image_url)
    #     images.append(pic.to_dict())
    # pic1 = Pic(name="Moon.jpg", url="https://s2.loli.net/2023/11/04/Y7nHOuRdrG5Ievh.jpg")
    # images.append(pic1.to_dict())
    return JsonResponse({'images': images})


@require_GET
def search_images(request):
    query = unquote(request.GET.get('query', ''))
    print("query",query)
    paths = []
    try:
        simimarity, paths = engine.search_image_by_text(query, 1, return_type="path")
    except Exception as e:
        # 当发生任何异常时执行的代码
        print("An error occurred:", e)

    images = []
    uploaded_images = get_uploaded_images()  # 获取上传图片集合

    for path in paths:
        image_name = os.path.basename(path) #获取图片名
        uploaded_image = uploaded_images.get(image_name)
        if uploaded_image:
            url = uploaded_image.get('url', '')
            pic = Pic(name=image_name, url=url)
            images.append(pic.to_dict())
    return JsonResponse({'images': images})

# 删除图片
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        image_name = request.POST.get('image_name', '')
        print(image_name)
        image_path = os.path.join('images', image_name)
        print(image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
            engine.remove_image_feature(image_path)
            delete_image(image_name)
            return JsonResponse({'message': 'Image deleted successfully'})
        else:
            return JsonResponse({'message': 'Image not found'}, status=404)
    return JsonResponse({'message': 'Invalid request'}, status=400)
