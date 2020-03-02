import requests
import re

headers = {
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
"Cookie":"stardustpgcv=0606; _uuid=B6CA2B1E-5DFB-4275-149D-D6100A9AEF4E30007infoc; CURRENT_FNVAL=16; buvid3=8F7D7F0B-19E4-425D-8708-AB71B87A8FD4155819infoc; sid=asvzmtg7; rpdid=|(u|kJR|JRm)0J'ul)JuJJuJJ; INTVER=1; DedeUserID=511634882; DedeUserID__ckMd5=83993beb74d570a2; SESSDATA=02052a4f%2C1585726806%2Cebcbba31; bili_jct=f1ce97b07a4a93ab8e80ffbc69fc91d8",
"Host":"api.bilibili.com"
}


def getdm(url):
    danmu_raw = requests.get(url, headers = headers).content.decode('utf-8')
    danmu_raw_list = re.findall(r"<d .*?</d>", danmu_raw)
    danmu_list = []
    for item in danmu_raw_list:
        m = re.match(r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?)>(.*?)</d>', item) # group(3和5)废弃
        danmu_list.append(m.group(6))
    return danmu_list

def main():
    starturl="https://api.bilibili.com/x/v2/dm/history?type=1&oid=142147168&date=2020-01-12"
    endurl="https://api.bilibili.com/x/v2/dm/history?type=1&oid=142147168&date=2020-03-02"
    url="https://api.bilibili.com/x/v2/dm/history?type=1&oid=142147168&date="
    from datetime import datetime, date, timedelta
    # today = (date.today()).strftime("%Y-%m-%d")
    # yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
    yesterday= (date.today()).strftime("%Y-%m-%d")
    for i in range(31,41):
        danmu_list=getdm(url+yesterday)
        with open(yesterday + ".txt", "w+",encoding='utf-8') as files:
            files.write("\n".join(danmu_list))                       
        yesterday = (date.today() + timedelta(days = -i)).strftime("%Y-%m-%d")


    

    

    
    
    
    # ass = generate_ass(danmu_list)
    # with open(cid + ".ass", "wb+") as ass_file:
    #     ass_file.write(ass.encode("utf-8"))

if __name__ == "__main__":
    main()