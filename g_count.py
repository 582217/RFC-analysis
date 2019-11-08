#%%
from selenium import webdriver
import pandas as pd
import time,random

#%%
df = pd.read_csv(r'C:\Users\wuyim\Desktop\rfc_infor.csv')
df.drop(columns='Unnamed: 0',inplace=True)

df_dns=df[df.area2=='DNS'].copy()

serch_res=[]
err_list=[]
for num in df_dns['num']:
    num=str(num)
    try:
        driver = webdriver.Chrome()     # 打开 Chrome 浏览器
        driver.get("https://www.google.com.hk/search?q=rfc"+num+"&btnG=Search&safe=active&gbv=1")
        res_count = driver.find_element_by_xpath('//*[@id="resultStats"]')
        serch_res.append([num,res_count.text])
        print(serch_res[-1])
        time.sleep(1)
        driver.close()
    except:
        err_list.append(num)
    time.sleep(random.randint(160,200))

dns_serch_res=pd.DataFrame(serch_res)
#%%
dns_serch_res=pd.DataFrame(serch_res)
dns_serch_res.to_csv(r'C:\Users\wuyim\Desktop\dns_serch_res.csv')

#%%
dns_serch_res=pd.read_csv('dns_serch_res.csv')

def to_num(str0):
    str1 = str0.split('（')[0]
    str2 = filter(str.isdigit, str1)
    str3 = list(str2)
    count = "".join(str3)
    count = int(count)
    return(count)

dns_serch_res['1']=dns_serch_res['1'].apply(to_num)
dns_serch_res.sort_values('1',ascending=False,inplace=True)
dns_serch_res

