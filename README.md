# sp_build_dataset_baidu
用百度图片构建数据集  

方法一：  
打开百度图片，输入想要搜索的图片后，打开开发者工具F12，进入控制台页面，复制baidu.js的内容粘贴，其中grabImageUrls(100)，100替换为想要的图片数量，随后浏览器会自动下载baidu_image_urls.txt  
替换build_dataset.py中的urlPath路径为baidu_image_urls.txt的路径，运行

方法二：
chrome浏览器运行chrome://version/，获取浏览器版本号  
进入页面https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json  
找到对应浏览器版本的chromedriver下载  
将baidu_image_downloader.py中的executable_path换成chromedriver的目录  
运行baidu_image_downloader.py



