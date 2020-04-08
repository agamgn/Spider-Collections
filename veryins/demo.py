import datetime,bs4,time,requests,json,pymysql

def db_exe(sql,judge):
    num = 1
    if judge == 'find':
        while True:
            if num > 5:
                return '失败'
            try:
                cur.execute(sql)
                return cur.fetchall()
            except:
                print('查询用户失败，正在重试！')
                num+=1
    else:
        while True:
            if num > 5:
                return '失败'
            pymysql.escape_string(sql)
            try:
                cur.execute(sql)
                db.commit()
                print('写入数据库成功')
                break
            except Exception  as e:
                print('写入数据库失败，正在重试'+str(num)+str(e))
                time.sleep(2)
                num+=1
                db.rollback()

def soup_bs(url):
    num = 1
    while True:
        try:
            if num>5:
                print('重试失败超过五次，退出本次循环')
                return '失败'
            res = requests.get(url, headers=headers, timeout=10)
            soup = bs4.BeautifulSoup(res.content, 'lxml')  # 解析网页源码
            print('正在解析网页源码，请稍等')
            return soup
        except:
            print('网页源码解析失败，正在重试第：'+str(num)+'次')
            num+=1
            time.sleep(3)

def add_user():
    sql = "select ins_number from ins_index where ins_name='' or ins_name is null "
    results = db_exe(sql,'find')#返回ins_name为空的用户
    print(len(results))
    if results =='失败':
        return '失败'
    if len(results) == 0:
        print('没有新添加的用户！,执行下一步')
        return
    else:
        for result in results:
            print('新添加用户为:'+result[0])
            print('正在获取该用户的用户名=====')
            url = veryins_url + '/' +result[0]
            soup = soup_bs(url)
            if soup =='失败':
                print('获取用户'+result[0]+'的页面失败，跳出该用户查询')
                continue
            ins_name = soup.find(attrs={'id': "username"}).get('data-fullname')
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('当前用户的用户名为：'+ins_name)
            if ins_name == '' :
                sql = ("update ins_index SET ins_name='%s',time_add='%s',time_update='%s' where ins_number='%s'" %(result[0],now_time,now_time,result[0]))
                db_exe_1 = db_exe(sql,'add')
                if db_exe_1 == '失败':
                    print('添加用户失败，跳出本次添加！')
                    continue
                print('新用户添加成功，进入页面分析')
            else:
                sql = ("update ins_index set ins_name='%s',time_add='%s',time_update='%s' where ins_number='%s'"%(ins_name,now_time,now_time,result[0]))
                db_exe_1 = db_exe(sql,'add')
                if db_exe_1 == '失败':
                    print('添加用户失败，跳出本次添加！')
                    continue
                print('新用户添加成功，进入页面分析')

def judge_ins():
    sql = 'select ins_number from ins_index'
    results = db_exe(sql,'find')
    print('一共'+str(len(results))+'位用户')
    for result in results:
        sql = ("select * from ins_mes where ins_num='%s'"%(result[0]))
        db_exe_1 = db_exe(sql,'find')
        if len(db_exe_1)>0:
            print('用户：'+result[0]+'执行更新操作')
            ins_update_1 = ins_add(result[0],'u')
            if ins_update_1 == '失败':
                print('用户'+result[0]+'执行更新操作失败，跳过该用户')
                continue
            if ins_update_1 == '更新完成':
                print(result[0]+'用户更新完成')
                continue
        else:
            print('用户：' + result[0] + '执行录入操作')
            ins_add_1 = ins_add(result[0],'a')
            if ins_add_1 == '失败':
                print('用户' + result[0] + '执行录入操作失败，跳过该用户')
                continue

