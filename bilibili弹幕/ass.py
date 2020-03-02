import requests
import re

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"}

# class Danmu:
#     def __init__(self, appear_time, disappear_time, mode, color, text):
#         self.appear_time = appear_time
#         self.disappear_time = disappear_time
#         self.mode = mode
#         self.color = color
#         if self.color == r"\c&HFFFFFF": # 默认白色则删去,压缩空间
#             self.color = ""
#         self.text = text

def get_cid(url):
    html = requests.get(url, headers = headers).content.decode('utf-8')
    if "cid" in html:
        return re.findall(r'"cid":(\d*)', html)
    else:
        return "x"

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

def get_danmu_list(danmu_url):
    danmu_raw = requests.get(danmu_url, headers = headers).content.decode('utf-8')
    danmu_raw_list = re.findall(r"<d .*?</d>", danmu_raw)
    danmu_list = []
    for item in danmu_raw_list:
        m = re.match(r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?)>(.*?)</d>', item) # group(3和5)废弃
        danmu_list.append(Danmu(format_time(float(m.group(1))), format_time(float(m.group(1)) + 8), int(m.group(2)), r"\c&H" + str(hex(int(m.group(4))))[2:].upper(), m.group(6)))
    print(danmu_list)
    return danmu_list


def main():
    url = input("url:")
    cid = get_cid(url)
    print(cid)
    if cid == "x":
        print("cid not found")
        exit(1)
    for ci in cid:
        if ci == 0:
            continue
        else:

            danmu_url = "https://comment.bilibili.com/" + ci + ".xml"
            danmu_raw=requests.get(danmu_url, headers = headers).content.decode('utf-8')
            with open(ci + ".xml", "wb+") as ass_file:
                ass_file.write(danmu_raw.encode("utf-8"))
            # danmu_list = get_danmu_list(danmu_url)
            # print(danmu_list)

    
    
    # ass = generate_ass(danmu_list)
    # with open(cid + ".ass", "wb+") as ass_file:
    #     ass_file.write(ass.encode("utf-8"))

if __name__ == "__main__":
    main()