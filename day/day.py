import requests
import re
from bs4 import BeautifulSoup
 
url='http://wufazhuce.com/one/'#每一期的链接共同的部分
words=['0']*1800#定义一个长度为1800的列表，用来保存每一句话，并初始化为全‘0’
for i in range(0,100):
    s=str(i)#数字类型转为字符串类型
    print(i)
    currenturl=url+s#当前期的链接
    try:
        res=requests.get(currenturl)
        res.raise_for_status()
    except requests.RequestException as e:#处理异常
        print(e)
    else:
        html=res.text#页面内容
        soup = BeautifulSoup(html,'html.parser')
        a=soup.select('.one-titulo')#查找期次所在的标签
        b=soup.select('.one-cita')#查找“每日一句”所在的标签
        #print(b)
        index=re.sub("\D","",a[0].string.split()[0])#从“vol.xxx”提取期次数值作为下标
        #print(index)
        if(index==''):
            continue
        #print(b[0].string.split())
        words[int(index)]=b[0].string.split()#将该期“每日一句”存入列表
        #print(words[int(index)])
print("begin!!!!!!!!!!!!!!!")      
f=open('C:\\Users\\lsy\\Desktop\\one.TXT','w')#将每句话写入这个txt文件中，先打开
for i in range(1,1774):
    if(words[i]=='0'):
        continue
    else:
        print(words[i])
        f.writelines('VOL.'+str(i)+'\n')#写入期次和换行
        f.writelines('    ')#每句话开始空四格
        f.writelines(words[i])#写入该句话
        f.writelines('\n\n')#换行，并空一行写入下一句        
f.close()#关闭文件