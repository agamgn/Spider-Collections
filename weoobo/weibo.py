import requests
from bs4 import BeautifulSoup
 
headers = {
    "cookie": "YOUR_COOKIE",       # 请传入cookie
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}
 
 
class Weibo(object):
    def __init__(self):
        self.uid = "Weibo_UID"      # 请设置微博用户的UID
        self.url = "https://weibo.cn/u/" + self.uid
 
    def mysql(self):
        pass
 
    @staticmethod
    def send_request(url):
        r = requests.get(url, headers=headers).content.decode("utf-8")
        return r
 
    def weibo_infos(self, html):
        parser = self.send_request(html)
        soup = BeautifulSoup(parser, "html.parser")
        weibo_name = soup.find("title").text.replace("的微博", "")
        pages = int(soup.find("div", class_="pa", id="pagelist").input["value"])
        weibo_url_list = ["https://weibo.cn/u/" + self.uid + "?page=%d" % (i+1) for i in range(pages)]
        return weibo_name, pages, weibo_url_list
 
    def weibo_parser(self, url):
        import re
        pic_id = list()
        get_info = BeautifulSoup(self.send_request(url), "html.parser")
        group_pic = [i["href"] for i in get_info.find_all("a", text=re.compile('组图'))]
        img_id = [i["src"].split("/")[-1] for i in get_info.find_all("img", alt="图片")]
        pic_id += img_id
        for i in group_pic:
            s_soup = BeautifulSoup(self.send_request(i), "html.parser")
            pic_list = [i["src"].split("/")[-1] for i in s_soup.find_all(alt="图片加载中...")]
            pic_id += [j for j in pic_list if j not in pic_id]
        return pic_id
 
    @staticmethod
    def img_download(name, pic_id, url):
        import os
        path = r"C:\Users\Administrator\%s" % name + "\\"
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            if os.path.exists(path + pic_id):
                print("%s：该张图片已下载！" % pic_id)
            else:
                byte = requests.get(url, headers).content
                with open(path + pic_id, "wb") as f:
                    f.write(byte)
        except Exception as e:
            print(e, "\n下载出错！")
 
    def main(self):
        total_pics = 0
        weibo_name, pages, weibo_url_list = self.weibo_infos(self.url)
        print("正在爬取 【 %s 】 的微博" % weibo_name)
        print("总共检测到 %d 页" % pages)
        for page, weibo_url in enumerate(weibo_url_list):
            print("正在爬取第 %d 页微博" % (page+1))
            pic_url = ["http://wx1.sinaimg.cn/large/" + pic_id for pic_id in self.weibo_parser(weibo_url)]
            print("抓取第 %d 页微博完成，正在下载图片..." % (page+1))
            for num, pic in enumerate(pic_url):
                print("正在保存：%s" % pic)
                self.img_download(weibo_name, pic.split("/")[-1], pic)
                total_pics += 1
                print(">>>第 %d 张图片<<<\n第 %d 页微博：第 %d 张图片保存成功！" % (total_pics, page+1, num+1))
        print("爬取完成！\n总共下载了 %d 张图片！" % total_pics)
 
 
if __name__ == '__main__':
    Weibo().main()