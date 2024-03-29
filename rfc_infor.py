#!/usr/bin/env python
# coding: utf-8
#%%
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from dateutil import parser

def re_crawler(url,pattern):
    content = requests.get(url)
    res = re.findall(pattern, content.text, re.I)
    return (res)

def title_process(title):
    p1 = re.compile(r'[[](.*?)[]]', re.S)
    p2 = re.compile(r'[(](.*?)[)]', re.S)

    date='null'
    status='null'
    stream='null'
    area='null'
    wg='null'
    obsoleted=False
    if title != "Not Issued":
            date = re.findall(p1,title)[0]
            oth_inf = re.findall(p2,title)
            for brac in oth_inf:
                if "TXT" in brac or "DOI" in brac:
                    pass
                if "Update" in brac:
                    pass
                if "Obsoleted-By"in brac:
                    obsoleted=True
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

            title_table.append([date,status,stream,area,wg,obsoleted])

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
title_table=[]
df[1].apply(title_process)
df_info=pd.DataFrame(title_table,columns=['date','status','stream','area','wg','obsoleted'])

#%%
df_title=pd.DataFrame(re_crawler('https://www.rfc-editor.org/rfc-index2.html',r"<b>(.*?)</b>"))
df_title=df_title[2:]
df_title.reset_index(drop=True,inplace=True)

#%%
num_list=[]
for n in df[df[1]!="Not Issued"][0]:
    num_list.append(int(str(n).split(';')[1]))
df_num=pd.DataFrame(num_list)

#%%
df_nti=pd.concat([df_num,df_title,df_info],axis=1)
df_nti.columns=['num','title','date','status','stream','area','wg','obsoleted']
df_nti.tail(10)


#%%
txt_content = 'EPP | FTP | HTTP | iCalendar | IDNA | IMAP | LDAP | MIME | OAuth | POP3 | URN | vCard | XMPP | RTSP | RTP | SDP | SIP | VoIP | DHCPv4 | DHCPv6 | DNS | IPv4 | IPv6 | MIPv4 | MIPv6 | MPLS | NTP | PWE3 | CAPWAP | Diameter | NETCONF | RADIUS | SMI | SNMP | YANG | BGP | CIDR | IS-IS | LDP | OSPF | PIM | RSVP-TE | VRRP | DKIM | IKEv1 | IKEv2 | Kerberos | OpenPGP | PEM | SSH | Syslog | TLS | DCCP | MTU+Discovery | PCN | ROHC | SCTP | nat64+or+dns64'
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

#%%
grp=df_nak.groupby('num')
df_akn=grp.agg(lambda x:', '.join(x))
df_result=pd.merge(df_nti,df_akn,how='outer',on='num')
df_result.to_csv('rfc_infor.csv')

#%%
# # df0 = pd.read_csv('rfc_infor.csv')
# # df1 = df_nti.copy().drop(columns=['title','date','status','stream','area','wg'])
# # df_res = pd.merge(df0,df1,how='inner',on='num')
# # df_res.to_csv('rfc_infor.csv')

# # # %%
# # df_res.to_csv('rfc_infor.csv')


# # # %%

# df = pd.read_csv('rfc_infor.csv')
# df.drop(columns=['Unnamed: 0','Unnamed: 0.1'],inplace=True)
# df.head()

# # %%
# df.to_csv('rfc_infor.csv')

# # %%
