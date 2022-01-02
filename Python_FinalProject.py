import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import threading 
import requests
from bs4 import BeautifulSoup
import os 
import sys
font = FontProperties(fname=os.environ['WINDIR']+'\\Fonts\\kaiu.ttf', size=16)
###############################################
def printTotal(addr,diction,string): ##print total number
    myset = set(addr)
    for index in myset:
        ##print(index,addr.count(index))
        diction.update({str(index):addr.count(index)})
    
    plt.figure(figsize=(20,5))
    plt.bar(range(len(diction)), list(diction.values()), align='center')
    plt.xticks(range(len(diction)), list(diction.keys()),fontproperties=font)
    plt.title(string,fontproperties=font)
    
##################################################
def countBook(url):
    html = requests.get(url).content.decode('utf-8')
    sp = BeautifulSoup(html,'html.parser') ##抓HTML table 資料
    ##li = sp.find('table',{'id':"fbonly"})## 抓title
    ##print(li_row.text)
      
    table = sp.find('table',{'id':"fbonly"}) ## by TAG
    rows = table.find_all('tr')
    
    
    for idx,row in enumerate(rows[1:]): ##抓營業地址
        address = row.find('td',{'headers':'companyAddress'})
        ##print(address.text[0:3]) ##抓縣市
        addr_1000W.append(address.text[0:3]) ##把每個縣市append to a new list
    ##printTotal(addr_1000W)
    
    ##li = sp.find('table',{'id':"fbonly_200"})## 抓title
    ##li_row = li.find("caption")
    ##print(li_row.text)
    
    
    
    table = sp.find('table',{'id':"fbonly_200"})
    rows = table.find_all('tr')
    
    for idx,row in enumerate(rows[1:]): ##抓營業地址
        address = row.find('td',{'headers':'companyAddress2'})
        ##print(address.text[0:3]) ##抓縣市
        addr_200W.append(address.text[0:3]) ##把每個縣市append to a new list
        
    ##printTotal(addr_200W)
############################INPUT########################################

S_year = input("Start Year = ")
S_month = input("Start Month = ")

E_year = input("End Year = ")
E_month = input("End Month = ")

#123456
#######################拿指定區間的URL，加到list去########################

new_Y = 0
new_M = 0

url_list = []

sub = int(E_year) - int(S_year) 

for m in range(int(S_month),int(E_month)+1+12*sub,2):
    new_Y = m //12
    new_M = m % 12
    if new_M > 10:
        url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(new_Y+int(S_year))+str(new_M)
        url_list.append(url)
    else:
        url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(new_Y+int(S_year))+'0'+str(new_M)
        url_list.append(url)

######################################################################
addr_1000W = []
addr_200W = []

count_1000W = dict()
count_200W = dict()

workers = []

########################Threading#####################################

for i in range(len(url_list)):
    t = threading.Thread(target=countBook,args=(str(url_list[i]),))
    t.start()
    workers.append(t)
for t in workers:
    t.join()

########################################################################
print("-----------")

printTotal(addr_1000W,count_1000W,'2000W 各縣市統計')

printTotal(addr_200W,count_200W,'200W 各縣市統計')

#######################################################################





    



    
