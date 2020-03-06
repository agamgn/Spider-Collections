import requests
import json
import os

def UrlAdd():
    URllists = []
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}"
    for i in range(16):
        urls = url.format(i * 20)
        URllists.append(urls)
    print(URllists)
    return URllists

def GetJson(URllists, headers):
    ContentLists = []
    for URllist in URllists:
        r = requests.get(URllist, headers=headers)
        r.encoding = r.apparent_encoding
        results = json.loads(r.text)
        for i in results['subjects']:
            contents = {}
            contents['电影名'] = i['title']
            contents['评分'] = i['rate']
            contents['链接'] = i['url']
            contents['图片地址'] = i['cover']
            ContentLists.append(contents)
    print("采集所有电影完成！")
    print("正在开始准备写入文件····")
    return ContentLists

def SaveCVS(ContenLists):
    if not os.path.exists('./DouBan'):
        os.mkdir('./DouBan')
    try:
        os.remove('./DouBan/MV.csv')
    except:
        pass
    with open('./DouBan/MV.csv', 'a')as f:
        f.write('电影名, 评分, 链接, 图片地址' + '\n')
        for ContenList in ContenLists:
            f.write(ContenList['电影名'] + ',' + ContenList['评分'] + ',' + ContenList['链接'] + ',' + ContenList['图片地址'] + '\n')
        print('文件已写入完成！')

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'bid=S3X0xqEuDe0; douban-fav-remind=1; __gads=ID=325982641d75d756:T=1581695651:S=ALNI_MaX8VdbavsyZmjMt2IuEp4z4OOpQg; ll="118348"; __utmc=30149280; __utma=223695111.1906555551.1583420349.1583420349.1583420349.1; __utmb=223695111.0.10.1583420349; __utmc=223695111; __utmz=223695111.1583420349.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=30149280.1158841288.1581695650.1583420349.1583420349.3; __utmz=30149280.1583420349.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1583420349; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1583420349%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __yadk_uid=HeAvEEVH3ASJU25vpCZTlhMH45m11GFf; ct=y; _pk_id.100001.4cf6=b88618ec651debfc.1583420349.1.1583420374.1583420349'
    }
    SaveCVS(GetJson(UrlAdd(), headers))