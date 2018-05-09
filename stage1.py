
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
# import bokeh.io
# from bokeh.charts import Donut, HeatMap, Histogram, Line, Scatter, show, output_notebook, output_file
# from bokeh.plotting import figure
import string
# import gensim.models.word2vec as w2v
import multiprocessing
import os
import copy
import re
import sklearn
import seaborn as sns
import wordcloud
get_ipython().run_line_magic('matplotlib', 'inline')
from subprocess import check_output


# ## Read dataset
# read all the data and convert them into pandas dataframes

# In[45]:


import json
from pprint import pprint

cwd = os.getcwd()
# print(cwd)
frames = []
for file in os.listdir('lyrics/'):
    date = file.split('.')[0].split('_')[-1]
    with open(cwd + '/lyrics/' + file,'r') as f:
        df = pd.DataFrame(json.load(f)).dropna()
        df['time'] = pd.Timestamp(date)
        frames.append(df)
raw_data = pd.concat(frames)    


# In[52]:


raw_data.head(10)


# ## Data preprocessing
# 1. str to lower
# 2. remove stop words
# 3. remove non-lyric content (eg: [Chorus: David McRae])
# 4. remove punctuations

# In[64]:


import copy
billboard = copy.deepcopy(raw_data)
stop = stopwords.words('english')

def preprocess(lyric):
    lyric = lyric.lower()
    lyric = re.sub(r'\[.*?\]', '', lyric)  # remove [*] pattern
    lyric = lyric.replace("'s",'')
    lyric = lyric.replace("'ve",'')
    lyric = lyric.replace("'",'')    # ' must be ignored
    lyric = lyric.replace("-",' ')
    
    translator = str.maketrans(string.punctuation,' '*len(string.punctuation))
    lyric = lyric.translate(translator)
    tokens = nltk.word_tokenize(lyric)
    
    return tokens

eg = """
[Verse 1] She calls out to the man on the street \"Sir, can you help me? It's cold and I've nowhere to sleep 
Is there somewhere you can tell me?\"  He walks on, doesn't look back He pretends he can't hear her Starts 
to whistle as he crosses the street Seems embarrassed to be there  [Chorus] Oh think twice, it's another day 
for You and me in paradise Oh think twice, it's just another day for you You and me in paradise  
[Verse 2] She calls out to the man on the street He can see she's been crying She's got blisters on the soles 
of her feet She can't walk but she's trying  [Chorus] Oh think twice, it's another day for You and me in paradise 
Oh think twice, it's just another day for you You and me in paradise  [Bridge] Oh lord, is there nothing more 
anybody can do? Oh lord, there must be something you can say  [Verse 3] You can tell from the lines on her face 
You can see that she's been there Probably been moved on from every place 'cos she didn't fit in there  
[Chorus] Oh think twice, it's another day for You and me in paradise Oh think twice, it's just another day 
for you You and me in paradise  ","title": "Another Day In Paradise
"""


# In[65]:


billboard['lyrics'] = billboard['lyrics'].apply(lambda x: preprocess(x))
billboard['lyrics'] = billboard['lyrics'].apply(lambda x:[w for w in x if w not in stop])
billboard.head(10)


# ## Vocabulary count

# ## 
