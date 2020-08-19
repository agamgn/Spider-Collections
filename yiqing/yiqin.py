import requests
from lxml import etree
import re
import csv
 
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
}
 
# 设置选项
choice = int(input("请输入要获取的内容 1 感染总人数 2 每日新增感染人数 3 现存感染人数 4 总死亡人数 5 每日新增死亡人数\n请输入: "))
 
# 设置文件名称
if choice == 1:
    f_name = '全球感染总人数'
elif choice == 2:
    f_name = '每日新增感染'
elif choice == 3:
    f_name = '现存感染'
elif choice == 4:
    f_name = '总死亡人数'
elif choice == 5:
    f_name = '每日新增死亡'
 
 
# 打开csv
f = open(f"{f_name}.csv", "a", newline="")
writer = csv.writer(f)
 
# csv文件的内容
url = 'https://www.worldometers.info/coronavirus/'
res = requests.get(url=url, headers=headers).content.decode()
html = etree.HTML(res)
# xpath选择节点
node_list = html.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr/td[2]/a')
# 循环遍历节点
for i in node_list:
    # 获取国家名称，国家的链接
    name = i.xpath('text()')[0]
    href = url + i.xpath('@href')[0]
    res_data = requests.get(url=href, headers=headers).content.decode()
    html_data = etree.HTML(res_data)
    # 尝试发送请求
    try:
        data = html_data.xpath(f'/html/body/div/div/div/div[{choice}]/div/script/text()')[0]
    except:
        # 跳过这个链接
        continue
    # 写入日期
    if name == "USA" or name == "China":
        compiles_date = re.compile("categories: \[(.*?)\]")
        date = compiles_date.findall(data)[0].replace('"', "").split(',')
        date.insert(0, "")
        writer.writerow(date)
    # 正则匹配到具体数据
    compiles_count = re.compile("data: \[(.*?)\]")
    try:
        counts = compiles_count.findall(data)[0]
    except:
        continue
    # 分割成列表
    counts_list = counts.split(",")
    # 在列表的第一行插入数据，注意列表的insert方法没有返回值
    counts_list.insert(0, name)
    try:
        writer.writerow(counts_list)
    except:
        continue
    print("》》》》》》》数据获取成功", name)
f.close()