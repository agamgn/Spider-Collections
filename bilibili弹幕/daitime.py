import requests
import re

headers = {
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
"Cookie":"stardustpgcv=0606; _uuid=B6CA2B1E-5DFB-4275-149D-D6100A9AEF4E30007infoc; CURRENT_FNVAL=16; buvid3=8F7D7F0B-19E4-425D-8708-AB71B87A8FD4155819infoc; sid=asvzmtg7; rpdid=|(u|kJR|JRm)0J'ul)JuJJuJJ; INTVER=1; DedeUserID=511634882; DedeUserID__ckMd5=83993beb74d570a2; SESSDATA=02052a4f%2C1585726806%2Cebcbba31; bili_jct=f1ce97b07a4a93ab8e80ffbc69fc91d8",
"Host":"api.bilibili.com"
}

class Danmu:
    def __init__(self, appear_time, text):
        self.appear_time = appear_time
        self.text = text


def getdm(url):
    danmu_raw = requests.get(url, headers = headers).content.decode('utf-8')
    danmu_raw_list = re.findall(r"<d .*?</d>", danmu_raw)
    danmu_list = []
    for item in danmu_raw_list:
        m = re.match(r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?)>(.*?)</d>', item) # group(3和5)废弃
        # danmu_list.append(m.group(6))
        danmu_list.append(Danmu(format_time(float(m.group(1))),m.group(6)))
    return danmu_list



# 出現的時間
def format_time(time_raw):
    hour = str(int(time_raw / 3600))
    if hour != '0':
        time_raw %= 3600
    minute = str(int(time_raw / 60))
    if minute != '0':
        time_raw %= 60
    if len(minute) == 1:
        minute = "0" + minute
    second = str(round(time_raw, 2))
    if '.' in second:
        if len(second.split('.')[0]) == 1:
            second = "0" + second
        if len(second.split('.')[1]) == 1:
            second = second + "0"
    else:
        if len(second) == 1:
            second = "0" + second + ".00"
        else:
            second = second + ".00"
    return hour + ':' + minute + ':' + second



def generate_ass(danmu_list):
    text=""
    for danmu in danmu_list:
        text += "%s#%s\n" % (danmu.appear_time, danmu.text)
    return text

def main():
    starturl="https://api.bilibili.com/x/v2/dm/history?type=1&oid=142147168&date=2020-01-12"
    endurl="https://api.bilibili.com/x/v2/dm/history?type=1&oid=142147168&date=2020-03-02"
    url="https://api.bilibili.com/x/v2/dm/history?type=1&oid=142147168&date="
    from datetime import datetime, date, timedelta
    # today = (date.today()).strftime("%Y-%m-%d")
    # yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    yesterday= (date.today()).strftime("%Y-%m-%d")
    for i in range(11,41):
        danmu_list=getdm(url+yesterday)
        plan=generate_ass(danmu_list)
        with open(yesterday + ".txt", "w+",encoding='utf-8') as files:
            files.write(plan)                       
        yesterday = (date.today() + timedelta(days = -i)).strftime("%Y-%m-%d")

if __name__ == "__main__":
    main()