#%%
import requests
import json
import pandas as pd
import time
from lxml import etree
import re
 


#%%

df = pd.read_csv('rfc_infor.csv')
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
df_res.to_csv('dns_infor0.csv')


#%%
from matplotlib import pyplot as plt
import seaborn as sns 
plt.figure(figsize=(20, 10))
sns.countplot(x='drafts count',data=df_res)
plt.show()


#%%
print(df_res[10<df_res['drafts count']])
df_res.to_csv('dns_infor0.csv')

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
#%%
df=pd.merge(df_dns,dns_serch_res,how='outer',left_on='num',right_on='0')

#%%
df.sort_values('1',ascending=False,inplace=True)
df

#%%
df0 = pd.read_csv('rfc_infor.csv')
dfd = pd.read_csv('dns_infor0.csv')
df0.drop(columns=['Unnamed: 0','title','date','status','stream','area','wg','area2','key words'],inplace=True)
df=pd.merge(dfd,df0,how='inner',on='num')
df.drop(columns=['Unnamed: 0'],inplace=True)
df

# %%
df.to_csv('dns_infor0.csv')

# %%
df=pd.read_csv('dns_infor0.csv')
df_ps=df[df.status==' PROPOSED STANDARD']
df_ps[df.obsoleted==False].to_csv('psn.csv')
# %%
df=pd.read_csv('dns_ps_F.csv')
df.drop(columns='Unnamed: 0',inplace=True)

# %%
df.head()

# %%
for n in df['num']:
    url='https://www.rfc-editor.org/info/rfc{}'.format(n)
    page = requests.get(url)
    tree = etree.HTML(page.text)
    abstract = tree.xpath(
        '//*[@id="post-127"]/div/p[5]/text()')[0]
    abstract=abstract.replace('\n','').replace('\r',' ')
    print(abstract)
    f = open('dns_ps_F_abstract.txt','a')
    f.write(abstract)
    f.write('\n')
    f.close()
    time.sleep(3)

# %%
l=[]
for line in open(r"C:\Users\wuyim\github\keywords_extraction_rake\output.txt"):  
    p = re.compile(r'[\'](.*?)[\']', re.S)  #最小匹配 
    l.append(re.findall(p,line))
# %%
for n in df['num']:
    f = open('dnspdfkeywords','a')
    f.write(str(n))
    f.write(str(l.pop(0)))
    f.write('\n')
    f.close()

# %%
