#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import numpy as np


# In[3]:


fec = pd.read_csv('datasets/fec/P00000001-ALL.csv')


# In[4]:


fec.info()


# In[5]:


fec.iloc[123456]


# In[6]:


unique_cands = fec.cand_nm.unique()


# In[7]:


unique_cands


# In[8]:


unique_cands[2]


# In[9]:


parties = {'Bachmann, Michelle' : 'Republican',
           'Cain, Herman' : 'Republican',
           'Gingrich, Newt' : 'Republican',
           'Huntsman, Jon' : 'Republican',
           'Johnson, Gary Earl' : 'Republican',
           'McCotter, Thaddeus G' : 'Republican',
           'Obama, Barack' : 'Democrat',
           'Paul, Ron' : 'Republican',
           'Pawlenty, Timothy' : 'Republican',
           'Perry, Rick' : 'Republican',
           "Roemer, Charles E. 'Buddy' III" : 'Republican',
           'Romney, Mitt' : 'Republican',
           'Santorum, Rick' : 'Republican'}


# In[10]:


fec.cand_nm[123456:123461]


# In[11]:


fec.cand_nm[123456:123461].map(parties)


# In[12]:


fec['party'] = fec.cand_nm.map(parties)


# In[13]:


fec['party'].value_counts()


# In[14]:


(fec.contb_receipt_amt > 0).value_counts()


# In[15]:


fec = fec[fec.contb_receipt_amt > 0]


# In[16]:


fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]


# In[17]:


#14.5.1 직업 및 고용주에 따른 기부 통계


# In[18]:


fec.contbr_occupation.value_counts()[:10]


# In[19]:


occ_mapping = {
    'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
    'INFORMATION REQUESTED' : 'NOT PROVIDED',
    'INFORMATION REQUESTED (BEST EFFORTS)' : 'NOT PROVIDED',
    'C.E.O': 'CEO'
}


# In[20]:


f = lambda x: occ_mapping.get(x,x)
fec.contbr_occupation = fec.contbr_occupation.map(f)


# In[21]:


emp_mapping = {
    'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
    'INFORMATION REQUESTED' : 'NOT PROVIDED',
    'SELEF' : 'SELF-EMPLOYED',
    'SELEF' : 'SELF-EMPLOYED',
    'SELF EMPLOYED' : 'SELF-EMPLOYED',
}


# In[22]:


f = lambda x: emp_mapping.get(x,x)
fec.contbr_employer = fec.contbr_employer.map(f)


# In[23]:


by_occupation = fec.pivot_table('contb_receipt_amt',
                               index='contbr_occupation',
                               columns='party', aggfunc='sum')


# In[24]:


over_2mm = by_occupation[by_occupation.sum(1) > 2000000]


# In[25]:


over_2mm


# In[26]:


over_2mm.plot(kind='barh')


# In[27]:


def get_top_amounts(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    return totals.nlargest(n)


# In[28]:


grouped = fec_mrbo.groupby('cand_nm')


# In[29]:


grouped.apply(get_top_amounts, 'contbr_occupation', n=7)


# In[30]:


grouped.apply(get_top_amounts, 'contbr_employer', n=10)


# In[31]:


# 14.5.2 기부금액


# In[32]:


bins = np.array([0,1,10,100,1000,10000,
                 100000, 1000000, 10000000])


# In[33]:


labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)


# In[34]:


labels


# In[35]:


grouped = fec_mrbo.groupby(['cand_nm', labels])


# In[36]:


grouped.size().unstack(0)


# In[37]:


bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)


# In[38]:


normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)


# In[39]:


normed_sums


# In[40]:


normed_sums[:-2].plot(kind='barh')


# In[41]:


# 14.5.3 주별 기부 통계


# In[42]:


grouped = fec_mrbo.groupby(['cand_nm', 'contbr_st'])


# In[43]:


totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)


# In[44]:


totals = totals[totals.sum(1) > 100000]


# In[45]:


totals[:10]


# In[46]:


percent = totals.div(totals.sum(1), axis=0)


# In[47]:


percent[:10]


# In[ ]:




