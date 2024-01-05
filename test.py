from image_retriever.engine import Engine
import torch
from PIL import Image

#%%
engine=Engine()
engine.load_model("/home/long/model/clip-vit-large-patch14",device="cuda",dtype=torch.float32)
# engine.add_images_by_directory_path("images")

i = len(engine)
print(i)

#simimarity,paths=engine.search_image_by_text("a bike",1,return_type="path")

#print(simimarity)
#print(paths)

import signal
import sys

def signal_handler(signal, frame):
    print("您按下了 Ctrl+C！")
    # 在这里调用您想要执行的函数
    do_cleanup()
    sys.exit(0)

def do_cleanup():
    print("执行清理操作...")

if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)

    # 启动 Django 开发服务器
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)