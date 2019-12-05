import requests,json,os,subprocess
 
 
# 发post请求，获取5条内容（title、author、下载url）
def getContent(music_name,type):
    print('正在获取'+type+'资源...')
    url = 'http://music.ifkdy.com/'
    data = {'input': music_name,
            'filter': 'name',#kuwo   netease
            'type': type,
            'page': '1'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'#这个必须带 否则出错
    }
    try:
        response = requests.post(url,headers=headers,data=data)
        Html_dict = json.loads(response.content.decode())
        music1= Html_dict['data'][0]
        music2 = Html_dict['data'][1]
        music3 = Html_dict['data'][2]
        music4 = Html_dict['data'][3]
        music5 = Html_dict['data'][4]
        print(type+'资源获取成功')
        return music1, music2, music3, music4, music5
    except:
        print(type+'资源获取失败')
        return []
 
#选择是否下载？下载哪一个？
def select(musicTuple):
    if musicTuple==[]:
        return 0
    print('-------------------音乐目录-------------------\n0、不下载')
    num = 1
    for music in musicTuple:
        print(str(num) + '、' + music['title'] + ' ' + music['author'])
        num += 1
    choice = input('请输入数字序号：')
    if choice==0:
        return 0
    else:
        return musicTuple[int(choice)-1]
 
#开始下载
def download(music):
    if music==0:
        return 0
    else:
        print('-------------------开始下载-------------------')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        try:
            data = requests.get(music['url'], headers=headers, stream=True)
            if (not (os.path.exists('e://音乐spider'))):
                os.mkdir('e://音乐spider')
            with open('E://音乐spider//{}.mp3'.format(music['title'] + ' ' + music['author']), 'wb')as f:
                for j in data.iter_content(chunk_size=512):
                    f.write(j)
                print('下载成功：' + music['title'] + ' ' + music['author'])
            path = 'e://音乐spider//{}.mp3'.format(music['title'] + ' ' + music['author'])
            return path
        except:
            print('下载失败：'+music['title'] + ' ' + music['author'])
 
def run():
    music_name = input('请输入音乐名称或音乐人姓名：')
    #发post请求，获取5条内容（title、author、下载url）
    musicTuple = getContent(music_name,'netease')
    #选择是否下载？true-->下载哪一个？true--->return music  false--->return
    music = select(musicTuple)
    #开始下载
    path = download(music)
    #音乐播放
    subprocess.Popen(path,shell=True)
 
if __name__ == '__main__':
    run()