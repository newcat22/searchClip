from minio import Minio
from minio.error import S3Error

def main():
    # 创建一个 Minio 客户端对象
    client = Minio(
        "192.168.163.128:9000",
        access_key="admin",
        secret_key="xrj12345678",
        secure=False
    )

    bucket_name = "clip"
    object_name = "code.png"
    file_path = "./images/code.png"  # 替换为您的图片路径

    try:
        # 上传图片
        client.fput_object(bucket_name, object_name, file_path)

        # 获取图片的访问 URL  Uploaded Image URL: http://192.168.163.128:9000/clip/code.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=admin%2F20231221%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231221T140954Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=af7a4feb445ac10845fd00b70ae29cb3a42ef4075a21f18b35614f0b2f4d4783
        object_url = client.presigned_get_object(bucket_name, object_name)
        print("Uploaded Image URL:", object_url)
    except S3Error as err:
        print("Error:", err)

    #client.remove_object(bucket_name, object_name) 删除图片，bucket_name填clip，object_name填文件名


if __name__ == "__main__":
    main()
