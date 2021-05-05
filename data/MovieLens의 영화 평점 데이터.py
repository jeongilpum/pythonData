#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#MovieLens의 영화 평점 데이터


# In[3]:


pd.options.display.max_rows = 10
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('datasets/movielens/users.dat', sep='::',
                      header=None, names=unames)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('datasets/movielens/ratings.dat', sep='::',
                        header=None, names=rnames)
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('datasets/movielens/movies.dat', sep='::',
                       header=None, names=mnames)


# In[7]:


users[:5]


# In[5]:


ratings[:5]


# In[6]:


movies[:5]


# In[8]:


ratings


# In[9]:


data = pd.merge(pd.merge(ratings, users), movies)


# In[10]:


data


# In[11]:


data.iloc[0]


# In[12]:


mean_ratings = data.pivot_table('rating', index='title',
                                columns='gender', aggfunc='mean')


# In[13]:


mean_ratings[:5]


# In[14]:


ratings_by_title = data.groupby('title').size()


# In[15]:


ratings_by_title[:10]


# In[16]:


active_titles = ratings_by_title.index[ratings_by_title >= 250]


# In[17]:


active_titles


# In[18]:


mean_ratings = mean_ratings.loc[active_titles]


# In[19]:


mean_ratings


# In[20]:


top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)


# In[21]:


top_female_ratings[:10]


# In[22]:


# 평점 차이 구하기


# In[23]:


mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']


# In[24]:


sorted_by_diff = mean_ratings.sort_values(by='diff')


# In[25]:


sorted_by_diff[:10]


# In[26]:


sorted_by_diff[::-1][:10]


# In[27]:


rating_std_by_title = data.groupby('title')['rating'].std()


# In[28]:


rating_std_by_title = rating_std_by_title.loc[active_titles]


# In[30]:


# 평점 내림차순으로 Series 정렬


# In[ ]:


rating_std_by_title.sort_values(ascending=False)[:10]

