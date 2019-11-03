import os,requests,re
from time import sleep
from bs4 import BeautifulSoup
from random import uniform
 
#网址解析
def url_open(url):
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    response = requests.get(url,headers=headers)
    response.encoding = "utf-8"  #该网站的编码格式：utf-8
 
    html =response.text
 
    return html
 
 
#目标链接收集
def collect_url(html,root_url):
    print("正在收集全站已完结的小说链接.....")
    novel_name_all = []
    novel_url_all = []
 
    soup = BeautifulSoup(html,"html.parser")
    totle_pages = int((soup.find("div",class_="pagelink").em.text).split("/")[1])  #查找总页数
    #print(totle_pages)
 
    #逐页打开手收集小说链接
    for page in range(1,totle_pages+1):
        url = root_url + 'modules/article/articlelist.php?fullflag=1&page={}'.format(page)
        #print(url)
        html = url_open(url)
        #收集当前页面的小说链接
        p_novel_url = fr'<a href="({root_url}xiaoshuo/.+.html)">'
        novel_url_temp = re.findall(p_novel_url,html)
 
        #将小说链接添加到URL总列表并获取小说名称。
        for novel_url in novel_url_temp:
            novel_url_all.append(novel_url)
            #获取小说名称
            p_novel_name = fr'{novel_url}">(.+)</a>'
            novel_name_temp = re.findall(p_novel_name,html)[0]
            novel_name_all.append(novel_name_temp)
 
        break #减少代码运行时间使用(若爬取全站则此处删除即可)
 
    data = [novel_name_all,novel_url_all]  #将数据进行打包，以便返回多个数据
 
    print("收集工作已完成，准备进入小说内容下载.....")
    sleep(1)
 
    return  data
 
 
#小说内容获取与保存
def get_and_save_data(data):
    novel_name_all = data[0]
    novel_url_all = data[1]
    i = -1  #用于索引获取小说名称
 
    for novel_url in novel_url_all:
        i += 1
        novel_name = novel_name_all[i]  # 获取小说名称
        print()  #交互美观使用
        print("正在下载小说：《%s》"%novel_name)
        print()  #交互美观使用
 
        html_1 = url_open(novel_url)
        soup_1 = BeautifulSoup(html_1, "html.parser")
        chapters_url = soup_1.find("p", class_="btnlinks").a["href"]
 
        #获取所有小说章节URL
        html_2 = url_open(chapters_url)
        soup_2 = BeautifulSoup(html_2, "html.parser")
        chapters_url_all = soup_2.find_all("td", class_="L")
 
        #逐页打开小说章节网址并获取内容保存
        for each in chapters_url_all:
            chapters_url = each.a["href"]
            html = url_open(chapters_url)
 
            soup = BeautifulSoup(html,"html.parser")
            chapters_name = soup.find("dd").h1.text  #抓取章节名称
            print("正在下载《%s》:%s"%(novel_name,chapters_name))
 
            #小说内容抓取
            contents = soup.find("dd",id="contents").text
            with open("%s.txt"%novel_name,"a",encoding="utf-8") as g:
                g.write("\n"*3 + "                               "+chapters_name+str("\n")*3)
                g.write("    "+contents)
 
            slee_time = uniform(0.35,0.75)
            sleep(slee_time) #减轻服务器压力
 
        print("小说%s已下载完毕"%novel_name)
        print("准备进入下一部小说下载")
        sleep(2)
 
        break #减少代码运行时间使用(若爬取全站则此处删除即可)
 
 
#主程序
def main():
    #设置工作路径
    path = r'C:\Users\Administrator\Desktop\test'
    if os.getcwd() != path:
        if os.path.exists(path) == False:
            os.mkdir(path)
            os.chdir(path)
        else:
            os.chdir(path)
    root_url = "https://www.ddxsku.com/"
    target_url = root_url + "full.html"
    data = collect_url(url_open(target_url),root_url)
    get_and_save_data(data)
 
 
if __name__ == "__main__":
    main()