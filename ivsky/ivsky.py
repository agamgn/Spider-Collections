import requests,os,time,threading,queue,socket
socket.setdefaulttimeout(60)
 
headers2 = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3732.400 QQBrowser/10.5.3817.400',
'Cookie':'Hm_lvt_862071acf8e9faf43a13fd4ea795ff8c=1573821045; _pk_ref.5.c0e8=%5B%22%22%2C%22%22%2C1573821045%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DKIqh9hZOaGfCjVK-AuinlS7oFMFsSfbW6Gp0JDGP8pW%26wd%3D%26eqid%3Dd436465b000b4310000000025dce99a3%22%5D; _pk_ses.5.c0e8=1; statistics_clientid=me; arccount49954=c; arccount51723=c; arccount56060=c; Hm_lpvt_862071acf8e9faf43a13fd4ea795ff8c=1573821909; _pk_id.5.c0e8=9e5d0a92e62bd205.1573821045.1.1573821909.1573821045.',
'Referer':'https://www.ivsky.com/'
}
while True:
    txt_list = os.listdir('./txt')
    for index,txt in enumerate(txt_list): print('%s:%s'%(index,txt))
 
    txt_name = input('请输入数字序号并按回车确定：')
    print('输入完成，请等待')
    urls = []
    for i in open('./txt/%s'%txt_list[int(txt_name)],'r',encoding='utf-8').readlines():
        if not i == '\n':
            imgs = {}
            img = eval(i.split('\n')[0])
            path = './图片收集下载/' + str(img['location']).replace('-','/') +  '/' + img['img_name'] + '.jpg'
            file_path = os.path.dirname(path)
            imgs['path'] = path
            imgs['url'] = img['img_url']
            # print(imgs)
            urls.append(path+'####'+img['img_url'])
 
 
    q = queue.Queue()
 
    # Python获取指定目录下所有子目录、所有文件名
    print('正在获取指定目录下所有子目录、所有文件名')
    pic_exis = []
    file_dir = './图片收集下载/%s'%txt_list[int(txt_name)].replace('.txt','')
    for root, dirs, files in os.walk(file_dir):
        # print('root_dir:', root)  # 当前目录路径
        # print('sub_dirs:', dirs)  # 当前路径下所有子目录
        # print('files:', files)  # 当前路径下所有非目录子文件
        if not len(files) == 0:
            pic_exis.extend(files)
    print(pic_exis)
 
    for index,url in enumerate(urls):
        # print(index,url)
        url_path = os.path.dirname(url.split('####')[0]).replace(' ','')
 
        if not os.path.exists(url_path): os.makedirs(url_path)
        q.put(url)
 
    start = time.time()
    def fetch_img_func(q):
        while True:
            try:
                url = q.get_nowait()# 不阻塞的读取队列数据
                url_path = url.split('####')[0].replace(' ','')
                url_img = url.split('####')[1]
                print('正在下载：' + url_path)
 
                i = q.qsize()
            except Exception as e:
                print (e)
                break
            # print ('Current Thread Name Runing %s ... ' % threading.currentThread().name)
            print("当前还有%s/%s个任务"% (i,len(urls)))
 
            pic_name = url_path.split('/')[-1]
            if not pic_name in pic_exis:
                res = requests.get(url_img,headers=headers2,timeout=60,stream=True)
                if res.status_code == 200:
                    # save_img_path = './img/%s.jpg'%str(i)
                    save_img_path = url_path
                    # 保存下载的图片
 
                    with open(save_img_path, 'wb') as fs:
                        for chunk in res.iter_content(1024):
                            fs.write(chunk)
            print('图片已存在')
 
    num=4  #线程数
    threads =[]
    for i  in range(num):
        t = threading.Thread(target=fetch_img_func, args=(q, ), name="child_thread_%s"%i)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
 
    print(time.time()-start)