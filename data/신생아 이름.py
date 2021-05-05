#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[2]:


# 신생아 이름


# In[3]:


get_ipython().system('head -n 10 datasets/babynames/yob1880.txt')


# In[4]:


names1880 = pd.read_csv('datasets/babynames/yob1880.txt',
                        names=['name', 'sex', 'births'])


# In[5]:


names1880


# In[6]:


names1880.groupby('sex').births.sum()


# In[7]:


years = range(1880, 2011)


# In[8]:


pieces = []


# In[9]:


columns = ['name', 'sex', 'births']


# In[10]:


for year in years:
    path = 'datasets/babynames/yob%d.txt' %year
    frame = pd.read_csv(path, names=columns)
    
    frame['year'] = year
    pieces.append(frame)


# In[11]:


names = pd.concat(pieces, ignore_index=True)


# In[12]:


names


# In[13]:


total_births = names.pivot_table('births', index='year',
                                 columns='sex', aggfunc=sum)


# In[14]:


total_births.tail()


# In[15]:


#연도와 성별별 출산수
total_births.plot(title='Total births by sex and year')


# In[16]:


def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group


# In[17]:


names = names.groupby(['year', 'sex']).apply(add_prop)


# In[18]:


names


# In[19]:


names.groupby(['year', 'sex']).prop.sum()


# In[20]:


def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]
grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)


# In[21]:


top1000.reset_index(inplace=True, drop=True)


# In[22]:


top1000


# In[23]:


boys = top1000[top1000.sex == 'M']


# In[24]:


girls = top1000[top1000.sex == 'F']


# In[25]:


total_births = top1000.pivot_table('births', index='year',
                                   columns='name',
                                   aggfunc=sum)


# In[26]:


total_births.info()


# In[27]:


subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]


# In[28]:


# 연도별 남아 및 여아 이름 추이
subset.plot(subplots=True, figsize=(12,10), grid=False,
            title="Number of births per year")


# In[29]:


table = top1000.pivot_table('prop', index='year',
                            columns='sex', aggfunc=sum)


# In[30]:


# 인기 있는 이름 1000개의 연도별/성별 비율
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))


# In[31]:


df = boys[boys.year == 2010]


# In[32]:


df


# In[33]:


prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()


# In[34]:


prop_cumsum[:10]


# In[35]:


prop_cumsum.values.searchsorted(0.5)


# In[36]:


df = boys[boys.year == 1900]


# In[37]:


in1900 = df.sort_values(by='prop', ascending=False).prop.cumsum()


# In[38]:


in1900.values.searchsorted(0.5) +1


# In[39]:


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1


# In[40]:


diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)


# In[41]:


diversity = diversity.unstack('sex')


# In[42]:


diversity.head()


# In[43]:


# 연도별 이름 다양성 지수
diversity.plot(title='Number of popular names in top 50%')


# In[44]:


get_last_letter = lambda x: x[-1]


# In[45]:


last_letters = names.name.map(get_last_letter)


# In[46]:


last_letters.name = 'last_letter'


# In[47]:


table = names.pivot_table('births', index=last_letters,
                          columns=['sex','year'], aggfunc=sum)


# In[48]:


subtable = table.reindex(columns=[1910, 1960, 2010], level='year')


# In[49]:


subtable.head()


# In[50]:


subtable.sum()


# In[51]:


letter_prop = subtable / subtable.sum()


# In[52]:


letter_prop


# In[53]:


#이름의 끝 글자 비율
fig, axes = plt.subplots(2,1, figsize=(10,8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',
                      legend=False)


# In[54]:


letter_prop = table / table.sum()


# In[55]:


dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T


# In[56]:


dny_ts.head()


# In[57]:


# d/n/y로 끝나는 이름을 가진 남아의 연도별 출생 추이
dny_ts.plot()


# In[58]:


all_names = pd.Series(top1000.name.unique())


# In[59]:


lesley_like = all_names[all_names.str.lower().str.contains('lesl')]


# In[60]:


lesley_like


# In[61]:


filtered = top1000[top1000.name.isin(lesley_like)]


# In[62]:


filtered.groupby('name').births.sum()


# In[63]:


table = filtered.pivot_table('births', index='year',
                             columns='sex', aggfunc='sum')


# In[64]:


table = table.div(table.sum(1), axis=0)


# In[65]:


table.tail()


# In[66]:


# Lesley와 비슷한 이름의 비율
table.plot(style={'M': 'k-', 'F': 'k-'})


# In[ ]:




