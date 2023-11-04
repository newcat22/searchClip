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
engine.add_images_by_directory_path("images")
len(engine)

simimarity, paths = engine.search_image_by_text("a china girl", 1)
print(simimarity)
print(paths)


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
        return JsonResponse({'message': 'Image uploaded successfully'})
    return JsonResponse({'message': 'Invalid request'}, status=400)


# 展示图库
def image_database(request):
    image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    if not os.path.exists(image_dir):
        return JsonResponse({'images': []})

    images = []
    for image_name in os.listdir(image_dir):
        image_url = os.path.join(settings.MEDIA_URL, 'images', image_name)
        pic = Pic(name=image_name, url=image_url)
        images.append(pic.to_dict())
    pic1 = Pic(name="Moon.jpg", url="https://s2.loli.net/2023/11/04/Y7nHOuRdrG5Ievh.jpg")
    images.append(pic1.to_dict())
    return JsonResponse({'images': images})


@require_GET
def search_images(request):
    query = unquote(request.GET.get('query', ''))
    simimarity, paths = engine.search_image_by_text(query, 2, return_type="path")
    image_dir = os.path.join(settings.MEDIA_ROOT, 'images')

    if not os.path.exists(image_dir):
        return JsonResponse({'images': []})

    images = []
    # for image_name in os.listdir(image_dir):
    #     image_url = settings.MEDIA_URL + 'images/' + image_name
    #     pic = Pic(name=image_name, url=image_url)
    #     images.append(pic.to_dict())
    for image_name in paths:
        #image_url = settings.MEDIA_URL + 'images/' + image_name
        pic = Pic(name=image_name, url=image_name)
        images.append(pic.to_dict())
    return JsonResponse({'images': images})

# 删除图片
@require_GET
def delete(request):
    query = unquote(request.GET.get('query', ''))
    simimarity, paths = engine.search_image_by_text(query, 2, return_type="path")
    image_dir = os.path.join(settings.MEDIA_ROOT, 'images')

    if not os.path.exists(image_dir):
        return JsonResponse({'images': []})

    images = []
    # for image_name in os.listdir(image_dir):
    #     image_url = settings.MEDIA_URL + 'images/' + image_name
    #     pic = Pic(name=image_name, url=image_url)
    #     images.append(pic.to_dict())
    for image_name in paths:
        #image_url = settings.MEDIA_URL + 'images/' + image_name
        pic = Pic(name=image_name, url=image_name)
        images.append(pic.to_dict())
    return JsonResponse({'images': images})
