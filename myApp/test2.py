import requests
import json
import os

# 全局字典来存储图片的URL和删除链接
uploaded_images = {}
headers = {'Authorization': '6kUT2VoDAqiLnUu6gSuN7VdnfuwwOUvY'}


def upload(path):
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
    return uploaded_images


def getHistory():
    url = 'https://sm.ms/api/v2/upload_history'
    history_response = requests.get(url, headers=headers, timeout=5).json()
    if history_response.get('success'):
        uploaded_images.clear()
        for item in history_response['data']:
            filename = item['filename']
            url = item['url']
            delete_url = item['delete']
            uploaded_images[filename] = {'url': url, 'delete': delete_url}  # 更新或添加图片信息
        print("Uploaded images updated successfully.")
    else:
        print("Failed to retrieve image history.")
    return history_response


# 使用示例
if __name__ == "__main__":
    test_image_path = "/home/long/code/searchClip/images/dog.png"  # 替换为实际图片路径
    upload(test_image_path)

    # 获取已上传图片列表
    print("Uploaded Images:", get_uploaded_images())

    # 删除图片
    test_image_name = os.path.basename(test_image_path)  # 获取文件名
    delete_image(test_image_name)
    print("Uploaded Images after deletion:", get_uploaded_images())

    history = getHistory()
    print("history", history)

# {'success': True, 'code': 'success', 'message': 'Get list success.', 'data': [
#     {'width': 2194, 'height': 1024, 'filename': '000000079.jpg', 'storename': 'x1Fc5MnrQjUq4Dz.jpg', 'size': 619004,
#      'path': '/2023/11/04/x1Fc5MnrQjUq4Dz.jpg', 'hash': 'cCF9rwLO6nAbDEGtmVJSeiPqKv',
#      'created_at': '2023-11-04 15:52:36', 'url': 'https://s2.loli.net/2023/11/04/x1Fc5MnrQjUq4Dz.jpg',
#      'delete': 'https://sm.ms/delete/cCF9rwLO6nAbDEGtmVJSeiPqKv', 'page': 'https://sm.ms/image/x1Fc5MnrQjUq4Dz'},
#     {'width': 800, 'height': 600, 'filename': 'Moon.jpg', 'storename': 'Y7nHOuRdrG5Ievh.jpg', 'size': 72227,
#      'path': '/2023/11/04/Y7nHOuRdrG5Ievh.jpg', 'hash': 'C9pcQL4jfKmVroSwPMs31be2xz',
#      'created_at': '2023-11-04 15:56:03', 'url': 'https://s2.loli.net/2023/11/04/Y7nHOuRdrG5Ievh.jpg',
#      'delete': 'https://sm.ms/delete/C9pcQL4jfKmVroSwPMs31be2xz', 'page': 'https://sm.ms/image/Y7nHOuRdrG5Ievh'},
#     {'width': 968, 'height': 472, 'filename': 'snake.png', 'storename': 'yqbonYitKsGFQjd.png', 'size': 527014,
#      'path': '/2023/11/04/yqbonYitKsGFQjd.png', 'hash': '3rgCZyGl8PANVMbYLf4aw9EKFB',
#      'created_at': '2023-11-04 15:59:57', 'url': 'https://s2.loli.net/2023/11/04/yqbonYitKsGFQjd.png',
#      'delete': 'https://sm.ms/delete/3rgCZyGl8PANVMbYLf4aw9EKFB', 'page': 'https://sm.ms/image/yqbonYitKsGFQjd'},
#     {'width': 982, 'height': 508, 'filename': 'monu.png', 'storename': '19cfWu6k2KF8zV7.png', 'size': 573096,
#      'path': '/2023/12/15/19cfWu6k2KF8zV7.png', 'hash': 'hytjbDVzmQ3owC4E6ZlJN8i2va',
#      'created_at': '2023-12-15 13:29:49', 'url': 'https://s2.loli.net/2023/12/15/19cfWu6k2KF8zV7.png',
#      'delete': 'https://sm.ms/delete/hytjbDVzmQ3owC4E6ZlJN8i2va', 'page': 'https://sm.ms/image/19cfWu6k2KF8zV7'}],
#  'CurrentPage': 1, 'TotalPages': 1, 'PerPage': 100, 'Count': 4, 'RequestId': 'C881020C-20F9-4C87-83D4-1F7ED3951CBF'}
