# //*[@id="message-thread"]/ul
#%%
from lxml import etree
import requests
import re
import time
import pandas as pd
import datetime


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
dic_data = {}
l_err_data = []
for mail_list in all_mail_lists:
    try:
        base_url = 'https://mailarchive.ietf.org'
        page_url = base_url + mail_list + '/?gbt=1'
        page = requests.get(page_url)
        tree = etree.HTML(page.text)
        mes_count = tree.xpath('//*[@id="message-count"]')[0].text
        mes_count = int(mes_count.split(' ')[0])

        if mes_count > 1:

            str_latest_date = tree.xpath(
                '//*[@id="msg-list"]/div/div/div[1]/div[3]')[0].text
            latest_date = datetime.datetime.strptime(str_latest_date, '%Y-%m-%d')
            latest_date = latest_date.date()
            today = datetime.date.today()
            interval = today - latest_date

            if interval.days < 90:
                print('start  ', mail_list)
                s_thr = set()

                for i in range(1, min(mes_count, 40)):

                    id = tree.xpath('//*[@id="msg-list"]/div/div/div[' + str(i) +
                                    ']/div[7]')[0].text
                    page2 = requests.get(
                        'https://mailarchive.ietf.org/arch/ajax/msg/?id={}'.format(
                            id))
                    tree2 = etree.HTML(page2.text)
                    mes_thread = tree2.xpath('//*[@id="message-thread"]/ul/li')

                    tit = tree2.xpath('//*[@id="msg-body"]/h3')[0].text

                    if len(mes_thread) > 3:
                        s_thr.add(tit)

                    time.sleep(1)

                dic_data[mail_list] = s_thr
                print('end  ', s_thr)
                print('_____________')
            else:
                print('pass this wg ,OLD ', mail_list)
        else:
            print('pass this wg ,NONE ', mail_list)
        time.sleep(1)
    except:
        l_err_data.append(mail_list)
#%%
