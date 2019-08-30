#!/usr/bin/env python
# coding: utf-8

# In[9]:
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib import request
import time
from dateutil import parser

def re_crawler(url,pattern):
    content = request.urlopen(url).read()
    res = re.findall(pattern, content.decode('utf-8'), re.I)
    return (res)

def title_process(title):
    p1 = re.compile(r'[[](.*?)[]]', re.S)
    p2 = re.compile(r'[(](.*?)[)]', re.S)

    date='null'
    status='null'
    stream='null'
    area='null'
    wg='null'

    if title != "Not Issued":
            date = re.findall(p1,title)[0]
            oth_inf = re.findall(p2,title)
            for brac in oth_inf:
                if "TXT" in brac or "DOI" in brac:
                    pass
                if "Update" in brac:
                    pass
                if "Obsolete"in brac:
                    pass
                if "Status" in brac:
                    status = brac.split(":")[1]
                if "Stream" in brac:
                    if"Area" in brac and "WG" in brac:
                        stream = brac.split(",")[0].split(":")[1]
                        area = brac.split(",")[1].split(":")[1]
                        wg = brac.split(",")[2].split(":")[1]
                    if"Area" not in brac and "WG" in brac:
                        stream = brac.split(",")[0].split(":")[1]
                        wg = brac.split(",")[1].split(":")[1]
                    if "Area" not in brac and "WG" not in brac:
                        stream = brac.split(":")[1]

            title_table.append([date,status,stream,area,wg])


def get_table(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tables = soup.select('table')
    df_list = []
    for table in tables:
        df_list.append(pd.concat(pd.read_html(table.prettify())))
    df_table = pd.concat(df_list)
    return (df_table)

def tonum (i):
    return (int(i.split(' ')[0].split(u'\xa0')[1]))

#%%
df=get_table('https://www.rfc-editor.org/rfc-index2.html')
df=df[5:]


#%%
title_table=[]

df[1].apply(title_process)
df_info=pd.DataFrame(title_table,columns=['date','status','stream','area','wg'])
df_info

#%%
df_title=pd.DataFrame(re_crawler('https://www.rfc-editor.org/rfc-index2.html',r"<b>(.*?)</b>"))
df_title=df_title[2:]
df_title.reset_index(drop=True,inplace=True)
df_title

#%%
num_list=[]
for n in df[df[1]!="Not Issued"][0]:
    num_list.append(int(str(n).split(';')[1]))
df_num=pd.DataFrame(num_list)
df_num

#%%
df_nti=pd.concat([df_num,df_title,df_info],axis=1)
df_nti.columns=['num','title','date','status','stream','area','wg']

#%%
txt = open(r"C:\Users\wuyim\Desktop\area2.txt", "r+")
txt_content = txt.read()
txt.close()
area2_list=txt_content.split(' | ')
ls_serch_res=list()
ls_num4k=list()
ls_area2=list()
df_kwds=pd.DataFrame()
for area2 in area2_list:
    num4kwd_url='https://www.rfc-editor.org/search/rfc_search_detail.php?title='+area2+'&page=All'
    kwd_url='https://www.rfc-editor.org/search/rfc_search_detail.php?page=All&title='+area2+'&pubstatus[]=Any&pub_date_type=any&keywords=keyson&sortkey=Number&sorting=ASC'
    ls_serch_res=get_table(num4kwd_url)['Number'][12:].apply(tonum).tolist()
    ls_area2+=[area2 for n in range(len(ls_serch_res))]
    ls_num4k+=ls_serch_res
    df_kwds=df_kwds.append(re_crawler(kwd_url,r'<td colspan="6">(.*?)</td>'))
    print(len(ls_area2))
    print(len(ls_num4k))
    print(len(df_kwds))
    print('------------')
    time.sleep(20)

#%%
df_num4k=pd.DataFrame(ls_num4k)
df_area2=pd.DataFrame(ls_area2)
df_kwds.reset_index(drop=True,inplace=True)
df_nak=pd.concat([df_num4k,df_area2,df_kwds],axis=1)
df_nak.drop_duplicates(inplace=True)
df_nak.columns=['num','area2','key words']
df_nak


#%%
grp=df_nak.groupby('num')
df_akn=grp.agg(lambda x:', '.join(x))

df_result=pd.merge(df_nti,df_akn,how='outer',on='num')
df_result

#%%
df_result.to_csv(r'C:\Users\wuyim\Desktop\rfc_infor.csv')

#%%
