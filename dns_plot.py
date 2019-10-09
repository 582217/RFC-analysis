#%%
import pandas as pd
import seaborn as sns 
from matplotlib import pyplot as plt

df = pd.read_csv(r'C:\Users\wuyim\Desktop\rfc_infor.csv')
df.drop(columns='Unnamed: 0',inplace=True)


df_dns=df[df.area2=='DNS'].copy()
df_dns.fillna('null',inplace=True)
for c in df_dns.columns:
    if c != 'num':
        df_dns[c]=df_dns[c].str.strip()



#%%

df_dns['wg'].replace('NON WORKING GROUP','N W G',inplace=True)
plt.figure(figsize=(20, 10))
sns.countplot(x='wg',data=df_dns)
plt.show()


#%%
df_dns['area'].replace('ops','Operations and Management',inplace=True)
df_dns['area'].replace('art','Applications and Real-Time',inplace=True)
df_dns['area'].replace('int','Internet',inplace=True)
df_dns['area'].replace('sec','Security',inplace=True)
df_dns['area'].replace('rai','Applications and Real-Time',inplace=True)
df_dns['area'].replace('app','Applications and Real-Time',inplace=True)
df_dns['area'].replace('tsv','Transport',inplace=True)
plt.figure(figsize=(18, 10))
sns.countplot(x='area',data=df_dns)
plt.show()

#%%
sns.countplot(x='stream',data=df_dns)
plt.show()

#%%
plt.figure(figsize=(25, 10))
sns.countplot(x='status',data=df_dns)

plt.show()


#%%
df_dns['date']=pd.to_datetime(df_dns['date'])
df_dns['year']=df_dns['date'].dt.year


plt.figure(figsize=(20, 10))
sns.countplot(df_dns['year'])

plt.show()

#%%
coun=df_dns.groupby([df_dns['wg'],df_dns['area']],as_index=False).count()
pivo=coun.pivot('wg','area','num')
plt.figure(figsize=(12, 10))
sns.heatmap(pivo,cmap='Reds')


#%%
coun=df_dns.groupby('year',as_index=False).count()
sns.tsplot(coun.num,coun.year)