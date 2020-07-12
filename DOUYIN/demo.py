import requests
import tkinter
import re
import urllib.request
from os import makedirs
from os.path import exists
import time
 
def mkdir(path):
    if not exists(path):
        makedirs(path)
 
 
def douyin(url):
    mkdir('视频\\')
    html = requests.get(url, timeout=10).url
    ht = re.findall(r'\d+', html)
    url1 = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + ht[0]
    html = requests.get(url1)
    ht = html.json()
    name = ht['item_list'][0]['author']['nickname']
    post = ht['item_list'][0]['video']['play_addr']['uri']
    url2 = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + post + "&line=0"
    html = requests.get(url2, headers=header, timeout=10).url
    urllib.request.urlretrieve(html, "视频\\" + name + ".mp4")
    print("下载完毕")
    print('程序即将退出')
    time.sleep(3)
 
 
header = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36"
}
url2 = input("请输入链接：")
url1 = re.findall(r'https://v.douyin.com/+[a-zA-Z0-9]+', url2)
while True:
    url1 = re.findall(r'https://v.douyin.com/+[a-zA-Z0-9]+', url2)
    if len(url1) > 0:
        print("解析中")
        url1 = str(url1[0]) + "/"
        douyin(url1)
        break
    else:
        url2 = input("请输入正确地址：")