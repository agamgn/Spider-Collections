import os 
import datetime
 
docList = os.listdir('./b')  #特定目录下的文件存入列表
docList.sort()   # 显示当前文件夹下所有文件并进行排序



str_time = datetime.datetime.now().strftime('%Y-%m-%d')  
with open('{0}.txt'.format(str_time), "w+",encoding='utf-8') as f:
    for i in docList:
        with open ('./b/{0}'.format(i),  "r",encoding='utf-8') as rnew:
            f.write(rnew.read())
         
    

