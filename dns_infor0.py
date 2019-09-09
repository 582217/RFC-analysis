#%%
import requests
import json
import pandas as pd
import time

df = pd.read_csv(r'C:\Users\wuyim\Desktop\rfc_infor.csv')
df.drop(columns='Unnamed: 0',inplace=True)
df_dns=df[df.area2=='DNS'].copy()
df_dns=df_dns.reset_index(drop=True)

#%%
dcount_list=[]
for rfcnum in df_dns['num']:
    print(rfcnum)
    url='https://datatracker.ietf.org/doc/rfc%s/doc.json'%rfcnum

    page=requests.get(url).text
    data=json.loads(page)

    d_count=len(data['rev_history'])-1
    dcount_list.append(d_count)

    time.sleep(1)
    print(d_count)
print(dcount_list)

#%%
df_dcl=pd.DataFrame(dcount_list)
df_dcl

#%%
df_res=pd.concat([df_dns,df_dcl],axis=1)
df_res=df_res.rename(columns={0:'drafts count'})
df_res.to_csv(r'C:\Users\wuyim\Desktop\dns_infor0.csv')


#%%
from matplotlib import pyplot as plt
import seaborn as sns 
plt.figure(figsize=(20, 10))
sns.countplot(x='drafts count',data=df_res)
plt.show()


#%%
print(df_res[10<df_res['drafts count']])
df_res.to_csv(r'C:\Users\wuyim\RFC-analysis\dns_infor0.csv')

#%%
