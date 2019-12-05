#美拍视频采集2
 
# -*- coding: UTF-8 -*-
import requests
import re,time,os,json
from fake_useragent import UserAgent
import base64
from contextlib import closing
 
 
#存储路径
os.makedirs(f'meipai/',exist_ok=True)
 
 
# 解密美拍视频真实地址
def decode(encoded_string):
    def getHex(param1):
        return {
            'str': param1[4:],
            'hex': ''.join(list(param1[:4])[::-1]),
        }
 
    def getDec(param1):
        loc2 = str(int(param1, 16))
        return {
            'pre': list(loc2[:2]),
            'tail': list(loc2[2:]),
        }
 
    def substr(param1, param2):
        loc3 = param1[0: int(param2[0])]
        loc4 = param1[int(param2[0]): int(param2[0]) + int(param2[1])]
        return loc3 + param1[int(param2[0]):].replace(loc4, "")
 
    def getPos(param1, param2):
        param2[0] = len(param1) - int(param2[0]) - int(param2[1])
        return param2
 
    dict2 = getHex(encoded_string)
    dict3 = getDec(dict2['hex'])
    str4 = substr(dict2['str'], dict3['pre'])
    return base64.b64decode(substr(str4, getPos(str4, dict3['tail'])))
 
 
#随机生成协议头
def ua():
    ua=UserAgent()
    headers={
        'Cookie': 'MUSID=0su478f5e30e4u8jlf9gqquhn5; MP_WEB_GID=748151043219051; sid=0su478f5e30e4u8jlf9gqquhn5; UM_distinctid=16ea084234822-0be7691d606889-43450521-1fa400-16ea0842349133; virtual_device_id=8818a5d35ed03e6b6b4fd638a6f765ae; pvid=TVqin0MOgIjpLnJZKxhiL%2FwcrYA2K7Ke; CNZZDATA1256786412=937407365-1574650874-https%253A%252F%252Fwww.baidu.com%252F%7C1574831840',
        'Host': 'www.meipai.com',
        'Referer': 'https://www.meipai.com/square/13',
        'User-Agent': ua.random,
        #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    return headers
 
#访问网页
def get_req(url):
    response = requests.get(url, headers=ua())
    if response.status_code==200:
        response=response.content.decode('utf-8')
        time.sleep(2)
    else:
        response =None
    return response
 
 
def get_video(response):
    reqs=json.loads(response)
    reqs=reqs['medias']
    for req in reqs:
        videoname=req['caption']
        if videoname:
            video_name=videoname
        else:
            video_name =req['weibo_share_caption']
        video_name = video_name.replace(' ', '')
        video_name = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", video_name)  # 剔除不合法字符
        print(video_name)
        video_url=req['video']
        print(video_url)
        try:
            videourl = decode(video_url).decode('utf8')  # 解密视频地址
            print(videourl)
            try:
                down(video_name, videourl)
                #server(video_name, videourl)
            except Exception as e:
                print(f'视频下载出错，错误代码：{e}')
                with open(r'meipai/spider.txt', 'a+', encoding='utf-8') as f:
                    f.write(f'视频下载出错，错误代码：{e}---采集{videourl}|{video_name}内容失败\n')
                pass
        except Exception as e:
            print(f'视频地址解密出错，错误代码：{e}')
            with open(r'meipai/spider.txt', 'a+', encoding='utf-8') as f:
                f.write(f'视频解密出错，错误代码：{e}---采集{video_url}|{video_name}内容失败\n')
            pass
 
#下载视频
def down(h1,url):
    print("准备下载！")
    file_path = f"meipai/{h1}.mp4"
    r = requests.get(url)
    print("开始下载！")
    with open(file_path, "wb") as file:
        file.write(r.content)
        print("下载完成！")
    time.sleep(2)
 
 
# 存储视频，附下载进度显示
def server(h1,videourl):
    print("准备下载！")
    file_path=f'meipai/{h1}.mp4'
    with closing(requests.get(videourl,headers=ua(),stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, file_path), end=" ")
            print("\n>>> 获取视频成功了！")
    time.sleep(2)
 
 
#运行主函数
def main():
    for i in range(1, 100):
        url = f"https://www.meipai.com/squares/new_timeline?page={i}&count=24&tid=13"
        print(url)
        response=get_req(url)
        if response:
            try:
                get_video(response)
            except Exception as e:
                print(f'获取视频出错了，错误代码：{e}')
                pass
 
 
 
 
if __name__ == '__main__':
    main()