def ins_add(add_ins,aoru):
    num =1
    num_1 =1
    while True:
        if num_1 >=5:
            print('用户网页打不开，跳过'+add_ins)
            return '失败'
        url = veryins_url+'/' +add_ins
        print(url)
        soup = soup_bs(url)
        if soup =='失败':
            print('分析'+add_ins+'失败，跳过该用户')
            return '失败'
        try:
            items = soup.findAll(attrs={'class': "item"})
            num_item = soup.findAll(attrs={'class': "count"})[0].get_text().split('帖子')[0]#找到帖子总数
            print(num_item)
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for item in items:
                img_wrap = item.find(class_="img-wrap")
                data_code = img_wrap.get('data-code')
                img_p_link = str(r'https://www.veryins.com/p/' + data_code)
                sql = ("select * from ins_mes where ins_code ='%s'" %data_code)
                db_exe_1 = db_exe(sql,'find')
                if len(db_exe_1) == 0:
                    sql = ("insert into ins_mes (ins_num,ins_code,ins_p_link,time_add,time_update) values('%s','%s','%s','%s','%s')"%(add_ins, data_code, img_p_link, now_time, now_time))
                    db_exe_1 = db_exe(sql,'add')
                    if db_exe_1 != '失败':
                        print('已写入数据库' + str(num) + '条')
                        num+=1
                else:
                    if aoru == 'u':
                        return '更新完成'
            break
        except Exception  as e:
            print('写入前12条数据出现错误，错误原因：'+ str(e))
            print('正在重试第'+str(num_1)+'次')
            time.sleep(2)
            num_1+=1
    #开始执行post，刷新更多数据
    try:
        uid_class_1 = soup.findAll(attrs={'class': "row"})[0]
        uid_class = uid_class_1.findAll('div')[0].get('class')[0].lower()
        uid_num = uid_class_1.findAll('div')[0].get(uid_class)
        next_cursor = soup.find(class_='list').get('next-cursor')
    except Exception  as e:
        print('获取当前博主的post数据失败，跳过该博主，错误原因：'+str(e))
        return '失败'
    while True:
        post_mes = str(r'https://www.veryins.com/user/post?next=' + next_cursor + r'&uid=' + uid_num)
        print(post_mes)
        while True:
            try:
                res1 = json.loads(requests.post(url=post_mes, headers=headers, timeout=10).text)
                break
            except:
                print('post失败，正在重试！')
        for k in res1['nodes']:
            data_code = k['code']
            img_p_link = str(r'https://www.veryins.com/p/' + data_code)
            sql = ("select * from ins_mes where ins_code ='%s'"%data_code)
            db_exe_1 = db_exe(sql, 'find')
            if len(db_exe_1) == 0:
                sql = ("insert into ins_mes (ins_num,ins_code,ins_p_link,time_add,time_update) values('%s','%s','%s','%s','%s')"%(add_ins, data_code, img_p_link, now_time, now_time))
                db_exe_1 = db_exe(sql, 'add')
                if db_exe_1 != '失败':
                    print('已写入数据库' + str(num) + '条')
                    num += 1
            else:
                if aoru == 'u':
                    return '更新完成'
                print('该条数据已存在，跳过')
        if str(res1['page_info']['has_next_page']) == 'True':
            next_cursor = res1['page_info']['end_cursor']
            time.sleep(3)
        else:
            break

