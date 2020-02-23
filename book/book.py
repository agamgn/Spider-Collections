import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import time

#资料保存的根目录
root = 'F:\\book\\'

#构造浏览器访问头
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
         "Referer":"https://ct.hep.com.cn/"}

#创建一个列表
#存储资料一级下载地址(因为会有两个302跳转)
resource_urls = []
for i in range(25,1151,25):

    # 这些数字是通过分析得来的
    # URL的构造同理(开发者控制台分析)
        resource_url = 'https://ct.hep.com.cn/public/page/wk-listData.html?' + \
        'pageConfig=%257B%2522start%2522%253A' + str(i) + \
        '%252C%2522limit%2522%253A25%252C%2522condition%2522%253A%255B%255D%257D'
        resource_urls.append(resource_url)

#创建两个列表
#分别存储二级下载地址和书名
download_urls = []
book_names = []        

for resource_url in resource_urls:

    #提取页面信息
    r = requests.get(url = resource_url, headers = headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup

    #进一步提取信息
    soup = soup.find_all('div', 'col-lg-2 col-md-2 col-sm-6 col-xs-6 btnDown')
    names = name.find_all('div', 'col-lg-6 col-md-6 col-sm-12 col-xs-12')

    for name in names:
        book_names.append(name.get_text()) 

    #从一级下载界面提取URL
    for elem in soup:
        elem = elem.find('a')
        elem = elem.get('href')

        #转换为我们需要的最终下载URL
        sep = elem.split('/')
        complete_url = 'http://2d.hep.com.cn/api/v1/pan/resources/' + sep[-2] + '/download'
        download_urls.append(complete_url)

#分别下载资料
for i in range(len(book_names)):

    #path为资料完整路径
    path = root + book_names[i] + '.rar'
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        print(book_names[i] + '下载中')
        try:
            #构造随机浏览器访问头
            ua = UserAgent()
            ua = ua.random
            headers = {"User-Agent":ua, "Referer":"https://ct.hep.com.cn/"}
            res = requests.get(url = download_urls[i], headers = headers)
            if (res.status_code == 200):
                with open(path, 'wb') as f:
                    f.write(res.content)
                    f.close()
                    print(book_names[i] + '下载完毕\n')
                    sleep(5)
            else:
                print(book_names[i] + '下载失败')
        except Exception:
            pass             