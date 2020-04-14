 
import os,time,requests,re
from lxml import etree
 
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Referer':'https://www.meitulu.com/t/changtui/',
    'Cookie': 'UM_distinctid=16f94d6dc9e568-0898b8c4c5d86b-645d7c2d-144000-16f94d6dc9f2f2; CNZZDATA1255357127=738626102-1578744969-%7C1578747140'
}
 
'https://www.meitulu.com/gangtai/'
main_url = 'https://www.meitulu.com/t/changtui/'
resp = requests.get(main_url, headers=headers)
text = resp.content.decode('utf-8')
html = etree.HTML(text)
 
#print('start-end：3-6')
#start = int(input('start:'))
#end = int(input('end:'))
 
for li in html.xpath('//ul[@class="menu"]/li'):
    frnqu_url = li.xpath('.//@href')[0]
    frnqu_name = li.xpath('./a/text()')[0]
    print(frnqu_url,frnqu_name)
    resp = requests.get(frnqu_url, headers=headers)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)
    pages = 1
    try:
        pages = html.xpath('//*[@id="pages"]/a/text()')[-2]
    except:
        pages = 1
    for page in range(1,int(pages)+1):
        detil_url = frnqu_url+'%s.html'%page
        # if detil_url == 'https://www.meitulu.com/t/fengsuniang/1.html':detil_url = frnqu_url
        if page==1:detil_url = frnqu_url
        print(detil_url)
        try:
            resp = requests.get(detil_url, headers=headers)
        except:
            time.sleep(5)
            resp = requests.get(detil_url, headers=headers)
        text = resp.content.decode('utf-8')
        html = etree.HTML(text)
        for li in html.xpath('//ul[@class="img"]/li'):
            title = li.xpath('string(.//p[@class="p_title"]/a/text())')
            title = re.sub('[\/:*?"<>|]', ' ', title)
            urls = li.xpath('./p[@class="p_title"]/a/@href')[0]
            if not re.findall('https',urls):
                url = 'https://www.meitulu.com'+ urls
            else:
                url = urls
            img = [li.xpath('./a/img/@src')[0]]
            num = re.findall(r'\d+',li.xpath('./p[1]/text()')[0])[0]
            try:
                resp = requests.get(url, headers=headers)
            except:
                time.sleep(5)
                resp = requests.get(url, headers=headers)
            text = resp.content.decode('utf-8')
            html = etree.HTML(text)
            img_pages = 1
            try:
                img_pages = html.xpath('//*[@id="pages"]/a/text()')[-2]
            except:
                img_pages = 1
            for img_page in range(1,int(img_pages)+1):
                img_url = url.replace('.html','_%s.html'%img_page)
                if img_page == 1: img_url = url
                try:
                    resp = requests.get(img_url, headers=headers)
                except:
                    time.sleep(5)
                    resp = requests.get(img_url, headers=headers)
                text = resp.content.decode('utf-8')
                html = etree.HTML(text)
                imgs = html.xpath('//*[@class="content"]//img/@src')
                for i in imgs:
                    img.append(i)
            all = {'分区':frnqu_name,'所在页数':page,'图片数量':num,'标题':title,'链接':url,'图片':img}
            print(all)
            url = all['链接']
            id = re.findall('\d+', url)[0]
            if len(all['图片']) != 0:
                for index, img in enumerate(all['图片']):
 
                    out_dir = './美图录/all下载/%s/' % all['标题']
                    out_name = '%s--#--%s.jpg' % (all['标题'], str(index))
                    out_path = out_dir + out_name
                    if not os.path.exists(out_path):
                        print('开始下载',page,img, all['标题'])
                        text = ''
                        try:
                            text = requests.get(img).content
                        except:
                            time.sleep(5)
                            try:
                                text = requests.get(img).content
                            except:
                                pass
                        if not os.path.exists(out_dir): os.makedirs(out_dir)
                        try:
                            open(out_path, 'wb').write(text)
                        except:
                            pass
                    else:
                        print('pic已存在',page,img, all['标题'])