def ins_info():
    sql = ('select ins_mes.ins_code from ins_mes left join all_pic_link on ins_mes.ins_code=all_pic_link.ins_code  where all_pic_link.ins_code is null')
    results_code = db_exe(sql,'find')
    print('获得所有未处理code')
    print(str(len(results_code)))
    for result_code in results_code:
        err = 1
        print('开始读取数据组建链接')
        url_2 = 'https://www.veryins.com/p/' +result_code[0]
        print(url_2)
        num = 1
        print('获取网页成功，正在分析图片地址')
        while True:
            try:
                soup = soup_bs(url_2)
                swiper_slide = soup.findAll(class_='swiper-slide')
                if len(swiper_slide) == 0:
                    try:
                        img_wrapper = soup.find(class_='imgwrapper').find('img').attrs['src'].replace('amp', '')
                        sql = ("insert into all_pic_link (ins_code,ins_pic_link) values('%s','%s')" % (
                        result_code[0], img_wrapper))
                        db_exe_1 = db_exe(sql, 'add')
                        if db_exe_1 == '失败':
                            print('写入失败')
                        else:
                            print('已写入数据库第' + str(num) + '张')
                            num += 1
                    except:
                        video_wrapper = soup.find(class_='imgwrapper').find('source').attrs['src'].replace('amp', '')
                        sql = ("insert into all_pic_link (ins_code,ins_pic_link) values('%s','%s')" % (
                        result_code[0], video_wrapper))
                        db_exe_1 = db_exe(sql, 'add')
                        if db_exe_1 == '失败':
                            print('写入失败')
                        else:
                            print('已写入数据库第' + str(num) + '部')
                            num += 1
                else:
                    for i in swiper_slide:
                        try:
                            img_link = i.find('img').attrs['src'].replace('amp', '')
                            sql = ("insert into all_pic_link (ins_code,ins_pic_link) values('%s','%s')" % (
                            result_code[0], img_link))
                            db_exe_1 = db_exe(sql, 'add')
                            if db_exe_1 == '失败':
                                print('写入失败')
                            else:
                                print('已写入数据库第' + str(num) + '张')
                                num += 1
                        except:
                            video_wrapper = i.find('source').attrs['src'].replace('amp', '')
                            try:
                                sql = ("insert into all_pic_link (ins_code,ins_pic_link) values('%s','%s')" % (
                                result_code[0], video_wrapper))
                                db_exe_1 = db_exe(sql, 'add')
                                if db_exe_1 == '失败':
                                    print('写入失败')
                                else:
                                    print('已写入数据库第' + str(num) + '部')
                                    num += 1
                            except:
                                print('出错，回滚2')
                                time.sleep(2)
                                continue
                dele = 1
                break
            except:
                print('出错重试！')
                time.sleep(2)
                print('获取网页失败，正在重试第：' + str(err) + '次')
                err+=1
                if err >5:
                    print(result_code[0]+'的网址分析失败次数超过五次，删除该链接')
                    sql = ("delete from ins_mes where ins_code='%s'"%(result_code[0]))
                    db_exe(sql,'add')
                    dele = 0
                    break
        if dele == 0:
            continue
        comments_link = soup.findAll(class_='comment-txt')
        for i in comments_link:
            herf_txt = i.find('a').get_text()
            comments_txt = pymysql.escape_string(i.find('p').get_text())
            try:
                sql = """insert into all_comments (ins_code,ins_commenter,comments) values('%s','%s','%s')"""%(result_code[0], herf_txt, comments_txt)
                print(sql)
                db_exe_1 = db_exe(sql, 'add')
                if db_exe_1 == '失败':
                    print('写入失败')
                else:
                    print('将评论写入数据库')
            except:
                print('出错，回滚3')
                time.sleep(2)
        article = pymysql.escape_string(soup.find(class_='caption').get_text())
        try:
            sql ="insert into all_articles (ins_code,articles) values('%s','%s')"%(result_code[0],article)
            print(sql)
            db_exe_1 = db_exe(sql, 'add')
            if db_exe_1 == '失败':
                print('写入失败')
            else:
                print('将帖子内容写入数据库')
        except:
            print('出错，回滚4')
            time.sleep(2)

if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    veryins_url = 'https://www.veryins.com'
    db =pymysql.connect('localhost',user = 'root',passwd = 'toor',db = 'veryins')
    cur = db.cursor()
    ins_long = cur.execute('select * from ins_index')
    add_user_1 = add_user()
    if add_user_1 =='失败':
        print('查询当前用户失败，跳出本次查询')
    judge_ins_1 = judge_ins()
    if judge_ins_1 =='失败':
        print('获取用户图片失败，跳出本次爬取')
    ins_info()
    print('进程执行完毕')
    sql = ("select ins_number from ins_index")
    results = db_exe(sql,'find')
    print('共有'+str(len(results))+'位博主')
    for result in results:
        sql = ("select * from ins_mes where ins_num='%s'"%result[0])
        db_exe_1 = db_exe(sql,'find')
        sql = ("select all_pic_link.id from ins_mes inner join all_pic_link on ins_mes.ins_num='%s' and ins_mes.ins_code=all_pic_link.ins_code"%result[0])
        db_exe_2 = db_exe(sql,'find')
        print(result[0]+'博主共有'+str(len(db_exe_1))+'篇帖子和'+str(len(db_exe_2))+'张照片和视频')