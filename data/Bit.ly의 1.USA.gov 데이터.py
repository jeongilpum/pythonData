#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from collections import defaultdict
from collections import Counter
import pandas as pd
import seaborn as sns
import numpy as np


# In[2]:


# Bit.ly의 1.USA.gov 데이터


# In[3]:


path = 'datasets/bitly_usagov/example.txt'


# In[4]:


records = [json.loads(line) for line in open(path)]


# In[5]:


records[0]


# In[6]:


# 파이썬으로 표준시간대 세어보기


# In[7]:


time_zones = [rec['tz'] for rec in records if 'tz' in rec]


# In[8]:


time_zones[:10]


# In[11]:


def get_counts(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts


# In[13]:


counts = get_counts(time_zones)


# In[14]:


counts['America/New_York']


# In[15]:


len(time_zones)


# In[16]:


def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


# In[17]:


top_counts(counts)


# In[18]:


counts = Counter(time_zones)


# In[19]:


counts.most_common(10)


# In[20]:


# pandas로 표준시간대 세어보기


# In[21]:


frame = pd.DataFrame(records)


# In[22]:


frame.info()


# In[23]:


frame['tz'][:10]


# In[24]:


tz_counts = frame['tz'].value_counts()


# In[25]:


tz_counts[:10]


# In[26]:


clean_tz = frame['tz'].fillna('Missing')


# In[27]:


clean_tz[clean_tz == ''] = 'Unknown'


# In[28]:


tz_counts = clean_tz.value_counts()


# In[29]:


tz_counts[:10]


# In[30]:


subset = tz_counts[:10]


# In[32]:


# usa.gov 데이터에서 가장 많이 나타난 시간대
sns.barplot(y=subset.index, x=subset.values)


# In[33]:


frame['a'][1]


# In[34]:


frame['a'][50]


# In[35]:


frame['a'][51][:50]


# In[36]:


results = pd.Series([x.split()[0] for x in frame.a.dropna()])


# In[37]:


results[:5]


# In[38]:


results.value_counts()[:8]


# In[39]:


cframe = frame[frame.a.notnull()]


# In[40]:


cframe['os'] = np.where(cframe['a'].str.contains('Windows'),
                         'Windows', 'Not Windows')


# In[41]:


cframe['os'][:5]


# In[42]:


by_tz_os = cframe.groupby(['tz','os'])


# In[43]:


agg_counts = by_tz_os.size().unstack().fillna(0)


# In[44]:


agg_counts[:10]


# In[45]:


indexer = agg_counts.sum(1).argsort()


# In[46]:


indexer[:10]


# In[47]:


count_subset = agg_counts.take(indexer[-10:])


# In[48]:


count_subset


# In[49]:


agg_counts.sum(1).nlargest(10)


# In[50]:


count_subset = count_subset.stack()


# In[51]:


count_subset.name = 'total'


# In[52]:


count_subset = count_subset.reset_index()


# In[53]:


count_subset[:10]


# In[55]:


# 윈도우 사용자와 비윈도우 사용자별 시간대
sns.barplot(x='total', y='tz', hue='os', data=count_subset)


# In[56]:


def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group


# In[57]:


results = count_subset.groupby('tz').apply(norm_total)


# In[59]:


# 윈도우 사용자와 비윈도우 사용자별 시간대 비율
sns.barplot(x='normed_total', y='tz', hue='os', data=results)


# In[ ]:




