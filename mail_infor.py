#%%
from lxml import etree
import requests
import re
import time
import pandas as pd

#%%
def re_crawler(url, pattern):
    content = requests.get(url)
    res = re.findall(pattern, content.text, re.I)
    return (res)

all_mail_lists = re_crawler('https://mailarchive.ietf.org/arch/browse/',
                            r"<a class=\"browse-link\"(.*?)</a>")

for i in range(len(all_mail_lists)):
    all_mail_lists[i] = all_mail_lists[i].split('\"')[1]

all_mail_lists
#%%
data = []
err_data=[]
for mail_list in all_mail_lists:
    try:

        row = []
        base_url = 'https://mailarchive.ietf.org'
        page_url = base_url + mail_list
        page = requests.get(page_url)
        tree = etree.HTML(page.text)
        mes_count = tree.xpath('//*[@id="message-count"]')[0].text
        date_end = tree.xpath('//*[@id="msg-list"]/div/div/div[1]/div[3]')[0].text

        time.sleep(0.5)

        page_url = page_url + '?so=date'
        page = requests.get(page_url)
        tree = etree.HTML(page.text)
        date_start = tree.xpath(
            '//*[@id="msg-list"]/div/div/div[1]/div[3]')[0].text

        print('________')
        ml_name = mail_list.split('/')[-2]
        row = [ml_name, mes_count, date_start, date_end]
        data.append(row)

        print(len(data))
        time.sleep(0.5)
    except:
        print(mail_list)
        err_data.append(mail_list)

#%%
df=pd.DataFrame(data,columns={'name','mes_count','start','end'})
df.to_csv(r'C:\Users\wuyim\RFC-analysis\mail_infor.csv')