# -*- coding:utf-8 -*-
import requests
import re
import random

local=input('请输入下载位置:')
while (1):
    trouble=0
    n=random.randrange(2,1000)
    url=(r'http://www.doutula.com/photo/list/?page=%d'%n)
    result=requests.get(url).text
    pattern=re.compile('data-original="(.*?)"\salt="(.*?)"\sclass=',re.S)
    image_urls=re.findall(pattern,result)
    '''for image_url in image_urls:
        yield1 ={
            'image': image_url[0],
            }'''
    for image_url in image_urls:
        image_name=image_url[1]
        image=requests.get(image_url[0]).content
        try:
            with open(r'%s\%s'%(local,image_name+'.'+image_url[0].split('.')[-1]),'wb')as file:
                file.write(image)
        except:
            print('下载错误')
            trouble+=1
    print('页码%d下载完成\n下载错误%d张'%(n,trouble))
        #print(image_url[0])