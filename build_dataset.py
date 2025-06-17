# -*- coding: utf-8 -*-
# author: haroldchen0414

from imutils import paths
import requests
import numpy as np
import random
import string
import time
import cv2
import os

urlPath = "baidu_image_urls.txt"
os.makedirs("output", exist_ok=True)

with open(urlPath, "r") as f:
    urls = f.read().strip().split("\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

randomPrefix = "".join(random.choice(string.ascii_lowercase) for _ in range(3))

for (i, url) in enumerate(urls):
    try:
        p = os.path.sep.join(["output", "{}_{}.jpg".format(randomPrefix, str(i))])
        r = requests.get(url, headers=headers, timeout=60)
        
        with open(p, "wb") as f:
            f.write(r.content)
            print("正在下载{}...".format(p))

        time.sleep(0.2)
        
    except Exception as e:
        print("下载失败:{}, 图片地址:{}\n失败原因:{}".format(p, url, e))

# 检查下载的图片是否异常, 异常则删除
for imagePath in paths.list_images("output"):
    delete = False

    try:
        image = cv2.imdecode(np.fromfile(imagePath, dtype="uint8"), -1)

        if image is None:
            delete = True
    
    except:
        delete = True
    
    if delete:
        print("图片异常, 删除图片{}".format(imagePath))
        os.remove(imagePath)