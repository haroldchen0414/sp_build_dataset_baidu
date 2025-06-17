# -*- coding: utf-8 -*-
# author: haroldchen0414

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from imutils import paths
import numpy as np
import requests
import random
import string
import time
import cv2
import os

class BaiduImageDownloader:
    def __init__(self):
        self.chormeOptions = Options()
        #self.chormeOptions.add_argument("--headless")
        #self.chormeOptions.add_argument("--no-sandbox")
        self.chormeOptions.add_argument("--window-size=1920,1080")
        os.makedirs("output", exist_ok=True)

    def collect_url(self, search_key, n=100):
        driver = webdriver.Chrome(service=Service(executable_path=r"D:\software\Python\chromedriver.exe"), options=self.chormeOptions)
        driver.get("https://image.baidu.com")
        searchBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "image-search-input")))
        searchBox.send_keys(search_key)
        searchBox.send_keys(Keys.RETURN)
        

        time.sleep(3)
        imageUrls = set()
        scrollPauseTime = 2

        while len(imageUrls) < n:
            imageElements = driver.find_elements(By.CSS_SELECTOR, "img[data-objurl], img.img_7rRSL")

            for image in imageElements:
                src = image.get_attribute("src")

                if src and src.startswith("http") and src not in imageUrls:
                    imageUrls.add(src)

                    if len(imageUrls) >= n:
                        break
            
            if len(imageUrls) < n:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scrollPauseTime)
        
        with open("baidu_image_urls.txt", "w", encoding="utf-8") as f:
            for url in imageUrls:
                f.write(url + "\n")

        print("已收集{}张图片".format(len(imageUrls)))
        driver.quit()
    
    def download_image(self, url_path):
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
        errorUrls = []
        randomPrefix = "".join(random.choice(string.ascii_lowercase) for _ in range(3))

        with open(url_path, "r", encoding="utf-8") as f:
            urls = f.read().strip().split("\n")
        
        for (i, url) in enumerate(urls):
            try:
                response = requests.get(url, stream=True, headers=headers, timeout=60)
                
                if response.status_code == 200:
                    p = os.path.sep.join(["output", "{}_{}.jpg".format(randomPrefix, str(i))])

                    with open(p, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print("正在下载第{}张图片:{} 剩余{}张...".format(str(i + 1), p, len(urls) - i - 1))

            except Exception as e:
                print("下载失败:{}, 图片地址:{}\n失败原因:{}".format(p, url, e))
                errorUrls.append(url)
    
        if errorUrls:
            with open("error_urls.txt", "w", encoding="utf-8") as f:
                for url in errorUrls:
                    f.write(url + "\n")

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

downloader = BaiduImageDownloader()
downloader.collect_url("猫", n=100)
downloader.download_image("baidu_image_urls.txt")