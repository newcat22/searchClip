from image_retriever.engine import Engine
import torch
from PIL import Image

#%%
engine=Engine()
engine.load_model("/home/long/model/clip-vit-large-patch14",device="cuda",dtype=torch.float32)
engine.add_images_by_directory_path("images")

len(engine)

simimarity,paths=engine.search_image_by_text("a bike",2,return_type="path")

print(simimarity)
print(paths)