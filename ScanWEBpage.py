import requests
import sys
import threading
import queue
import xlrd

#py3 urlv3.py 'filename' 'threadnum'
list_name = sys.argv[1]
num = int(sys.argv[2])

quit = queue.Queue()
threading_num = num

#创建一个空数组存储url地址
url_list=[]
#打开excel
data = xlrd.open_workbook(list_name)
#获取第一个sheet
table1=data.sheets()[0]
#获取行数
nrows1=table1.nrows
for i in range(nrows1):
    #读取a1，b1的值
    value_row=table1.cell(i,0).value
    value_col=table1.cell(i,1).value
    #拼接为url
    url='http://'+value_row+':'+str(int(value_col))
    #添加url到数组
    url_list.append(url)

for line in url_list:
    line = line.rstrip()
    quit.put(line)


def crawler():
    while not quit.empty():
        url = quit.get()
        try:
            requests.packages.urllib3.disable_warnings()
            content = requests.get(url, verify=False, allow_redirects=True, timeout=5)
            #判断响应状态码是否为200
            if content.status_code == requests.codes.ok:
                print (url,'',requests.codes.ok)
        except requests.RequestException as e:
            pass

if __name__ == '__main__':
    for i in range(threading_num):
        t = threading.Thread(target=crawler)
        t.start()
